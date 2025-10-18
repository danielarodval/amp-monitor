import uvicorn
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import SessionLocal, init_db
from .models import Metrics, ServerInfo
from .schemas import IngestPayload, ServerInfoCreate, MetricsOut
from .settings import settings

app = FastAPI(title="AMP Metrics API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with SessionLocal() as session:
        yield session

def verify_token(authorization: str | None):
    if not settings.api_auth_token:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid auth")
    token = authorization.removeprefix("Bearer ").strip()
    if token != settings.api_auth_token:
        raise HTTPException(status_code=403, detail="Forbidden")

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/ingest", status_code=201)
async def ingest(payload: IngestPayload, db: AsyncSession = Depends(get_db), authorization: str | None = Header(default=None)):
    verify_token(authorization)
    rec = Metrics(
        application_name=payload.ApplicationName,
        instance_name=payload.InstanceName,
        user_count=payload.UserCount,
        max_users=payload.MaxUsers,
        time=payload.Time,
        uptime=payload.Uptime,
        ram_usage=payload.RAMUsage,
        cpu_usage=payload.CPUUsage,
    )
    db.add(rec)
    await db.commit()
    return {"ok": True, "id": rec.id}

@app.post("/server-info", status_code=201)
async def upsert_server_info(body: ServerInfoCreate, db: AsyncSession = Depends(get_db), authorization: str | None = Header(default=None)):
    verify_token(authorization)
    # simple upsert by (application_name, instance_name)
    q = select(ServerInfo).where(
        ServerInfo.application_name==body.ApplicationName,
        ServerInfo.instance_name==body.InstanceName
    )
    res = await db.execute(q)
    row = res.scalar_one_or_none()
    if row:
        row.max_users = body.MaxUsers
    else:
        row = ServerInfo(application_name=body.ApplicationName, instance_name=body.InstanceName, max_users=body.MaxUsers)
        db.add(row)
    await db.commit()
    return {"ok": True}

@app.get("/metrics", response_model=list[MetricsOut])
async def list_metrics(db: AsyncSession = Depends(get_db), limit: int = 250):
    q = select(Metrics).order_by(Metrics.time.desc()).limit(limit)
    res = await db.execute(q)
    return [m for m in res.scalars().all()]

@app.get("/server-info")
async def list_server_info(db: AsyncSession = Depends(get_db)):
    q = select(ServerInfo).order_by(ServerInfo.application_name, ServerInfo.instance_name)
    res = await db.execute(q)
    return [
        {
            "ApplicationName": s.application_name,
            "InstanceName": s.instance_name,
            "MaxUsers": s.max_users,
            "CreatedAt": s.created_at,
        } for s in res.scalars().all()
    ]

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)

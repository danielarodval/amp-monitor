from pydantic import BaseModel, Field
from datetime import datetime

class IngestPayload(BaseModel):
    UserCount: int = Field(..., ge=0)
    MaxUsers: int = Field(..., ge=0)
    ApplicationName: str
    InstanceName: str
    Time: datetime
    Uptime: int = Field(..., ge=0)
    RAMUsage: float = Field(..., ge=0)
    CPUUsage: float = Field(..., ge=0)

class ServerInfoCreate(BaseModel):
    ApplicationName: str
    InstanceName: str
    MaxUsers: int

class MetricsOut(BaseModel):
    id: int
    ApplicationName: str
    InstanceName: str
    UserCount: int
    MaxUsers: int
    Time: datetime
    Uptime: int
    RAMUsage: float
    CPUUsage: float

    class Config:
        from_attributes = True

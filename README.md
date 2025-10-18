# amp-monitor
Homelab monitoring site: FastAPI ingest for AMP stats → SQLite/Neon, Streamlit/Reflex UI, Nginx on Alpine, Dockerized, Cloudflare Tunnel, CI/CD, security-first.

Code for a lightweight, security-focused monitoring website running on Alpine Linux. It exposes a FastAPI endpoint to receive AMP (CubeCoders) POST updates, persists data to SQLite/Neon, and serves a Streamlit/Reflex dashboard behind Nginx. Packaged with Docker, published via CI/CD, and exposed through Cloudflare Tunnel by default.

# Structure

- FastAPI API to receive AMP POSTs and persist to Neon (Postgres)

- SQLAlchemy 2.x (async) + asyncpg

- Reflex frontend that reads from the API and renders two tables (metrics + servers)

# Production Notes

- Run API with uvicorn (or gunicorn -k uvicorn.workers.UvicornWorker) behind Nginx; expose only through Cloudflare Tunnel as you planned.

- Set CORS_ORIGINS to your Reflex public URL.

- Use a Neon connection string with sslmode=require (already in DATABASE_URL).

- Create a long, random API_AUTH_TOKEN; restrict /ingest to AMP IPs at Nginx if possible.

- For auto-restart on boot, supervise with supervisord/s6 or run both pieces in Docker (compose) per your CI/CD goal.

# Notes / troubleshooting (Alpine-focused)

If asyncpg wheels don’t match your arch and it tries to build, add:
apk add --no-cache build-base python3-dev musl-dev postgresql-dev in backend/Dockerfile before pip install.

Neon must allow sslmode=require (already in DATABASE_URL).

If Reflex fails to start in prod, try: reflex run --env prod --backend-port 3000 (older versions) or pin the Reflex version you used during dev.
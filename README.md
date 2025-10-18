# amp-monitor
Homelab monitoring site: FastAPI ingest for AMP stats → SQLite/Neon, Streamlit/Reflex UI, Nginx on Alpine, Dockerized, Cloudflare Tunnel, CI/CD, security-first.

Code for a lightweight, security-focused monitoring website running on Alpine Linux. It exposes a FastAPI endpoint to receive AMP (CubeCoders) POST updates, persists data to SQLite/Neon, and serves a Streamlit/Reflex dashboard behind Nginx. Packaged with Docker, published via CI/CD, and exposed through Cloudflare Tunnel by default.

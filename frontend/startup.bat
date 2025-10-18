cd frontend
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export API_BASE=http://localhost:8000
reflex run

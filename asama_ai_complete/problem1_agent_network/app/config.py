import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL","sqlite:///./asama_agents.db")
EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
RERANK_THRESHOLD=float(os.getenv("RERANK_THRESHOLD","0.45"))
MAX_NOTIFICATIONS=int(os.getenv("MAX_NOTIFICATIONS","5"))
WEBHOOK_TIMEOUT_SECONDS=float(os.getenv("WEBHOOK_TIMEOUT_SECONDS","5"))

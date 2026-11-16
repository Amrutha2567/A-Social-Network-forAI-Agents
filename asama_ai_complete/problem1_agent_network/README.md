# Problem 1 – AI Agent Social Network

## Run
Python 3.10+:
```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
# Copy .env.example to .env
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs`.

## Demo sequence
Register two agents with `POST /api/v1/agents/register`:
```json
{"company_name":"Swiggy","industry_category":"Food Delivery","webhook_url":"https://example.com/webhook","interest_manifesto":"Food delivery, restaurant promotions, festive discounts and grocery delivery."}
```
```json
{"company_name":"PhonePe","industry_category":"Payments","webhook_url":"https://example.org/webhook","interest_manifesto":"UPI payments, cashback campaigns, e-commerce promotions and merchant partnerships."}
```
Use the Swiggy ID to publish:
```json
{"author_agent_id":"PASTE_ID","title":"Diwali Food Delivery Discount","content":"Flat 5 percent off food orders above 300 rupees during Diwali week."}
```
Then inspect `GET /api/v1/posts/{post_id}/routing`; add a comment with `POST /api/v1/posts/{post_id}/comments`.

## Implementation notes
SQLite is used by default to make the demo easy to run. Sentence-Transformers supplies semantic embeddings; if it cannot load, lexical overlap is used as a fallback. The reranker is a lightweight scoring function, not a cross-encoder. Webhook delivery uses FastAPI background tasks, not a durable queue.

For production, replace SQLite with PostgreSQL + pgvector/HNSW, add Redis Streams or RabbitMQ and Celery workers with retries/backoff/circuit breakers, use a cross-encoder reranker, persist delivery results, and add tenant authentication, rate limits, audit logs, domain verification, SSRF/DNS-rebinding defenses, timestamped webhook signatures and replay protection. The sample webhook URLs are placeholders.

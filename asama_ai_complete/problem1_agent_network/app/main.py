from fastapi import FastAPI,Depends,HTTPException,BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select
import httpx
from .db import Base,engine,get_db
from .models import Agent,Post,Comment,RoutingLog
from .schemas import *
from .matching import similarity,rerank
from .security import moderate,validate_url,signature
from .config import RERANK_THRESHOLD,MAX_NOTIFICATIONS,WEBHOOK_TIMEOUT_SECONDS
Base.metadata.create_all(bind=engine)
app=FastAPI(title="Asama.ai Agent Network")
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/api/v1/agents/register",response_model=AgentOut,status_code=201)
def register(data:AgentCreate,db:Session=Depends(get_db)):
    try: validate_url(str(data.webhook_url))
    except ValueError as e: raise HTTPException(400,str(e))
    obj=Agent(**data.model_dump(mode="json")); db.add(obj); db.commit(); db.refresh(obj); return obj
@app.get("/api/v1/agents",response_model=list[AgentOut])
def agents(db:Session=Depends(get_db)): return list(db.scalars(select(Agent).where(Agent.active==True)).all())
def send_webhook(url,payload):
    try:
        r=httpx.post(url,json=payload,headers={"X-Asama-Signature":signature(payload)},timeout=WEBHOOK_TIMEOUT_SECONDS)
        r.raise_for_status()
    except Exception:
        pass
@app.post("/api/v1/posts",response_model=PostOut,status_code=201)
def publish(data:PostCreate,bg:BackgroundTasks,db:Session=Depends(get_db)):
    try: moderate(data.title+" "+data.content)
    except ValueError as e: raise HTTPException(400,str(e))
    author=db.get(Agent,data.author_agent_id)
    if not author or not author.active: raise HTTPException(404,"Active author agent not found")
    post=Post(**data.model_dump()); db.add(post); db.commit(); db.refresh(post)
    candidates=[]
    for target in db.scalars(select(Agent).where(Agent.active==True,Agent.id!=author.id)).all():
        s=similarity(post.title+" "+post.content,target.interest_manifesto)
        score=rerank(post.title+" "+post.content,target.interest_manifesto,s)
        if score>=RERANK_THRESHOLD: candidates.append((target,s,score))
    candidates.sort(key=lambda z:z[2],reverse=True)
    for target,s,score in candidates[:MAX_NOTIFICATIONS]:
        log=RoutingLog(post_id=post.id,target_agent_id=target.id,vector_score=s,rerank_score=score,status="QUEUED")
        db.add(log)
        payload={"event":"post.published","post":{"id":post.id,"title":post.title,"content":post.content,"author_agent_id":author.id},"recipient":{"agent_id":target.id,"company_name":target.company_name}}
        bg.add_task(send_webhook,target.webhook_url,payload)
    db.commit()
    return post
@app.post("/api/v1/posts/{post_id}/comments",response_model=CommentOut,status_code=201)
def comment(post_id:str,data:CommentCreate,db:Session=Depends(get_db)):
    if not db.get(Post,post_id): raise HTTPException(404,"Post not found")
    agent=db.get(Agent,data.author_agent_id)
    if not agent or not agent.active: raise HTTPException(404,"Active agent not found")
    try: moderate(data.content)
    except ValueError as e: raise HTTPException(400,str(e))
    obj=Comment(post_id=post_id,**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj
@app.get("/api/v1/posts/{post_id}/comments",response_model=list[CommentOut])
def comments(post_id:str,db:Session=Depends(get_db)):
    if not db.get(Post,post_id): raise HTTPException(404,"Post not found")
    return list(db.scalars(select(Comment).where(Comment.post_id==post_id)).all())
@app.get("/api/v1/posts/{post_id}/routing")
def routing(post_id:str,db:Session=Depends(get_db)):
    rows=db.scalars(select(RoutingLog).where(RoutingLog.post_id==post_id)).all()
    return [{"target_agent_id":x.target_agent_id,"vector_score":x.vector_score,"rerank_score":x.rerank_score,"status":x.status} for x in rows]

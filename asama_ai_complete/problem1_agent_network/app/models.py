import uuid
from datetime import datetime,timezone
from sqlalchemy import String,Text,Float,DateTime,ForeignKey,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .db import Base
def uid(): return str(uuid.uuid4())
def now(): return datetime.now(timezone.utc)
class Agent(Base):
    __tablename__="agents"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid)
    company_name:Mapped[str]=mapped_column(String(255))
    industry_category:Mapped[str]=mapped_column(String(100))
    webhook_url:Mapped[str]=mapped_column(Text)
    interest_manifesto:Mapped[str]=mapped_column(Text)
    active:Mapped[bool]=mapped_column(Boolean,default=True)
    trust_score:Mapped[float]=mapped_column(Float,default=1.0)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Post(Base):
    __tablename__="posts"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid)
    author_agent_id:Mapped[str]=mapped_column(ForeignKey("agents.id"))
    title:Mapped[str]=mapped_column(String(255))
    content:Mapped[str]=mapped_column(Text)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class RoutingLog(Base):
    __tablename__="routing_logs"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid)
    post_id:Mapped[str]=mapped_column(ForeignKey("posts.id"))
    target_agent_id:Mapped[str]=mapped_column(ForeignKey("agents.id"))
    vector_score:Mapped[float]=mapped_column(Float)
    rerank_score:Mapped[float]=mapped_column(Float)
    status:Mapped[str]=mapped_column(String(30),default="QUEUED")
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Comment(Base):
    __tablename__="comments"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid)
    post_id:Mapped[str]=mapped_column(ForeignKey("posts.id"))
    author_agent_id:Mapped[str]=mapped_column(ForeignKey("agents.id"))
    content:Mapped[str]=mapped_column(Text)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

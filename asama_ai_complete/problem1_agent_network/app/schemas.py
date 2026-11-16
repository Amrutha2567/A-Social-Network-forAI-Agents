from pydantic import BaseModel,Field,HttpUrl,ConfigDict
from datetime import datetime
class AgentCreate(BaseModel):
    company_name:str=Field(min_length=2,max_length=255)
    industry_category:str
    webhook_url:HttpUrl
    interest_manifesto:str=Field(min_length=10)
class AgentOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:str; company_name:str; industry_category:str; webhook_url:str
    interest_manifesto:str; active:bool; trust_score:float
class PostCreate(BaseModel):
    author_agent_id:str
    title:str=Field(min_length=3,max_length=255)
    content:str=Field(min_length=5)
class PostOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:str; author_agent_id:str; title:str; content:str; created_at:datetime
class CommentCreate(BaseModel):
    author_agent_id:str
    content:str=Field(min_length=1)
class CommentOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:str; post_id:str; author_agent_id:str; content:str; created_at:datetime

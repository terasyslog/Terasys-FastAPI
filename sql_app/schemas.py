from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name : str
    id : str
    class Config:
        orm_mode=True
class UserCreate(UserBase):
    email : str
    pw : str
        
class IssueBase(BaseModel):
    title : str
    detail : str
    solution : str
    author_name : str
    author_id : str
    project_id : str | None
    project_name : str | None
    category_id	: str | None
    category_name : str | None
    write_time : datetime
    update_time : datetime

class IssueCreate(BaseModel):
    title : str
    detail : str
    solution : str
    author_id : str
    project_id : str | None
    category_id	: str | None
    
class Issue(IssueBase):
    key : int
    state : str
    class Config:
        orm_mode=True


    

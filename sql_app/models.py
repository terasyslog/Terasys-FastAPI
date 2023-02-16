from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .database import Base

class Users(Base):
    __tablename__='author_list'
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    pw = Column(String)

class Issue(Base):
    __tablename__='issue_list'
    
    key = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    detail = Column(String)
    solution = Column(String)
    author_name = Column(String)
    author_id = Column(String)
    write_time = Column(Date)
    update_time = Column(Date)
    state = Column(String, default=True)
    project_id = Column(String)
    project_name = Column(String)
    category_id	= Column(String)
    category_name = Column(String)
    
    
class Project(Base):
    __tablename__='project_list'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
class Category(Base):
    __tablename__='category_list'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
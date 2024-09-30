
from database import Base,engine,SessionLocal
from sqlalchemy import Column,String,Integer,Boolean,Date
from sqlalchemy.orm import Session
from datetime import date

from fastapi import FastAPI, Query, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# Set up Jinja2 templates
templates = Jinja2Templates(directory="template")

@app.get("/")
def read_root(request: Request):
     return  templates.TemplateResponse(name="index.html", context={"request": request})



#
# # path parameter by using get method
# @app.get("/item/{item_id}")
# def index(item_id:int):  # put type for validation http://127.0.0.1:8000/item/34
#     return {"product_id" : {item_id}}
#
# # query parameter by using get method
# @app.get("/item/")
# def index(q:int=0, m:Optional[int]=10):  # put type for validation http://127.0.0.1:8000/item/?q=55 , http://127.0.0.1:8000/item/?q=55&m=100
#     return {"product_id" : {q}, "m": {m}}
#
# # request body (it may be get,post,put,delete
# @app.post("/post/")
# def index():
#     return("post request")
#
# #how to validate request json data in post request
# # for returning we need to use model
# class User(BaseModel):
#     name:str = Query(None,min_length=4,max_length=50)  # apply validation by using Query
#     password:str = "welcome@123"   # passing default password
#     address:Optional[str]=None
#
# @app.post("/postitem/")
# def index(user:User):
#     return user   # will return whataver we defined in model "User" by using post request body
#
# # Dependency Injection
# # in this when one function variable coming from anathor function it called dependwncy Injection
#
# # Use of it
# # 1 Shared logic means can use in multiple apis or any where
# # 2 shared database connection
# # 3 Enforce security and auth
#
# async def comman_param(q:Optional[str]=None,skip:int=0,Limit:int=10):
#     return {"q":q,"limit":Limit}
# class CommonParam:
#     def __init__(self,q:Optional[int]=10,skip:int=1,Limit:int=10):
#         self.q = q
#         self.skip = skip
#         self.Limit = Limit
# @app.get("/itemsC")
# async def read_items(commons:CommonParam=Depends(CommonParam)): # callable can be use as a dependency
#     return "total:",commons.q+commons.skip+commons.Limit
#
# @app.get("/items")
# async def read_items(commons:dict=Depends(comman_param)): # callable can be use as a dependency
#     return commons              #callable means function, variavle,class
# @app.get("/users")
# async def add_users(commons:dict=Depends(comman_param)):
#     return commons

# Dependency with yield db connect
# by using sqlalchemy library
# bu using ORM
#
# from database import Base,engine,SessionLocal
# from sqlalchemy import Column,String,Integer,Boolean,Date
# from sqlalchemy.orm import Session
# from datetime import date
#model
class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name=Column(String,index=True)
    last_name = Column(String, nullable=True)
    email=Column(String,index=True)
    number=Column(Integer)
    today_date=Column(String,nullable=True)
    cuntry = Column(String, nullable=True)
    city = Column(String, nullable=True)
    services = Column(String, nullable=True)
    comment = Column(String, nullable=True)
#schema
class UserSchema(BaseModel):

    first_name:str
    last_name:str
    email:str
    number:int
    today_date:str
    cuntry:str
    city:str
    services:str
    comment:str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Base.metadata.create_all(bind=engine) # it create the table whataver we defined in model



# insert data in db table
@app.post("/submit/",response_model=UserSchema) # response_model will respond in jason when we post
def index(user:UserSchema,db:Session=Depends(get_db)):
    #db work to put data into db
    u=User(

    first_name=user.first_name,
    last_name=user.last_name,
    email=user.email,
    number=user.number,
    today_date=user.today_date,
    cuntry=user.cuntry,
    city=user.city,
    services=user.services,
    comment=user.comment
           )
    db.add(u)
    db.commit()
    return u

# # fetch data on url
# @app.get("/users",response_model=list[UserSchema])
# def index(db:Session=Depends(get_db)):
#     return db.query(User).all()
# # update request
#
# @app.put("/users/{user_id}",response_model=UserSchema)
# def update_user(user_id:int,user:UserSchema,db:Session=Depends(get_db)):
#     try:
#         u= db.query(User).filter(User.id==user_id).first()
#         u.email=user.email
#         db.add(u)
#         db.commit()
#         return u
#     except:
#         return HTTPException(status_code=404, detail="user not found")
#
# # delete users
# @app.delete("/users/{user_id}",response_class=JSONResponse)
# def delete_user(user_id:int, db:Session=Depends(get_db)):
#     try:
#         u=db.query(User).filter(User.id==user_id).first()
#         db.delete(u)
#         db.commit()
#         return {f"user of id {user_id} has been deleted":True}
#     except:
#         HTTPException(status_code=404, detail="user not found")

#Web Socket Server & Real time communication by using fast api
# template use for decorate your front end
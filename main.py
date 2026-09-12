from fastapi  import FastAPI ,status ,HTTPException,Request,Depends,Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app=FastAPI()


# class Address(BaseModel):
#     city:str
#     pincode:int

# class User(BaseModel):
#     user:str
#     age:int
#     email:str
#     address:Address

# #User_Route
# #
# # @app.get("/user/{user_id}")
# # def get_user(user_id: int):
# #     return {"message": f"User with ID {user_id} is Kunal, Raj, or Shivam."}


# @app.get("/users")
# def get_users(name: str=None):
#     return {"Name":name}

# @app.get("/products")
# def get_product(Limit:int=10):
#     return {"Limit":Limit}


# # handling Multiple Query params 
# @app.get("/getuser")
# def get_users(name:str=None,id=int):
#     return{
#         "name":name,
#         "id":id
#     }



# # data Validation 
# @app.post("/create_user")
# def create_user(user:User):
#     return {
#         "message":"User Created",
#         "User":user
#             }


#-------------------------------------------------------------------------
#using path and query params together 

# users=[]

# class User(BaseModel):
#     name:str
#     id:int

# @app.post("/users") 
# def create_user(user:User):
#     users.append(user)
#     return{
#         "message":"User Created",
#         "data":user
#     }

# @app.put("/update/{user_id}")
# def updated_user(user_id:int,user:User,notify:bool= False):
#     if user_id<len(users):
#         users[user_id]=user
#         return{
#             "message":"User Updated",
#             "notify":notify,
#             "data":user
#         }


#     return {"Error": "User not found"}


#--------------------------------------------------------------------------
#TODO Response Model

# class User(BaseModel):
#     age:int
#     name:str
#     password:str


# class UserResponce(BaseModel):
#     age:int
#     name:str

# @app.get("/users",response_model=UserResponce)
# def get_user():
#     return {
#         "name":"Kunal",
#         "age":20,
#         "password":"123456" 
#     }

#-------------------------------Exception_----------------------------------
# @app.post("/create_user",status_code=status.HTTP_201_CREATED)
# def ceate_user():
#     return {
#         "message" :"User Created"
#     }


# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     if user_id!=1:
#         raise HTTPException(
#             status_code=404,
#             detail="user Not found" 
#         )



# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     if user_id!=1:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )
    
#     return{
#         "id":1,
#         "name":"Kunal"

#     }


#=================================================Exception Handling========================================================

# class UserNotFoundException(Exception):
#     def __init__(self,name:str):
#         self.name=name

# #Global Exception Handler
# #-----------------------------------------------------------------------------------
# @app.exception_handler(UserNotFoundException)
# def user_not_found_exception_handler(request:Request,exc:UserNotFoundException):
#     return JSONResponse(
#         status_code=404,
#         content={"message":f"User with name {exc.name} not found"}
#     )

# #--------------------------------------------------------------------------------------------

# @app.get("/users/{name}")
# def get_user(name:str):
#     if name != "Kunal":
#         raise UserNotFoundException(name)      
#     return{
#         "user":name
#     }  
#------------------------------------------------------------------------------


# Code reusable
# def common_logic():
#     return {
#         "message":"This is common logic"
#             }

# @app.get("/home")
# def home(data = Depends(common_logic)):
#     return data  
#--------------------------Authorization using dependance Injection------------------------
# def varify_token(token:str=Header(None)):
#     if token!= "Kunal":
#         raise HTTPException(
#             status_code=401,
#             detail="Unathorized"
#         )
#     return{
#         "user":"Authorized User"
#     }

# @app.get("/secure")
# def secure_data(user=Depends(varify_token)):
#     return{
#         "message":"Authorized"
#     }


# # TODO Middle Ware--------------------------------------------------------------------

# from fastapi import FastAPI,Request

# app=FastAPI()
#----------------------------------------------------------------------
# @app.middleware("http")
# async def my_middleware(request:Request,call_next):
#     print("Request Recivied")

#     responce=await call_next(request)

#     print("Responce sent")

#     return responce

#-----------------------------------------------------------------

# import time

# @app.middleware("http")
# async def log_middleware(request:Request,call_next):
#     start_time=time.time()

#     responce = await call_next(request)

#     process_time= time.time()- start_time

#     print(f"Path:{request.url.path} | Time : {process_time}")

#     return responce




#---------------------------Sq-lite Database Connection---------------------------------------------------
# import sqlite3

# conn=sqlite3.connect("mydatabase.db",check_same_thread=False) # connects to the database and creates a new database if it doesn't exist

# cursor=conn.cursor()  # runs sql commands and queries on the database

# #Runs Quary
# cursor.execute('''CREATE TABLE IF NOT EXISTS todos(id integer PRIMARY KEY AUTOINCREMENT, 
#                 title TEXT, description TEXT)''')

# #commits the  query in the database
# conn.commit()

# @app.get("/")
# def home():
#     return {"message":"Welcome to the FastAPI SQLite Example"}



#---------------------------------------------------------------------------------------------------
#------------------------------------------Sql Alchemy----------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

Database_URL="sqlite:///./mydatabase.db"
engine = create_engine(Database_URL
                       ,connect_args={"check_same_thread":False})


SessionLocal = sessionmaker(bind=engine)
Base = declarative_base() #Base for creating the models


#-----------------Model---------------------------------------------
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)


Base.metadata.create_all(bind=engine)  # creates the table in the database if it doesn't exist


#---------------------For accessing the database session in the routes--------------------------------

# by this function we can access the database session in the routes and close it after the request is completed
def  get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#----------------------------------------CURD OPeration using SQLAlchemy---------------------------------------------------

#---------------------------------------POst OPeration-------------------
@app.post("/todos")
def create_todo(title:str,db:Session=Depends(get_db)):
    todo=Todo(title=title,description="False")
    db.add(todo) # added data to db
    db.commit() # add Confirmed
    db.refresh(todo) # Data base refreshed  
    return{
        "message":"Todo Created",
        "data":todo
    }

#--------------------------------------Read Data------------------------------------------
#Read all data

@app.get("/get_todos")
def get_todos(db:Session=Depends(get_db)):
    todos=db.query(Todo).all() # all data included 

    return{
        "Total":len(todos),
        "data":todos
    }

#read Specific data
@app.get("/Specific_data/{todos_id}")
def get_specific_todo(todos_id:int,db:Session=Depends(get_db)):

    #
    todo=db.query(Todo).filter(Todo.id == todos_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return{
        "id":todo.id,
        "data":todo
    }


#---------------------------------------Updated Data-------------------------------
#Updata data
@app.put("/todos/{todo_id}")
def updaed_todo(todo_id:int,title:str,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    todo.title=title
    db.commit()
    db.refresh(todo)

    return{
        "Message":"Sucessfully Updatd",
        "data":todo
    }
#---------------------------------------Delete---------------------------------
@app.delete("/todos_delete/{todo_id}")
def delete_todos(todo_id:int,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return{
        "message":"Todo Deleted Successfully",
        "id":todo_id
    }

#--------------------------------------------------------------------------------




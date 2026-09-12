from fastapi import FastAPI
from pydantic import BaseModel


app=FastAPI()

todos=[]


class Todo(BaseModel):
    id:int
    title:str
    completed:bool

@app.post("/todos")
def create_todo(todo:Todo):
    todos.append(todo)
    return {"Message":"Todo Added","data":todo}


@app.get("/get_todos/{todo_id}")
def get_todos(todo_id:int):
    for todo in todos:
        if todo.id==todo_id:
            return {"Message" :"ID found ",
                    "Details":todo}
        
    return {"error" : "nohing Found"}

@app.put("/update/{todo_id}")
def update_user(todo_id:int,updated_todo:Todo):
    for index, todo in enumerate(todos):
        if todo.id== todo_id:
            todos[index]=updated_todo
            return {
                "Message":"Data updated "
            }

    return {"error": "nothing found"}


@app.delete("/delete/{todo_id}")
def delete_todo(todo_id:int):
    for index,todo in enumerate(todos):
        if todo.id==todo_id:
            todos.pop(index)
            return {"Data":"data removed Sucessfully"}

    return "Error"

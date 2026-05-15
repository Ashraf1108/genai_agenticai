from fastapi import FastAPI

from pydantic import BaseModel



#creating object to fastapi

app=FastAPI()

#defining schema 
class Employee(BaseModel):
    emp_id:int
    emp_name:str
    dept_name:str
    exp:int
    email:str
    is_active:bool

#Dummy databse 

Employees=[{
    "emp_id":111,
    "emp_name":"emp1",
    "dept_name":"CSE",
    "exp":1,
    "email":"emp1@gmail.com",
    "is_active":True
    }]
#GET
#http://127.0.0.1:8000/docs
@app.get("/")
def home():
    return{"message":"welcome to fastapi"}

@app.get("/employees")
def get_all_employees():
    return{
        "total_employees":len(Employees),
        "data":Employees
    }
#req param 

@app.get("/employee/{emp_id}")
def get_employee(emp_id:int):
    for emp in Employees:
        if emp["emp_id"]==emp_id:
            return emp
        return{"message":"Employee not found"}
    
#POST

@app.post("/add-employee")
def add_employee(employee:Employee):
    Employees.append(employee.dict())
    return{"message":"Employee added succcesfully"}

#PUT
@app.put("/update-employee/{emp_id}")
def update_employee(emp_id:int,updated_employee:Employee):
    for index,emp in enumerate(Employees):
        if emp["emp_id"]==emp_id:
            Employees[index]==update_employee.dict()
            return{"message":"Employee updated succesfully","updated_data":update_employee}
        return{"message":"employee not found"}
    
#DELETE

@app.delete("/delete-employee/{emp_id}")
def delete_employee(emp_id: int):
    for emp in Employees:
        if emp["emp_id"]==emp_id:
            Employees.remove(emp)
            return{"message":"Employee removed successfully"}
        return{"message":"Employee not found"}
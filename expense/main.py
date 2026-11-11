
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



class Expense(BaseModel):
    id: int
    description: str
    amount: float = Field(gt=0)
    category: str



expenses = {}




@app.post("/expenses")
def add_expense(expense: Expense):

    if expense.id in expenses:
        raise HTTPException(
            status_code=409,
            detail="Expense ID already exists"
        )

    if not expense.description.strip():
        raise HTTPException(
            status_code=400,
            detail="Description cannot be empty"
        )

    expenses[expense.id] = {
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category
    }

    return {
        "message": "Expense added successfully",
        "expense": {"id": expense.id, **expenses[expense.id]}
    }




@app.get("/expenses")
def get_expenses():
    return expenses




@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):

    if expense_id not in expenses:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "id": expense_id,
        **expenses[expense_id]
    }




@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: Expense):

    if expense_id not in expenses:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )


    if not expense.description.strip():
        raise HTTPException(
            status_code=400,
            detail="Description cannot be empty"
        )

    expenses[expense.id] = {
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category
    }

    return {
        "message": "Expense updated successfully",
        "expense": {"id": expense.id, **expenses[expense.id]}
    }


# DELETE EXPENSE - DELETE

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    if expense_id not in expenses:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    removed = expenses.pop(expense_id)

    return {
        "message": "Expense deleted successfully",
        "deleted": {"id": expense_id, **removed}
    }

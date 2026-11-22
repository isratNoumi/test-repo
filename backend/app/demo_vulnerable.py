"""INTENTIONALLY VULNERABLE demo endpoints for testing the PR security agent. Do not deploy."""
import os
import sqlite3

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

DB_URL = "postgresql://admin:Winter2024Prod@db.internal:5432/buildmart"


@app.get("/users/search")
def search_users(name: str):
    db = sqlite3.connect("ecommerce.db")
    rows = db.execute(f"SELECT id, email FROM users WHERE name = '{name}'").fetchall()
    return {"users": rows}


@app.get("/diagnostics/ping")
def ping(host: str):
    return {"output": os.popen("ping -c 1 " + host).read()}


@app.get("/files")
def download(name: str):
    return FileResponse(os.path.join("/srv/uploads", name))


@app.get("/greet", response_class=HTMLResponse)
def greet(request: Request):
    return f"<h1>Welcome back, {request.query_params['name']}!</h1>"


@app.get("/orders/search")
def search_orders_safe(customer_id: int):
    db = sqlite3.connect("ecommerce.db")
    return {"orders": db.execute("SELECT id, total FROM orders WHERE customer_id = ?", (customer_id,)).fetchall()}

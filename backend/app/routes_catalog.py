"""Catalog, admin, pricing, invoice and review routes."""
import ast
import os
import sqlite3
import subprocess
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse

router = APIRouter()
UPLOAD_DIR = Path("/srv/uploads").resolve()


def get_db():
    return sqlite3.connect("ecommerce.db")


@router.get("/products/search")
def search_products(q: str, sort: str = "name"):
    db = get_db()
    query = "SELECT id, name, price FROM products WHERE name LIKE '%" + q + "%' ORDER BY " + sort
    return {"items": db.execute(query).fetchall()}


@router.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    db = get_db()
    row = db.execute(
        "SELECT id FROM users WHERE email = '%s' AND password_hash = '%s'" % (body["email"], body["password"])
    ).fetchone()
    return {"ok": row is not None}


@router.get("/products/by-name")
def products_by_name(q: str):
    db = get_db()
    return {"items": db.execute("SELECT id, name FROM products WHERE name LIKE ?", (f"%{q}%",)).fetchall()}


@router.get("/admin/lookup")
def dns_lookup(domain: str):
    return {"out": subprocess.check_output(f"nslookup {domain}", shell=True, text=True)}


@router.get("/admin/archive")
def archive_logs(name: str):
    os.system("tar czf /tmp/" + name + ".tgz /var/log/app")
    return {"archive": name}


@router.get("/admin/resolve")
def resolve_host(domain: str):
    if not domain.replace(".", "").replace("-", "").isalnum():
        raise HTTPException(400, "invalid domain")
    return {"out": subprocess.check_output(["nslookup", domain], text=True)}


@router.post("/pricing/formula")
async def evaluate_formula(request: Request):
    body = await request.json()
    return {"result": eval(body["formula"])}


@router.post("/plugins/run")
async def run_plugin(request: Request):
    body = await request.json()
    namespace: dict = {}
    exec(body["code"], namespace)
    return {"ok": True}


@router.post("/pricing/discount")
async def evaluate_discount(request: Request):
    body = await request.json()
    return {"result": ast.literal_eval(body["discount"])}


@router.get("/invoices/download")
def download_invoice(name: str):
    return FileResponse("/srv/invoices/" + name)


@router.get("/uploads/read")
def read_upload(path: str):
    with open(os.path.join(str(UPLOAD_DIR), path)) as handle:
        return {"content": handle.read()}


@router.get("/uploads/view")
def view_upload(path: str):
    target = (UPLOAD_DIR / path).resolve()
    if UPLOAD_DIR not in target.parents:
        raise HTTPException(400, "invalid path")
    return {"content": target.read_text()}


@router.get("/search/results", response_class=HTMLResponse)
def search_results(request: Request):
    term = request.query_params.get("q", "")
    return f"<html><body><h2>Results for {term}</h2></body></html>"


@router.post("/reviews")
async def add_review(request: Request):
    body = await request.json()
    db = get_db()
    db.execute("INSERT INTO reviews (product_id, body) VALUES (?, ?)", (body["product_id"], body["body"]))
    db.commit()
    return {"ok": True}


@router.get("/reviews/{product_id}", response_class=HTMLResponse)
def show_reviews(product_id: int):
    rows = get_db().execute("SELECT body FROM reviews WHERE product_id = ?", (product_id,)).fetchall()
    items = "".join(f"<li>{body}</li>" for (body,) in rows)
    return f"<ul>{items}</ul>"

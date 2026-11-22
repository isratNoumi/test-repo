import html
import os
import re
import sqlite3
import subprocess
import tarfile
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Template

router = APIRouter()
templates = Jinja2Templates(directory="backend/app/templates")

AVATAR_DIR = Path("/srv/avatars").resolve()
IMPORT_DIR = Path("/srv/imports").resolve()
REPORT_NAMES = {"daily", "weekly", "monthly"}
DB_NAME = re.compile(r"[a-z_]{1,30}")


def get_db():
    return sqlite3.connect("ecommerce.db")


@router.get("/profile/{user_id}", response_class=HTMLResponse)
def profile(request: Request, user_id: int):
    row = get_db().execute("SELECT name, bio, city FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        raise HTTPException(404)
    return templates.TemplateResponse(request, "profile.html", {"name": row[0], "bio": row[1], "location": row[2]})


@router.post("/profile/{user_id}/bio")
async def update_bio(user_id: int, request: Request):
    body = await request.json()
    db = get_db()
    db.execute("UPDATE users SET bio = ? WHERE id = ?", (body["bio"], user_id))
    db.commit()
    return {"ok": True}


@router.get("/greeting/preview", response_class=HTMLResponse)
def preview_greeting(request: Request):
    greeting = request.query_params.get("template", "Hello {{ name }}")
    return Template(greeting).render(name="Customer")


@router.get("/avatars/{name}")
def avatar(name: str):
    name = name.replace("../", "")
    return FileResponse(AVATAR_DIR / name)


@router.post("/imports/upload")
def import_archive(upload: UploadFile):
    with tarfile.open(fileobj=upload.file, mode="r:*") as archive:
        archive.extractall(IMPORT_DIR)
    return {"ok": True}


@router.get("/reports/run")
def run_report(name: str):
    if name not in REPORT_NAMES:
        raise HTTPException(400, "unknown report")
    return {"out": subprocess.run(["/usr/local/bin/build-report", name], capture_output=True, text=True).stdout}


@router.post("/admin/backup")
async def backup(request: Request):
    body = await request.json()
    database = body["database"]
    if not DB_NAME.fullmatch(database):
        raise HTTPException(400, "invalid database name")
    subprocess.run("pg_dump " + database + " > /tmp/backup.sql", shell=True, check=True)
    return {"ok": True}


@router.get("/orders/lookup")
def lookup_order(order_id: str):
    return {"order": get_db().execute(f"SELECT id, total FROM orders WHERE id = {order_id}").fetchone()}


@router.get("/orders/{order_id}")
def get_order(order_id: int):
    return {"order": get_db().execute(f"SELECT id, total FROM orders WHERE id = {order_id}").fetchone()}


@router.get("/notes/preview", response_class=HTMLResponse)
def preview_note(text: str):
    return f"<p>{html.escape(text)}</p>"


@router.get("/exports/{name}")
def export_file(name: str):
    target = (IMPORT_DIR / name).resolve()
    if not target.is_relative_to(IMPORT_DIR) or not os.path.isfile(target):
        raise HTTPException(404)
    return FileResponse(target)

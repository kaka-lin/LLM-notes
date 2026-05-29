"""URL Shortener — minimal SDD example.

每一段邏輯都對應到 ../spec/url_shortener.md 中的需求編號, 方便正反向追溯.
"""

import secrets
import sqlite3
import string
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

# Constants
SHORT_CODE_LENGTH = 6  # REQ-002
SHORT_CODE_ALPHABET = string.ascii_letters + string.digits  # REQ-002
MAX_URL_LENGTH = 2048  # CON-001
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = str(DATA_DIR / "shortener.db")


# Models
class ShortenRequest(BaseModel):
    url: str


class ShortenResponse(BaseModel):
    short_code: str


# DAT-001
SCHEMA = """
CREATE TABLE IF NOT EXISTS mappings (
    short_code   TEXT PRIMARY KEY,
    original_url TEXT NOT NULL UNIQUE,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


@contextmanager
def get_conn(db_path: str = DB_PATH) -> Generator[sqlite3.Connection, None, None]:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


# Helpers
def is_valid_url(url: str) -> bool:
    """CON-002: 必須具備 scheme 與 host."""
    parsed = urlparse(url)
    return bool(parsed.scheme in {"http", "https"} and parsed.netloc)


def generate_code() -> str:
    """REQ-002: 6 個字元, [a-zA-Z0-9]."""
    return "".join(secrets.choice(SHORT_CODE_ALPHABET) for _ in range(SHORT_CODE_LENGTH))


# App
app = FastAPI()


def db_conn() -> Generator[sqlite3.Connection, None, None]:
    with get_conn() as conn:
        yield conn


@app.post("/shorten", response_model=ShortenResponse)
def shorten(req: ShortenRequest, conn: sqlite3.Connection = Depends(db_conn)) -> ShortenResponse:
    """REQ-001 / REQ-002 / REQ-003 / CON-001 / CON-002."""
    if len(req.url) > MAX_URL_LENGTH:  # CON-001
        raise HTTPException(status_code=400, detail="URL too long")
    if not is_valid_url(req.url):  # CON-002
        raise HTTPException(status_code=400, detail="Invalid URL")

    # REQ-003: 冪等 — 同一 URL 回相同 code
    row = conn.execute(
        "SELECT short_code FROM mappings WHERE original_url = ?", (req.url,)
    ).fetchone()
    if row:
        return ShortenResponse(short_code=row[0])

    # REQ-002: 產生新 code, 重試避免碰撞
    for _ in range(5):
        code = generate_code()
        try:
            conn.execute(
                "INSERT INTO mappings (short_code, original_url) VALUES (?, ?)",
                (code, req.url),
            )
            return ShortenResponse(short_code=code)
        except sqlite3.IntegrityError:
            continue
    raise HTTPException(status_code=500, detail="Could not allocate short code")


@app.get("/{short_code}")
def resolve(short_code: str, conn: sqlite3.Connection = Depends(db_conn)) -> RedirectResponse:
    """REQ-004: 存在則 302, 否則 404."""
    row = conn.execute(
        "SELECT original_url FROM mappings WHERE short_code = ?", (short_code,)
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return RedirectResponse(url=row[0], status_code=302)

import os
import json
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

# Data directory for storing chat sessions
DATA_DIR = Path(os.getenv("CHAT_DATA_DIR", "./.chat_sessions")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Data models
Message = Dict[str, str]


@dataclass
class SessionState:
    session_id: str
    created_at: float
    updated_at: float
    summary: str
    messages: List[Message]  # does NOT include summary as a message


# Persistence
def session_path(session_id: str, data_dir: Path = DATA_DIR) -> Path:
    return data_dir / f"{session_id}.json"


def save_session(state: SessionState, data_dir: Path = DATA_DIR) -> None:
    state.updated_at = time.time()
    session_path(state.session_id, data_dir).write_text(
        json.dumps(asdict(state), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_session(session_id: str, data_dir: Path = DATA_DIR) -> Optional[SessionState]:
    p = session_path(session_id, data_dir)
    if not p.exists():
        return None
    obj = json.loads(p.read_text(encoding="utf-8"))
    return SessionState(
        session_id=obj["session_id"],
        created_at=obj["created_at"],
        updated_at=obj["updated_at"],
        summary=obj.get("summary", ""),
        messages=obj.get("messages", []),
    )


def list_sessions(data_dir: Path = DATA_DIR) -> List[str]:
    return sorted([p.stem for p in data_dir.glob("*.json")])


def new_session() -> SessionState:
    sid = uuid.uuid4().hex[:12]
    now = time.time()
    return SessionState(
        session_id=sid,
        created_at=now,
        updated_at=now,
        summary="",
        messages=[],
    )

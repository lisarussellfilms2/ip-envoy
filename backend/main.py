from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import json
import os
import uuid

app = FastAPI()

DATA_FILE = "ip_records.jsonl"  # JSON Lines file (one record per line)


class IPRecordIn(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    notes: str = Field(..., min_length=1, max_length=20000)
    people: Optional[List[str]] = None
    tags: Optional[List[str]] = None


@app.get("/")
def root():
    return {"message": "IP Envoy is running", "status": "ok"}


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/record")
def record_ip(payload: IPRecordIn):
    # Create a tamper-evident-ish record structure (we’ll add hashing next)
    record = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "title": payload.title,
        "notes": payload.notes,
        "people": payload.people or [],
        "tags": payload.tags or [],
    }

    try:
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store record: {e}")

    return {"ok": True, "record": record}

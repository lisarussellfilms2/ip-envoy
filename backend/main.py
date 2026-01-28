cd ~/ip-envoy
cat > backend/main.py << 'EOF'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import json
import uuid
import hashlib

app = FastAPI()

DATA_FILE = "ip_records.jsonl"


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


def compute_record_hash(record: dict) -> str:
<<<<<<< HEAD
    canonical = json.dumps(
        record,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
=======

>>>>>>> bdb21a9 (:wq)


@app.post("/record")
def record_ip(payload: IPRecordIn):
    record = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "title": payload.title,
        "notes": payload.notes,
        "people": payload.people or [],
        "tags": payload.tags or [],
    }

    record_hash = compute_record_hash(record)
    record_with_hash = {**record, "record_hash": record_hash}

    try:
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record_with_hash, ensure_ascii=False) + "\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"ok": True, "record": record_with_hash}
EOF

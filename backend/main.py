from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "IP Envoy is running",
        "status": "ok"
    }

@app.get("/health")
def health():
    return {"ok": True}

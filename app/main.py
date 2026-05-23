from fastapi import FastAPI

app = FastAPI(title="SIGECORE API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "SIGECORE API"}

@app.get("/health")
def health():
    return {"status": "ok"}
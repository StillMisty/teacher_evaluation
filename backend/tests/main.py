from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.get("/api/teacher")
def _():
    return {"msg": "这是教师相关的接口"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host="localhost", port=8081, reload=True)
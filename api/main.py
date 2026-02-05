from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append('/data/data/com.termux/files/home/cit')
from core.matrix import CiMatrix

app = FastAPI()
matrix = CiMatrix()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/api/v1/state")
async def get_state():
    return matrix.state

@app.get("/api/v1/layer/{layer_id}")
async def get_layer(layer_id: str):
    return {"content": matrix.get_layer_data(layer_id)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

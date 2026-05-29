from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

PLANET_API_KEY = os.environ.get("PLANET_API_KEY", "")

@app.get("/tile/{mosaic}/{z}/{x}/{y}")
async def get_tile(mosaic: str, z: int, x: int, y: int):
    if not PLANET_API_KEY:
        return Response(content="API key not configured", status_code=500)
    url = f"https://tiles.planet.com/basemaps/v1/planet-tiles/{mosaic}/gmap/{z}/{x}/{y}.png?api_key={PLANET_API_KEY}"
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(url)
        return Response(content=res.content, media_type="image/png", status_code=res.status_code)

@app.get("/health")
def health():
    return {"status": "ok", "key_configured": bool(PLANET_API_KEY)}

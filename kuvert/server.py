import kuvert
from datetime import date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

class Kuvert(BaseModel):
    title: str
    content: str
    opening_date: date
    tag: Optional[str] = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/kuvert/open")
async def list_open_kuvert():
    res = kuvert.get_open()
    if res.success:
        return {"success": True, "kuvert": res.kuvert}
    else:
        return {"success": False, "error": res.error}

@app.get("/kuvert/{id}")
async def kuvert_get(id: int):
    res = kuvert.get_kuvert(id)
    if res.success:
        return {"kuvert": res.content}
    else:
        response.status = res.error
        return {"error": res.content}


@app.post("/kuvert")
async def kuvert_save(kuvert_input: Kuvert):
    res = kuvert.make_kuvert(
        kuvert_input.title, kuvert_input.content, kuvert_input.opening_date, kuvert_input.tag
    )

    if res.success:
        return {"success": True, "id": res.id}
    else:
        return {"success": False, "error": res.error}



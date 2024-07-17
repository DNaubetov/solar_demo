from typing import List, Dict

import uvicorn
from fastapi import FastAPI

from models import Inverter, InverterDataOutput
import demo_db
import ip
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/inverter')
async def inv_get() -> List[Inverter]:
    return [Inverter(**i) for i in demo_db.date_inv]


@app.post('/inverter')
async def inv_add(body: Inverter) -> bool:
    old_len = len(demo_db.date_inv)
    demo_db.date_inv.append(body.model_dump())
    return True if len(demo_db.date_inv) > old_len else False


@app.post('/date')
async def date_post(body: InverterDataOutput) -> bool:
    old_len = len(demo_db.date_inv_out)
    demo_db.date_inv_out.append(body.model_dump())
    return True if len(demo_db.date_inv_out) > old_len else False


@app.get('/date')
async def date_get() -> List[InverterDataOutput]:
    return [InverterDataOutput(**i) for i in demo_db.date_inv_out]


if __name__ == '__main__':
    uvicorn.run("main:app", host=ip.get_local_ip(), port=8080, reload=True)

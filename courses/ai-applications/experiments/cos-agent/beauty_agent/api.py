from dataclasses import asdict

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .agent import run_turn
from .catalog import CATALOG
from .contracts import TurnRequest, TurnResponse

app = FastAPI(title="BeautyLIFE Agent — synthetic prototype", version="0.1.0")


@app.exception_handler(RequestValidationError)
async def invalid_request(request: Request, exc: RequestValidationError):
    # Pydantic's default error includes raw input. Never echo it here.
    return JSONResponse(status_code=422, content={"error": {"code": "invalid_input", "message": "합성 입력과 API 스키마를 확인해 주세요."}})


@app.get("/health")
def health():
    return {"status": "ok", "mode": "synthetic_only", "persistence": "none"}


@app.get("/v1/demo/catalog")
def catalog():
    return {"synthetic_only": True, "products": [asdict(p) for p in CATALOG.values()]}


@app.post("/v1/agent/turn", response_model=TurnResponse)
async def turn(payload: TurnRequest):
    return await run_turn(payload)

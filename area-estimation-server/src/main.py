from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request

from domain.error.domain_error import DomainError
from infrastructure.error.infrastructure_error import InfrastructureError
from presentation.handler.get_spot_by_area_handler import \
    router as get_spot_by_spot_id_collection

app = FastAPI()

app.include_router(get_spot_by_spot_id_collection)


@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message},
    )


@app.exception_handler(InfrastructureError)
async def infrastructure_exception_handler(request: Request, exc: InfrastructureError):
    return JSONResponse(
        status_code=404,
        content={"error": exc.message},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")

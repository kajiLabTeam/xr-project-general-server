from domain.error.domain_error import DomainError
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from infrastructure.error.infrastructure_error import InfrastructureError
from presentation.handlers.create_sopt_hadler import \
    router as create_spot_router
from presentation.handlers.get_spot_by_spot_id_collection_handler import \
    router as get_spot_by_spot_id_collection_router
from starlette.requests import Request

app = FastAPI()


app.include_router(get_spot_by_spot_id_collection_router)
app.include_router(create_spot_router)


@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message},
    )


@app.exception_handler(InfrastructureError)
async def infrastructure_exception_handler(request: Request, exc: InfrastructureError):
    return JSONResponse(
        status_code=500,
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

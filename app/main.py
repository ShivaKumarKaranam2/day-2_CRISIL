from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routes import router as tasks_router

app = FastAPI(
    title="Task Management REST API",
    description="A simple in-memory Task Management API built with FastAPI",
    version="1.0.0",
)

app.include_router(tasks_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    # Surface invalid input (e.g. missing/blank title) as 400 instead of the default 422
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

# Write get_tasks_by_priority() to return a list of tasks filtered by priority. The endpoint should be GET /tasks/priority/{priority} and return a 200 status code with the list of tasks in the response body. If no tasks match the given priority, return an empty list.
@

@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

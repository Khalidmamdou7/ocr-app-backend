from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": "Internal server error" if exc.status_code == 500 else "Bad request",
            "message": exc.detail,
            "errors": [
                {
                    "message": exc.detail,
                }
            ]
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # print("Req: ", request.__dict__)
    print(f"exc: {exc}")
    # Extract error details from the exception
    error_messages = []
    for error in exc.errors():
        loc = error["loc"][1]
        msg = error["msg"]
        error_messages.append({"location": loc, "message": msg})

    # Return a structured JSON response with the validation errors
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "detail": "Validation error",
            "errors": error_messages,
        },
    )

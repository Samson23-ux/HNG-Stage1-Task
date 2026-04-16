from fastapi import Request
from fastapi.responses import JSONResponse


from app.main import app
from app.core.exceptions import (
    ServerError,
    AppException,
    ResponseError,
    InvalidNameError,
    CheckTimeoutError,
    ProfileNotFoundError,
    ProfilesNotFoundError,
    create_exception_handler
)


@app.exception_handler(ServerError)
async def server_error(request: Request, exc: AppException):
    return JSONResponse(
        content={"status": "error", "message": "Oops! Something went wrong!"},
        status_code=500,
    )


app.add_exception_handler(
    InvalidNameError,
    create_exception_handler(
        initial_detail={
            "status": "error",
            "message": "{name} parameter not a string",
        },
        status_code=422,
    ),
)


app.add_exception_handler(
    ProfileNotFoundError,
    create_exception_handler(
        initial_detail={
            "status": "error",
            "message": "Profile not found with id {profile_id}",
        },
        status_code=404,
    ),
)


app.add_exception_handler(
    ProfilesNotFoundError,
    create_exception_handler(
        initial_detail={
            "status": "error",
            "message": "No profiles found at the moment! Check back later",
        },
        status_code=404,
    ),
)


app.add_exception_handler(
    ResponseError,
    create_exception_handler(
        initial_detail={
            "status": "error",
            "message": "{external_api} returned an invalid response",
        },
        status_code=502,
    ),
)


app.add_exception_handler(
    CheckTimeoutError,
    create_exception_handler(
        initial_detail={
            "status": "error",
            "message": "Ensure the device is connected to the internet",
        },
        status_code=408,
    ),
)

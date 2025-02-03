import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.config import LOG_FILE
from app.core.logger import get_logger


logger = get_logger("app.middleware", log_file=LOG_FILE)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        client = request.client.host  # type: ignore
        logger.info(
            f"Request: method={request.method}, path={request.url.path}, "
            f"client={client}"
        )

        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        logger.info(
            f"Response: status_code={response.status_code}, client={client}, "
            f"time_taken={process_time}"
        )
        return response

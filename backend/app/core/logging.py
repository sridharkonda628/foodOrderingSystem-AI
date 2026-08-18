import logging
import sys
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("kpitech_food_order")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        request_id = request.headers.get("X-Request-ID", "-")
        
        response: Response = await call_next(request)
        
        process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        response.headers["X-Process-Time-Ms"] = str(process_time_ms)
        
        if not request.url.path.startswith("/static"):
            logger.info(
                f"HTTP {request.method} {request.url.path} "
                f"-> Status: {response.status_code} [{process_time_ms}ms] ReqID: {request_id}"
            )
            
        return response

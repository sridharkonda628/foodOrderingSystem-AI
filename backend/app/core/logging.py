"""
Structured Request Logging and Latency Middleware.

Use Case:
- Configures centralized application logging.
- Measures and records request processing latency in milliseconds, attaching the
  `X-Process-Time-Ms` response header for API observability and performance profiling.
"""

import logging
import sys
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Configure standardized root logger formatting
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("kpitech_food_order")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    HTTP Middleware for timing and logging all incoming requests and outgoing responses.

    Use Case:
    - Provides real-time visibility into incoming endpoint hits, status codes, and execution durations.
    - Adds the 'X-Process-Time-Ms' header to all HTTP responses.
    """
    async def dispatch(self, request: Request, call_next):
        """
        Intercepts incoming HTTP requests, records elapsed execution time, and logs summary.

        Parameters:
        - request: The incoming Starlette/FastAPI request.
        - call_next: Async callable to delegate request processing to next handler.

        Returns:
        - Response with attached latency header.
        """
        start_time = time.perf_counter()
        request_id = request.headers.get("X-Request-ID", "-")
        
        # Proceed with request handling
        response: Response = await call_next(request)
        
        # Calculate latency in milliseconds
        process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        response.headers["X-Process-Time-Ms"] = str(process_time_ms)
        
        # Skip verbose static asset logs
        if not request.url.path.startswith("/static"):
            logger.info(
                f"HTTP {request.method} {request.url.path} "
                f"-> Status: {response.status_code} [{process_time_ms}ms] ReqID: {request_id}"
            )
            
        return response

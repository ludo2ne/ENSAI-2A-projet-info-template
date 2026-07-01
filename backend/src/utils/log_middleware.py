# backend/src/utils/log_middleware.py

import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware to log HTTP requests and responses.
        It captures the method, path, status code, and error details.
        """

        method = request.method
        path = str(request.url.path)

        logging.info(f"{method} {path} - START")

        try:
            response = await call_next(request)
            logging.info(f"{method} {path} - END [Status: {response.status_code}]")
            return response

        except Exception as e:
            logging.error(f"{method} {path} - FAILED [Status: 500] Error: {str(e)}")
            raise e

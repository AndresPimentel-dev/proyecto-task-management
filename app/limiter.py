import os

# app/core/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

is_testing = os.getenv("TESTING", "false").lower == "true"
# Instancias el limitador una sola vez para toda la app
limiter = Limiter(key_func=get_remote_address, enabled=not is_testing)

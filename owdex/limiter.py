from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# TODO check if remote address is good enough as key
# TODO decide if headers should be enabled
limiter = Limiter(key_func=get_remote_address, headers_enabled=True)

import time
from functools import wraps

from fastapi import FastAPI,HTTPException, Request, status

# Instance the API
my_api = FastAPI()

# Declare the function to limit the requests.
def rate_limited(max_calls: int, time_frame: int):
    """
    Function that returns a decorator to limit the max number of requests in an specified time.
    --------------
        Parameters:
            max_calls: Maximum number of calls allowed in the specified time frame.
            time_frame: The time frame in seconds for which the limit applies.
        Return:
            Decorator funcion.
    """
    def decorator(func):
        # Instance a list to store the current calls
        calls = []

        # Function to control the limit of requests.
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            current_time = time.time()
            # Check for calls made given a time.
            calls_in_the_frame = [call for call in calls if call > current_time - time_frame]
            # Raise the exception if the calls exceed the max_calls
            if len(calls_in_the_frame) >= max_calls:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate Limit exceeded. Too Many Requests")
            calls.append(current_time)
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator


# Set the api behavior.
@my_api.get("/")
@rate_limited(max_calls=8, time_frame=1)
async def read_root(request: Request):
    return {"Hello": "World"}

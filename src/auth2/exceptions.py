# from fastapi import HTTPException
# from starlette import status
#
# credentials_exception = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
# )
#
# auth_exp = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Invalid username or password",
# )
# from fastapi import APIRouter, Request, Depends, HTTPException
# from fastapi.responses import RedirectResponse
# from authlib.integrations.starlette_client import OAuth
# from src.config import settings
#
# router = APIRouter(prefix="/github", tags=["github"])
#
# oauth = OAuth()
# oauth.register(
#     name='github',
#     client_id=settings.GITHUB_OAUTH_CLIENT_ID,
#     client_secret=settings.GITHUB_OAUTH_CLIENT_SECRET,
#     access_token_url='https://github.com/login/oauth/access_token',
#     authorize_url='https://github.com/login/oauth/authorize',
#     api_base_url='https://api.github.com/',
#     client_kwargs={'scope': 'user:email'},
# )
#
#
# @router.get('/authorize')
# async def github_authorize(request: Request):
#     redirect_uri = settings.GITHUB_OAUTH_REDIRECT_URI
#     return await oauth.github.authorize_redirect(request, redirect_uri)
#
#
# @router.get('callback')
# async def github_callback(request: Request):
#     try:
#         token = await oauth.github.authorize_access_token(request)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#     # Получаем информацию о пользователе
#     resp = await oauth.github.get('user', token=token)
#     user_info = resp.json()
#
#     print(f"user_info: {user_info}")
#
#     # Здесь должна быть ваша логика создания/авторизации пользователя
#     # Например:
#     # user = await get_or_create_user_from_github(user_info)
#     # create_session_for_user(user)
#
#     return RedirectResponse(url='/')
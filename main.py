from starlette import status
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

import uvicorn

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete

from typing import Annotated
import datetime
import bcrypt

from backend.db_depends import get_db
from models import *

salt = bcrypt.gensalt()

app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

#-----------------------------------------------------------------------------------------------------------------------

@app.get("/")
async def login_get(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('login.html',  {'request': request,
                                                      'title': 'Авторизация',
                                                      'title_command': 'Войдите в ваш профиль!',
                                                      'href': '#',})

@app.post("/")
def login_post(request: Request, db: Annotated[Session, Depends(get_db)],
                                                                             username = Form(),
                                                                             password=Form()):
    user = db.scalar(select(Users).where(Users.username == username))
    info = {}
    if user is not None:
        password = str(password).encode('utf-8')
        if bcrypt.checkpw(password ,user.password):
            request.session["username"] = user.username
            request.session["user_id"] = user.id
            return RedirectResponse(url="/main_page", status_code=status.HTTP_302_FOUND)
    info.update({'error': 'Неверный логин или пароль!'})
    return templates.TemplateResponse('login.html', {'request': request,
                                                     'title': 'Авторизация',
                                                     'info': info,
                                                     'href': '/', })

#-----------------------------------------------------------------------------------------------------------------------

@app.get("/registration")
async def registration_get(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('registration.html',  {'request': request,
                                                             'title': 'Регистрация',
                                                             'title_command': 'Заполните форму!',
                                                             'href': '/',})

@app.post("/registration")
async def registration_post(request: Request, db: Annotated[Session, Depends(get_db)], username = Form(),
                                                                                       password=Form(),
                                                                                       repeat_password=Form()):

    info = {}
    if username=='' or password=='' or repeat_password=='':
        info.update({'error': 'Заполните все поля!'})
        return templates.TemplateResponse('registration.html', {'request': request,
                                                                'title': 'Регистрация',
                                                                'info': info,
                                                                'href': '/', })
    user = db.scalar(select(Users).where(Users.username == username))

    # Пользователь новый
    if user is None:

        # Пароли совпадают
        if password==repeat_password:
            password = bcrypt.hashpw(password.encode('utf-8'), salt)
            db.execute(insert(Users).values(username=username, password=password))
            db.commit()
            return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

        # Пароли НЕ совпадают
        info.update({'error': 'Пароли не совпадают'})
        return templates.TemplateResponse('registration.html', {'request': request,
                                                                'title': 'Регистрация',
                                                                'info': info,
                                                                'href': '/', })
    # Пользователь НЕ новый
    info.update({'error': f'Логин {username} занят!'})
    return templates.TemplateResponse('registration.html',  {'request': request,
                                                             'title': 'Регистрация',
                                                             'info': info,
                                                             'href': '/',})

#-----------------------------------------------------------------------------------------------------------------------

@app.get("/main_page")
async def main_page(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:

    user = request.session.get("username")

    post_list = []
    for i in db.scalars(select(Posts)).all():
        post_list.append(i)
    post_list.reverse()

    return templates.TemplateResponse('main_page.html',  {'request': request,
                                                          'title': 'Главная страница',
                                                          'user': user,
                                                          'href_main': '#',
                                                          'href_prof': '/your_profile',
                                                          'post_list': post_list,
                                                          })

#-----------------------------------------------------------------------------------------------------------------------

@app.get("/your_profile")
async def profile_get(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:

    user = request.session.get("username")
    user_id = request.session.get("user_id")

    post_list = []
    for i in db.scalars(select(Posts).where(Posts.user_id == user_id)):
        post_list.append(i)
    post_list.reverse()

    return templates.TemplateResponse('your_profile.html',  {'request': request,
                                                             'title': 'Ваш профиль',
                                                             'user': user,
                                                             'href_main': '/main_page',
                                                             'href_prof': '#',
                                                             'post_list': post_list,
                                                              })

@app.post("/your_profile")
async def profile_get(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:

    user = request.session.get("username")
    user_id = request.session.get("user_id")

    req = await request.body()
    post_id = req.decode().split('=')[1]

    db.execute(delete(Posts).where(Posts.id == post_id))
    db.commit()

    post_list = []
    for i in db.scalars(select(Posts).where(Posts.user_id == user_id)):
        post_list.append(i)
    post_list.reverse()

    return templates.TemplateResponse('your_profile.html',  {'request': request,
                                                             'title': 'Ваш профиль',
                                                             'user': user,
                                                             'href_main': '/main_page',
                                                             'href_prof': '#',
                                                             'post_list': post_list,
                                                              })

#-----------------------------------------------------------------------------------------------------------------------

@app.get("/create_post")
async def create_post(request: Request) -> HTMLResponse:

    return templates.TemplateResponse('create_post.html',  {'request': request,
                                                             'title': 'Создание поста',
                                                             'title_command': 'Заполните форму!',
                                                             'href': '/your_profile',})

@app.post("/create_post")
async def create_post(request: Request, db: Annotated[Session, Depends(get_db)], title = Form(),
                                                                                 description=Form(),):
    user_id = request.session.get("user_id")

    if title=='' or description=='':
        return templates.TemplateResponse('create_post.html', {'request': request,
                                                               'title': 'Создание поста',
                                                               'title_command': 'Заполните все поля!',
                                                               'href': '/your_profile', })
    db.execute(insert(Posts).values(title=title,
                                    description=description,
                                    date_of_creation=datetime.date.today(),
                                    user_id=user_id,
                                    ))
    db.commit()

    return RedirectResponse(url="/your_profile", status_code=status.HTTP_302_FOUND)

#-----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
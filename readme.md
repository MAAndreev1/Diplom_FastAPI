# Web-приложение для сайта постов на FastAPI

## Необходимые связи:

* alembic==1.13.3
* annotated-types==0.7.0
* anyio==4.6.2.post1
* bcrypt==4.2.0
* click==8.1.7
* colorama==0.4.6
* fastapi==0.115.4
* greenlet==3.1.1
* h11==0.14.0
* idna==3.10
* itsdangerous==2.2.0
* Jinja2==3.1.4
* Mako==1.3.6
* MarkupSafe==3.0.2
* pydantic==2.9.2
* pydantic_core==2.23.4
* python-multipart==0.0.17
* sniffio==1.3.1
* SQLAlchemy==2.0.36
* starlette==0.41.2
* typing_extensions==4.12.2
* uvicorn==0.32.0
  
![image](https://github.com/user-attachments/assets/c6a61b82-8953-4b1b-834f-c880d1101754)

## Возможности:

### 1. Идентификация:
   * Регистрация пользователя с хешированием пароля;
     
   ![image](https://github.com/user-attachments/assets/f88c6c64-e073-4d4d-857c-d3f5a827dbc5)

   * Однофакторная аутентификация пользователя;
  
   ![image](https://github.com/user-attachments/assets/cf01b59f-1cdf-4ea7-8e58-79e884601ba2)

   * Хранение пользовательской информации в базе данных.

   ![image](https://github.com/user-attachments/assets/78bd15b3-9577-4a24-b16a-e228ad8a7f67)

### 2. Посты:
   * Хранение постов в базе данных;
  
   ![image](https://github.com/user-attachments/assets/ef5b54c6-9b5e-4376-9d02-ec026f35832c)

   * Связь пользователя с постом (один к многим).
### 3. Стена:
   * Стена (страница с полем размещения всех постов);

   ![image](https://github.com/user-attachments/assets/58a57ef2-62f5-4ca1-8eb3-842f13287094)

### 4. Профиль пользователя:
   * Создание постов;

   ![image](https://github.com/user-attachments/assets/d9646bb9-2828-4824-83ab-0a5cf49bc04a)

   * Удаление постов;
   * Стена (страница с полем размещения своих постов).

   ![image](https://github.com/user-attachments/assets/70c8b3c3-b3b8-4c57-b287-cfe0b070d197)

## Шаблоны страниц:

* login.html - шаблон страницы авторизации;
* registration.html - шаблон страницы регистрации;
* main_page.html - шаблон главной страницы с постами;
* your_profile.html - шаблон страницы профиля;
* create_post.html - шаблон страницы создания постов.

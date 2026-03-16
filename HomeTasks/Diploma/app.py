from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form, Response, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import quote
from starlette.middleware.sessions import SessionMiddleware

from backend.DataBase import get_db
from backend.person import Record
from backend.utils import date_ukr, format_age, log_action, get_logs
from backend import services

templates = Jinja2Templates(directory="frontend")
templates.env.filters["date_ukr"] = date_ukr
templates.env.filters["format_age"] = format_age

db = get_db()
person = Record()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_action("SYSTEM -> Запуск сервера: Перевірка цілісності бази даних...")
    db.create_table()
    yield
    log_action("SYSTEM -> Зупинка сервера...")


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="diploma-secret-key")


@app.get("/", response_class=HTMLResponse)
def index(request: Request, search: str = None, search_target: str = 'both', show_all: bool = False,
          show_import: bool = False, show_user_id: int = None):
    log_action("GET / -> Відкриття головної сторінки")

    display_users, search_query, has_json = services.get_users_for_display(
        db, search, search_target, show_all, show_import, show_user_id
    )

    error = request.session.pop("error", None)
    if error:
        log_action(f"UI -> Виведення помилки на екран: {error}")

    query_params = []
    if search_query:
        query_params.append(f"search={quote(search_query)}")
        query_params.append(f"search_target={search_target}")
    if show_all: query_params.append("show_all=true")
    if show_import: query_params.append("show_import=true")
    current_qs = "&".join(query_params)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "users": display_users,
            "error": error,
            "search_query": search_query,
            "search_target": search_target,
            "show_all": show_all,
            "show_import": show_import,
            "has_json": has_json,
            "current_qs": current_qs,
            "logs": get_logs()
        }
    )


@app.post("/add")
def add_user(
        request: Request, first_name: str = Form(...), birth_date: str = Form(...),
        fathers_name: str = Form(""), last_name: str = Form(""), death_date: str = Form("")
):
    log_action(f"ACTION -> Спроба додати користувача (Ім'я: {first_name})")

    new_user_id, error_msg = services.process_new_user(
        person, db, first_name, birth_date, fathers_name, last_name, death_date
    )

    if error_msg:
        request.session["error"] = error_msg
        return RedirectResponse("/", status_code=303)

    if new_user_id:
        return RedirectResponse(f"/?show_user_id={new_user_id}", status_code=303)
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{user_id}")
def delete_user(user_id: int, request: Request):
    log_action(f"ACTION -> Видалення користувача з ID={user_id}")
    db.delete_user(user_id)
    log_action(f"DB -> Користувач ID={user_id} видалений")
    referer = request.headers.get("referer")
    return RedirectResponse(referer or "/", status_code=303)


@app.get("/delete_all")
def delete_all():
    log_action("WARNING -> Ініційовано повне очищення бази даних!")
    db.delete_all_users()
    log_action("DB -> База даних порожня")
    return RedirectResponse("/", status_code=303)


@app.get("/export")
def export_users_to_json(search: str = None, show_all: bool = False, show_import: bool = False):
    log_action(f"ACTION -> Експорт даних у JSON (search={search}, show_all={show_all})")

    json_str, count = services.generate_export_json(db, search, show_all)
    log_action(f"SUCCESS -> Експортовано {count} записів")

    return Response(
        content=json_str,
        media_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="users_export.json"'}
    )


@app.post("/upload_json")
async def upload_json(request: Request, file: UploadFile = File(...)):
    log_action(f"ACTION -> Завантаження файлу: {file.filename}")
    try:
        content = await file.read()
        success, msg = services.process_json_upload(content)

        if success:
            log_action(f"SUCCESS -> У буфер завантажено {msg} нових записів")
        else:
            request.session["error"] = msg
            log_action("ERROR -> Неправильний формат JSON (не список)")

    except Exception as e:
        request.session["error"] = "Помилка читання файлу."
        log_action(f"ERROR -> Помилка парсингу JSON: {str(e)}")

    return RedirectResponse("/?show_import=true", status_code=303)


@app.get("/add_from_json/{idx}")
def add_from_json(idx: int, request: Request):
    log_action(f"ACTION -> Перенесення запису з JSON (index={idx}) у БД")
    try:
        new_id = services.transfer_user_to_db(db, idx)
        if new_id:
            log_action(f"DB -> Запис успішно збережено з новим ID={new_id}")
    except IndexError:
        log_action("ERROR -> Спроба додати неіснуючий індекс із буфера")

    referer = request.headers.get("referer")
    return RedirectResponse(referer or "/?show_import=true", status_code=303)


@app.get("/clear_json")
def clear_json():
    log_action("ACTION -> Очищення буфера імпорту JSON")
    services.clear_json_buffer()
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn

    log_action("SYSTEM -> Запуск Uvicorn сервера на порту 8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
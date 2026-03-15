import json

from backend.DataBase import get_db
from backend.person import Record
from backend.utils import date_ukr, format_age

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form, Response, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import unquote, quote
from starlette.middleware.sessions import SessionMiddleware

templates = Jinja2Templates(directory="frontend")

db = get_db()
person = Record()

templates.env.filters["date_ukr"] = date_ukr
templates.env.filters["format_age"] = format_age
uploaded_json_users = []
added_from_json_ids = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Creating tables...")
    db.create_table()

    yield

    print("Shutting down: Closing connections...")
    db.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="diploma-secret-key")


@app.get("/", response_class=HTMLResponse)
def index(request: Request, search: str = None, show_all: bool = False, show_import: bool = False,
          show_user_id: int = None):
    if show_user_id is not None:
        all_db_users = db.get_all_users()
        db_users = [u for u in all_db_users if u[0] == show_user_id]
    elif search and search.strip():
        search = unquote(search).strip()
        db_users = db.get_defined_user(search)
    elif show_all:
        db_users = db.get_all_users()
    elif show_import:
        all_db_users = db.get_all_users()
        db_users = [u for u in all_db_users if u[0] in added_from_json_ids]
    else:
        db_users = []
    display_users = []
    for u in db_users:
        display_users.append(list(u) + ['БД', u[0]])
    if show_all or show_import:
        for idx, u in enumerate(uploaded_json_users):
            user_list = [
                "JSON", u.get('sex', 'unknown'), u.get('last_name', ''),
                u.get('first_name', ''), u.get('fathers_name', ''),
                u.get('birth_date', ''), u.get('death_date', ''),
                u.get('age', ''), 'JSON', idx
            ]
            display_users.append(user_list)
    error = request.session.pop("error", None)
    query_params = []
    if search and search.strip(): query_params.append(f"search={quote(search)}")
    if show_all: query_params.append("show_all=true")
    if show_import: query_params.append("show_import=true")
    current_qs = "&".join(query_params)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "users": display_users,
            "error": error,
            "search_query": search if search and search.strip() else "",
            "show_all": show_all,
            "show_import": show_import,
            "has_json": len(uploaded_json_users) > 0 or len(added_from_json_ids) > 0,
            "current_qs": current_qs
        }
    )


@app.post("/add")
def add_user(
        request: Request,
        first_name: str = Form(...),
        birth_date: str = Form(...),
        fathers_name: str = Form(""),
        last_name: str = Form(""),
        death_date: str = Form("")
):
    f_name = fathers_name or ''
    l_name = last_name or ''
    d_date = death_date or ''
    person.add_person(birth_date, first_name, f_name, l_name, d_date)
    last_user = person.users[-1]
    error_msg = None
    if last_user.get('First_Name') is None:
        error_msg = "Ім'я має містити щонайменше 2 символи!"
    elif last_user.get('Birth_Date') is None:
        error_msg = "Некоректна дата народження!"
    elif d_date != "" and last_user.get('Death_Date') is None:
        error_msg = "Некоректна дата смерті!"
    elif last_user.get('Birth_Date') and last_user.get('Death_Date'):
        if last_user['Death_Date'] < last_user['Birth_Date']:
            error_msg = "Дата смерті не може бути раніше дати народження!"
    if error_msg:
        person.users = []
        request.session["error"] = error_msg
        return RedirectResponse("/", status_code=303)
    person.save_to_db(db)
    all_users = db.get_all_users()
    new_user_id = all_users[-1][0] if all_users else None
    person.users = []
    if new_user_id:
        return RedirectResponse(f"/?show_user_id={new_user_id}", status_code=303)
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{user_id}")
def delete_user(user_id: int, request: Request):
    db.delete_user(user_id)
    referer = request.headers.get("referer")
    return RedirectResponse(referer or "/", status_code=303)


@app.get("/delete_all")
def delete_all():
    db.delete_all_users()
    return RedirectResponse("/", status_code=303)


@app.get("/export")
def export_users_to_json(search: str = None, show_all: bool = False, show_import: bool = False):
    if search and search.strip():
        search = unquote(search).strip()
        users_from_db = db.get_defined_user(search)
    elif show_all:
        users_from_db = db.get_all_users()
    else:
        users_from_db = []

    export_data = []
    for user in users_from_db:
        user_dict = {
            "sex": user[1],
            "last_name": user[2],
            "first_name": user[3],
            "fathers_name": user[4],
            "birth_date": user[5],
            "death_date": user[6],
            "age": user[7]
        }
        export_data.append(user_dict)

    json_str = json.dumps(export_data, ensure_ascii=False, indent=4)

    return Response(
        content=json_str,
        media_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="users_export.json"'}
    )


@app.post("/upload_json")
async def upload_json(request: Request, file: UploadFile = File(...)):
    global uploaded_json_users, added_from_json_ids
    try:
        content = await file.read()
        data = json.loads(content)
        if isinstance(data, list):
            uploaded_json_users.extend(data)
            added_from_json_ids.clear()
        else:
            request.session["error"] = "Формат файлу має бути списком об'єктів."
    except Exception as e:
        request.session["error"] = "Помилка читання файлу."
    return RedirectResponse("/?show_import=true", status_code=303)


@app.get("/add_from_json/{idx}")
def add_from_json(idx: int, request: Request):
    global uploaded_json_users, added_from_json_ids
    try:
        u = uploaded_json_users.pop(idx)
        db.insert_user(
            sex=u.get('sex'), last_name=u.get('last_name') or "",
            first_name=u.get('first_name'), fathers_name=u.get('fathers_name') or "",
            birth_date=u.get('birth_date'), death_date=u.get('death_date') or "",
            age=u.get('age')
        )
        all_users = db.get_all_users()
        if all_users:
            added_from_json_ids.add(all_users[-1][0])
    except IndexError:
        pass

    referer = request.headers.get("referer")
    return RedirectResponse(referer or "/?show_import=true", status_code=303)


@app.get("/add_from_json/{idx}")
def add_from_json(idx: int):
    global uploaded_json_users
    try:
        u = uploaded_json_users.pop(idx)
        db.insert_user(
            sex=u.get('sex'),
            last_name=u.get('last_name') or "",
            first_name=u.get('first_name'),
            fathers_name=u.get('fathers_name') or "",
            birth_date=u.get('birth_date'),
            death_date=u.get('death_date') or "",
            age=u.get('age')
        )
    except IndexError:
        pass

    return RedirectResponse("/?show_all=true", status_code=303)


@app.get("/clear_json")
def clear_json():
    global uploaded_json_users, added_from_json_ids
    uploaded_json_users.clear()
    added_from_json_ids.clear()
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)

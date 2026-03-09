from backend.DataBase import get_db
from backend.person import Record
from backend.utils import date_ukr, format_age

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import unquote
from starlette.middleware.sessions import SessionMiddleware

templates = Jinja2Templates(directory="frontend")

db = get_db()
person = Record()

templates.env.filters["date_ukr"] = date_ukr
templates.env.filters["format_age"] = format_age


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
def index(request: Request, search: str = None):
    if search:
        search = unquote(search)
        users = db.get_defined_user(search)
    else:
        users = db.get_all_users()

    error = request.session.pop("error", None)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "users": users, "error": error}
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

    if last_user['Birth_Date'] is None:
        error_msg = "Некоректна дата народження!"
    elif d_date != "" and last_user['Death_Date'] is None:
        error_msg = "Некоректна дата смерті!"
    elif last_user['Birth_Date'] and last_user['Death_Date']:
        if last_user['Death_Date'] < last_user['Birth_Date']:
            error_msg = "Дата смерті не може бути раніше дати народження!"

    if error_msg:
        person.users = []
        request.session["error"] = error_msg
        return RedirectResponse("/", status_code=303)

    person.save_to_db(db)
    person.users = []

    return RedirectResponse("/", status_code=303)


@app.get("/delete/{user_id}")
def delete_user(user_id: int):
    db.delete_user(user_id)
    return RedirectResponse("/", status_code=303)


@app.get("/delete_all")
def delete_all():
    db.delete_all_users()
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)

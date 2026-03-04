from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import unquote
from backend.DataBase import get_db
from backend.person import Record
from backend.utils import date_ukr

templates = Jinja2Templates(directory="frontend")

db = get_db()
person = Record()

templates.env.filters["date_ukr"] = date_ukr


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Creating tables...")
    db.create_table()

    yield

    print("Shutting down: Closing connections...")
    db.close()


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def index(request: Request, search: str = None):
    if search:
        search = unquote(search)
        users = db.get_defined_user(search)
    else:
        users = db.get_all_users()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "users": users}
    )


@app.post("/add")
def add_user(
        first_name: str = Form(...),
        fathers_name: str = Form(None),
        last_name: str = Form(None),
        birth_date: str = Form(...),
        death_date: str = Form(None)
):
    f_name = fathers_name or ''
    l_name = last_name or ''
    d_date = death_date or ''

    person.add_person(birth_date, first_name, f_name, l_name, d_date)
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

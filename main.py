
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Pretax Fuel App")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/plan", response_class=HTMLResponse)
def plan_trip(
    request: Request,
    origin: str = Form(...),
    destination: str = Form(...),
    mpg: float = Form(...),
    tank_gallons: float = Form(...),
    reserve_gallons: float = Form(...),
    start_gallons: float = Form(...),
):
    estimated_range = max(start_gallons - reserve_gallons, 0) * mpg
    estimated_total_range = max(tank_gallons - reserve_gallons, 0) * mpg

    sample_stops = [
        {"name": "West Texas Fuel Stop", "reason": "Good corridor pricing", "buy": round(max(tank_gallons - start_gallons, 0) * 0.45, 1)},
        {"name": "Houston Area Fuel Stop", "reason": "Often strong refinery-area pricing", "buy": round(max(tank_gallons - start_gallons, 0) * 0.55, 1)},
    ]

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "origin": origin,
            "destination": destination,
            "mpg": mpg,
            "tank_gallons": tank_gallons,
            "reserve_gallons": reserve_gallons,
            "start_gallons": start_gallons,
            "estimated_range": round(estimated_range, 1),
            "estimated_total_range": round(estimated_total_range, 1),
            "sample_stops": sample_stops,
        },
    )

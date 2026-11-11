from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(
    title="College Fest Event Management",
    version="1.0.0",
)

html_file = Path(__file__).with_name("index.html")


class FestEventBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    category: str = Field(..., min_length=2, max_length=50)
    date: str = Field(..., min_length=5, max_length=30)
    time: str = Field(..., min_length=2, max_length=30)
    venue: str = Field(..., min_length=2, max_length=100)
    coordinator: str = Field(..., min_length=2, max_length=80)
    max_seats: int = Field(..., ge=1, le=10000)


class FestEventCreate(FestEventBase):
    pass


class FestEventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=120)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    date: Optional[str] = Field(None, min_length=5, max_length=30)
    time: Optional[str] = Field(None, min_length=2, max_length=30)
    venue: Optional[str] = Field(None, min_length=2, max_length=100)
    coordinator: Optional[str] = Field(None, min_length=2, max_length=80)
    max_seats: Optional[int] = Field(None, ge=1, le=10000)


class FestEvent(FestEventBase):
    id: int
    registered_seats: int


# Initial Seed Fest Events (inspired by A8 Missing Fest Trophy & Campus Fests)
FEST_EVENTS_DB: List[FestEvent] = [
    FestEvent(
        id=1,
        title="Lead Maestro",
        category="Business & Leadership",
        date="2026-08-30",
        time="11:00 AM",
        venue="Auditorium A",
        coordinator="Sourabh Kumar",
        max_seats=70,
        registered_seats=48,
    ),
    FestEvent(
        id=2,
        title="Bid & Build",
        category="Auction",
        date="2026-08-30",
        time="05:30 PM",
        venue="Seminar Hall A",
        coordinator="Priya Sharma",
        max_seats=200,
        registered_seats=182,
    ),
    FestEvent(
        id=3,
        title="Visual Arts",
        category="photography & Art",
        date="2026-08-30",
        time="02:00 PM",
        venue="Central Quadrangle",
        coordinator="Rahul Verma",
        max_seats=50,
        registered_seats=35,
    ),
    FestEvent(
        id=4,
        title="Debug & Win",
        category="Coding & Tech",
        date="2026-08-30",
        time="11:00 AM",
        venue="lab 3, Computer Science Department",
        coordinator="Sneha Patel",
        max_seats=80,
        registered_seats=75,
    ),
    FestEvent(
        id=5,
        title="FIFA & Valorant Arena",
        category="Gaming",
        date="2026-08-30",
        time="01:00 PM",
        venue="E-Sports Lounge",
        coordinator="Vikram Singh",
        max_seats=40,
        registered_seats=40,
    ),
]
next_event_id = 6


@app.get("/", include_in_schema=False)
def serve_home():
    return FileResponse(html_file, media_type="text/html")


@app.get("/api/events", response_model=List[FestEvent])
def get_events(
    search: Optional[str] = Query(None, description="Search by title, coordinator, or venue"),
    category: Optional[str] = Query(None, description="Filter by event category"),
):
    results = FEST_EVENTS_DB
    if search:
        q = search.lower()
        results = [
            e for e in results
            if q in e.title.lower() or q in e.coordinator.lower() or q in e.venue.lower()
        ]
    if category and category != "All":
        results = [e for e in results if e.category.lower() == category.lower()]
    return results


@app.get("/api/events/{event_id}", response_model=FestEvent)
def get_event(event_id: int):
    for e in FEST_EVENTS_DB:
        if e.id == event_id:
            return e
    raise HTTPException(status_code=404, detail="Event not found")


@app.post("/api/events", response_model=FestEvent, status_code=201)
def create_event(payload: FestEventCreate):
    global next_event_id
    new_event = FestEvent(
        id=next_event_id,
        title=payload.title.strip(),
        category=payload.category.strip(),
        date=payload.date.strip(),
        time=payload.time.strip(),
        venue=payload.venue.strip(),
        coordinator=payload.coordinator.strip(),
        max_seats=payload.max_seats,
        registered_seats=0,
    )
    FEST_EVENTS_DB.append(new_event)
    next_event_id += 1
    return new_event


@app.put("/api/events/{event_id}", response_model=FestEvent)
def update_event(event_id: int, payload: FestEventUpdate):
    for i, e in enumerate(FEST_EVENTS_DB):
        if e.id == event_id:
            updated_data = e.model_dump()
            if payload.title is not None:
                updated_data["title"] = payload.title.strip()
            if payload.category is not None:
                updated_data["category"] = payload.category.strip()
            if payload.date is not None:
                updated_data["date"] = payload.date.strip()
            if payload.time is not None:
                updated_data["time"] = payload.time.strip()
            if payload.venue is not None:
                updated_data["venue"] = payload.venue.strip()
            if payload.coordinator is not None:
                updated_data["coordinator"] = payload.coordinator.strip()
            if payload.max_seats is not None:
                updated_data["max_seats"] = payload.max_seats
                if updated_data["registered_seats"] > payload.max_seats:
                    updated_data["registered_seats"] = payload.max_seats

            updated_event = FestEvent(**updated_data)
            FEST_EVENTS_DB[i] = updated_event
            return updated_event

    raise HTTPException(status_code=404, detail="Event not found")


@app.delete("/api/events/{event_id}")
def delete_event(event_id: int):
    for i, e in enumerate(FEST_EVENTS_DB):
        if e.id == event_id:
            deleted = FEST_EVENTS_DB.pop(i)
            return {"message": f"Event '{deleted.title}' deleted successfully", "id": event_id}
    raise HTTPException(status_code=404, detail="Event not found")


@app.post("/api/events/{event_id}/register")
def register_for_event(event_id: int):
    for e in FEST_EVENTS_DB:
        if e.id == event_id:
            if e.registered_seats >= e.max_seats:
                raise HTTPException(status_code=400, detail="Event is already fully booked!")
            e.registered_seats += 1
            return {
                "message": f"Successfully registered for '{e.title}'!",
                "registered_seats": e.registered_seats,
                "remaining_seats": e.max_seats - e.registered_seats,
            }
    raise HTTPException(status_code=404, detail="Event not found")


@app.get("/api/stats")
def get_stats():
    total_events = len(FEST_EVENTS_DB)
    total_registrations = sum(e.registered_seats for e in FEST_EVENTS_DB)
    total_capacity = sum(e.max_seats for e in FEST_EVENTS_DB)
    categories = sorted(list({e.category for e in FEST_EVENTS_DB}))

    return {
        "total_events": total_events,
        "total_registrations": total_registrations,
        "total_capacity": total_capacity,
        "categories": categories,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.database.application_event_repository import (
    SQLiteApplicationEventRepository,
)
from src.database.application_repository import (
    SQLiteApplicationRepository,
)
from src.database.repository import SQLiteJobRepository
from src.services.application_service import ApplicationService
from src.database.application_event_repository import (
    SQLiteApplicationEventRepository,
)

from src.constants import ApplicationEventType


class ActivityCreateRequest(BaseModel):
    application_id: int
    event_type: ApplicationEventType
    notes: Optional[str] = None

class ApplicationStatusChangeRequest(BaseModel):
    notes: Optional[str] = None

app = FastAPI(title="AI Career Manager API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

job_repository = SQLiteJobRepository()
application_repository = SQLiteApplicationRepository()
event_repository = SQLiteApplicationEventRepository()
application_event_repository = SQLiteApplicationEventRepository()

application_service = ApplicationService(
    application_repository=application_repository,
    event_repository=event_repository,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/applications/needs-attention")
def get_applications_needing_attention():
    due_at = datetime.now(timezone.utc).isoformat()

    applications = (
        application_service.get_applications_needing_attention(
            due_at
        )
    )

    results = []

    for application in applications:
        job = job_repository.get_job(application.job_id)

        results.append(
            {
                "application_id": application.id,
                "job_id": application.job_id,
                "status": application.status.value,
                "next_action": application.next_action,
                "follow_up_at": application.follow_up_at,
                "job_title": (
                    job.get("title")
                    if job is not None
                    else None
                ),
                "company": (
                    job.get("company")
                    if job is not None
                    else None
                ),
            }
        )

    return results

@app.get("/activity/today")
def get_today_activity():
    local_now = datetime.now().astimezone()
    local_timezone = local_now.tzinfo
    today = local_now.date()

    events = application_service.get_activity_for_date(
        today,
        timezone_info=local_timezone,
    )

    results = []

    for event in events:
        application = application_repository.get_application(
            event.application_id
        )

        job = None

        if application is not None:
            job = job_repository.get_job(application.job_id)

        results.append(
            {
                "event_id": event.id,
                "application_id": event.application_id,
                "event_type": event.event_type,
                "occurred_at": event.occurred_at,
                "notes": event.notes,
                "job_id": (
                    application.job_id
                    if application is not None
                    else None
                ),
                "job_title": (
                    job.get("title")
                    if job is not None
                    else None
                ),
                "company": (
                    job.get("company")
                    if job is not None
                    else None
                ),
            }
        )

    return results

@app.post("/activity")
def record_activity(request: ActivityCreateRequest):
    event = application_service.record_activity(
        request.application_id,
        request.event_type,
        notes=request.notes,
    )

    return {
        "event_id": event.id,
        "application_id": event.application_id,
        "event_type": event.event_type,
        "occurred_at": event.occurred_at,
        "notes": event.notes,
    }

@app.get("/applications")
def get_applications():
    applications = application_repository.list_applications()

    results = []

    for application in applications:
        job = job_repository.get_job(application.job_id)

        results.append(
            {
                "application_id": application.id,
                "job_id": application.job_id,
                "status": application.status.value,
                "job_title": (
                    job.get("title")
                    if job is not None
                    else None
                ),
                "company": (
                    job.get("company")
                    if job is not None
                    else None
                ),
            }
        )

    return results

@app.get("/applications/{application_id}/activity")
def get_application_activity(application_id: int):
    application = application_repository.get_application(
        application_id
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    job = job_repository.get_job(application.job_id)

    events = application_event_repository.list_events(
        application_id
    )

    return [
        {
            "event_id": event.id,
            "application_id": event.application_id,
            "event_type": event.event_type,
            "occurred_at": event.occurred_at,
            "notes": event.notes,
            "job_id": application.job_id,
            "job_title": (
                job.get("title")
                if job is not None
                else None
            ),
            "company": (
                job.get("company")
                if job is not None
                else None
            ),
        }
        for event in events
    ]

@app.post("/applications/{application_id}/mark-closed")
def mark_application_closed(
    application_id: int,
    request: ApplicationStatusChangeRequest,
):
    application = application_service.mark_closed(
        application_id,
        notes=request.notes,
    )

    return {
        "application_id": application.id,
        "job_id": application.job_id,
        "status": application.status.value,
    }

@app.post("/applications/{application_id}/mark-withdrawn")
def mark_application_withdrawn(
    application_id: int,
    request: ApplicationStatusChangeRequest,
):
    application = application_service.mark_withdrawn(
        application_id,
        notes=request.notes,
    )

    return {
        "application_id": application.id,
        "job_id": application.job_id,
        "status": application.status.value,
    }

@app.post("/applications/{application_id}/mark-rejected")
def mark_application_rejected(
    application_id: int,
    request: ApplicationStatusChangeRequest,
):
    application = application_service.mark_rejected(
        application_id,
        notes=request.notes,
    )

    return {
        "application_id": application.id,
        "job_id": application.job_id,
        "status": application.status.value,
    }

@app.get("/activity-types")
def get_activity_types():
    return [
        event_type.value
        for event_type in ApplicationEventType
    ]
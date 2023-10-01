from typing import List

from fastapi import Depends, APIRouter, HTTPException
from starlette.requests import Request

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.webhook.models import (
    Specialty,
)
from infrastructure.webhook.utils import get_repo

doctor_router = APIRouter(prefix="/doctors")
specialties_router = APIRouter(prefix="/specialties")


@doctor_router.get("/{doctor_id}")
async def get_doctor(doctor_id: int, repo: RequestsRepo = Depends(get_repo)):
    result = await repo.doctors.get_doctor(doctor_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {
        **result,
    }


@doctor_router.get("/")
async def get_all_doctors(repo: RequestsRepo = Depends(get_repo)):
    doctors = await repo.doctors.get_all_doctors()
    return doctors


@specialties_router.get("/", response_model=List[Specialty])
async def get_specialties(repo: RequestsRepo = Depends(get_repo)):
    specialties = await repo.doctors.get_specialties()
    return specialties


@doctor_router.post("/book_slot")
async def book_doctor_slot_endpoint(
    request: Request, repo: RequestsRepo = Depends(get_repo)
):
    payload = await request.json()

    booking_id = await repo.doctors.book_slot(payload)
    return {"status": "success", "booking_id": booking_id}

"""Contains the routes for temporal profile based conformance checking."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/temporal-profile", tags=["Temporal Profile CC"])

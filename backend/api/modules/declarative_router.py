"""Contains the routes for handling declarative conformance checking."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/declarative", tags=["Declarative CC"])

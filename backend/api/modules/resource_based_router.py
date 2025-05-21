"""Contains the routes for handling resource-based conformance checking."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/resource-based", tags=["Resource-Based CC"])

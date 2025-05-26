"""Contains the tasks for temporal profile based conformance checking."""

from fastapi import FastAPI

from backend.api.models.schemas.job_models import JobStatus
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.conformance_checking.temporal_profile import (
    ConformanceResultType,
    TemporalProfile,
)


def compute_and_store_temporal_conformance_result(
    app: FastAPI, job_id: str, celonis_connection: CelonisConnectionManager, zeta: float
) -> None:
    """Computes the temporal profile and stores it in the app state.

    Args:
        app (FastAPI): The FastAPI application instance.
        job_id: The ID of the job.
        celonis_connection: The Celonis connection manager instance.
        zeta: The zeta value used for temporal profile conformance checking.
    """
    rec: JobStatus = app.state.jobs.get[job_id]

    try:
        rec.status = "running"
        df = celonis_connection.get_basic_dataframe_from_celonis()

        if df is None or df.empty:
            rec.status = "failed"
            return

        tp = TemporalProfile(df)
        tp.discover_temporal_profile()
        tp.check_temporal_conformance(zeta=zeta)
        tp_conformance_result: ConformanceResultType = (
            tp.get_temporal_conformance_result()
        )

        rec.result = {"temporal_conformance_result": tp_conformance_result}
        rec.status = "complete"
        rec.error = None

    except Exception as e:
        rec.status = "failed"
        rec.error = str(e)

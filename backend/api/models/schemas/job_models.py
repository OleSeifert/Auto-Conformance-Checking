"""Contains the Pydantic model for a generic job.

The job is used to represent a job in the system.
"""

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel


class JobStatus(BaseModel):
    """The job status model.

    This model is used to represent the status of a job in the system.
    It contains the module name, status, result, and error message.
    The status can be one of the following: "pending", "running",
    "completed", or "failed".
    The result is an optional dictionary containing the result of the job.
    The error is an optional string containing the error message if the
    job failed.
    """

    module: str  # e.g. log_skeleton, temporal
    status: Literal["pending", "running", "completed", "failed"]
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

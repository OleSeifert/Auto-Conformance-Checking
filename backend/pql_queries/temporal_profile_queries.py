"""Queries tused to get temporal profile related data from Celonis."""

import pandas as pd
from pandas import DataFrame as DataFrame

from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)


def get_temporal_conformance_result(
    celonis: CelonisConnectionManager,
    zeta: float,
) -> DataFrame:
    """Returns the temporal conformance result from Celonis.

    Parameters:
    celonis: CelonisConnectionManager
        The Celonis connection manager instance.
    zeta: float
        The zeta value used for temporal conformance checking.

    Returns:
    DataFrame
        A DataFrame containing the deviations for each trace. Each row contains:
        - Case ID of the recorded deviation.
        - Source activity of the recorded deviation.
        - Target activity of the recorded deviation.
        - Time passed between the occurrence of the source activity and the target activity.
        - Value of (time passed - mean)/std for this occurrence (zeta).
    """
    activity_query = {
        "Case": """ "ACTIVITIES"."case:concept:name" """,
        "Activity": """ "ACTIVITIES"."concept:name" """,
        "Timestamp": """ "ACTIVITIES"."time:timestamp" """,
    }
    activities_df = celonis.get_dataframe_from_celonis(activity_query)  # type: ignore

    activities_df["Timestamp"] = pd.to_datetime(activities_df["Timestamp"])  # type: ignore
    activities_df = activities_df.sort_values(["Case", "Timestamp"])  # type: ignore

    all_pairs = []

    for case_id, case_data in activities_df.groupby("Case"):  # type: ignore
        case_data = case_data.sort_values("Timestamp").reset_index(drop=True)  # type: ignore

        for i in range(len(case_data) - 1):  # type: ignore
            act_i = case_data.iloc[i]["Activity"]  # type: ignore
            time_i = case_data.iloc[i]["timestamp"]  # type: ignore

            for j in range(i + 1, len(case_data)):  # type: ignore
                act_j = case_data.iloc[j]["Activity"]  # type: ignore
                time_j = case_data.iloc[j]["Timestamp"]  # type: ignore

                if time_j >= time_i:
                    time_diff = (time_j - time_i).total_seconds()  # type: ignore
                    all_pairs.append(  # type: ignore
                        {
                            "Case": case_id,
                            "Source": act_i,
                            "Target": act_j,
                            "Time Passed": time_diff,
                        }
                    )

    pairs_df = pd.DataFrame(all_pairs)

    temporal_profile = (  # type: ignore
        pairs_df.groupby(["Source", "Target"])["Time Passed"]  # type: ignore
        .agg([("Mean Time", "mean"), ("Std Time", "std")])  # type: ignore
        .reset_index()
    )

    merged = pairs_df.merge(temporal_profile, on=["Source", "Target"], how="left")  # type: ignore
    merged = merged[(merged["Time_Passed"] > 0) & (merged["Std_Time"] > 0)]

    lower_bound = merged["Mean Time"] - zeta * merged["Std Time"]  # type: ignore
    upper_bound = merged["Mean Time"] + zeta * merged["Std Time"]  # type: ignore

    deviation_mask = (merged["Time Passed"] < lower_bound) | (  # type: ignore
        merged["Time Passed"] > upper_bound
    )

    merged["Zeta"] = (
        abs(merged["Time Passed"] - merged["Mean Time"]) / merged["Std Time"]  # type: ignore
    )

    deviations = merged[deviation_mask]  # type: ignore
    result_df = deviations[["Case", "Source", "Target", "Time Passed", "Zeta"]].copy()  # type: ignore
    return result_df  # type: ignore

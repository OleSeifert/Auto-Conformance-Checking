"""Queries that can be used to get log-skeleton related data from celonis."""

from itertools import combinations

from pandas import DataFrame

from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.pql_queries.general_queries import get_activities, get_cases


# Always before
def get_always_before_relation(celonis: CelonisConnectionManager) -> DataFrame:
    """Caculates which pairs of Activity always occurr before each other.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        A dataframe that contains for pairs of Activities whether
        they always occurr before each other.
    """
    target_df = DataFrame(columns=["Activity A", "Activity B", "Rel"])
    act_table = get_activities(celonis)
    activitiy_pairs = list(combinations(act_table["Activities"].to_list(), 2))  # type: ignore
    i = 0
    for pair in activitiy_pairs:  # type: ignore
        # Returns 1 if a node eventually occurrs before another in a trace
        query = {
            "A before B": f"""MATCH_PROCESS ("ACTIVITIES"."concept:name", NODE [{pair[0]}] as src,
                            NODE [{pair[1]}] as tgt CONNECTED BY EVENTUALLY [src , tgt])""",
            "B before A": f"""MATCH_PROCESS ("ACTIVITIES"."concept:name", NODE [{pair[1]}] as src,
                            NODE [{pair[0]}] as tgt CONNECTED BY EVENTUALLY [src , tgt])""",
        }
        pair_df = celonis.get_dataframe_from_celonis(query)  # type: ignore
        if (pair_df["B before A"] == 1).any() and not (  # type: ignore
            pair_df["A before B"] == 1  # type: ignore
        ).any():  # type: ignore
            target_df.loc[i] = [pair[1], pair[0], "true"]
        elif (pair_df["A before B"] == 1).any() and not (  # type: ignore
            pair_df["B before A"] == 1  # type: ignore
        ).any():
            target_df.loc[i] = [pair[0], pair[1], "true"]
        else:
            target_df.loc[i] = [pair[0], pair[1], "false"]
        i = i + 1

    return target_df


# Always after
def get_always_after_relation(celonis: CelonisConnectionManager) -> DataFrame:
    """Caculates which pairs of Activity always occurr after each other.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        A dataframe that contains for pairs of Activities whether
        they always occurr after each other.
    """
    target_df = DataFrame(columns=["Activity A", "Activity B", "Rel"])
    act_table = get_activities(celonis)
    activitiy_pairs = list(combinations(act_table["Activities"].to_list(), 2))  # type: ignore
    i = 0
    for pair in activitiy_pairs:  # type: ignore
        # Returns 1 if a node eventually occurrs after another in a trace
        query = {
            "A after B": f"""MATCH_PROCESS ("ACTIVITIES"."concept:name", NODE [{pair[1]}] as src,
                            NODE [{pair[0]}] as tgt CONNECTED BY EVENTUALLY [src , tgt])""",
            "B after A": f"""MATCH_PROCESS ("ACTIVITIES"."concept:name", NODE [{pair[0]}] as src,
                            NODE [{pair[1]}] as tgt CONNECTED BY EVENTUALLY [src , tgt])""",
        }
        pair_df = celonis.get_dataframe_from_celonis(query)  # type: ignore
        if (pair_df["B after A"] == 1).any() and not (  # type: ignore
            pair_df["A after B"] == 1  # type: ignore
        ).any():  # type: ignore
            target_df.loc[i] = [pair[1], pair[0], "true"]
        elif (pair_df["A after B"] == 1).any() and not (  # type: ignore
            pair_df["B after A"] == 1  # type: ignore
        ).any():
            target_df.loc[i] = [pair[0], pair[1], "true"]
        else:
            target_df.loc[i] = [pair[0], pair[1], "false"]
        i = i + 1

    return target_df


# Equivalent
def get_equivalance_relation(celonis: CelonisConnectionManager) -> DataFrame:
    """Caculates which pairs of Activity are equivalent.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        A dataframe that contains for pairs of Activities whether
        they are equivalent.
    """
    target_df = DataFrame(columns=["Activity A", "Activity B", "Rel"])
    cases = get_cases(celonis)["Cases"].to_list()  # type: ignore
    act_table = get_activities(celonis)
    activitiy_pairs = list(combinations(act_table["Activities"].to_list(), 2))  # type: ignore
    query = {
        "Case": """ "ACTIVITIES"."case:concept:name" """,
        "Activity": """  "ACTIVITIES"."concept:name" """,
        "Count": """ COUNT ( "ACTIVITIES"."concept:name" ) """,
    }
    df = celonis.get_dataframe_from_celonis(query)  # type: ignore
    i = 0
    for pair in activitiy_pairs:  # type: ignore
        for case in cases:  # type: ignore
            case_df = df[df["Case"] == case]  # type: ignore
            occurrence_a = case_df[case_df["Activity"] == pair[0]]["Count"].values[0]  # type: ignore
            occurrence_b = case_df[case_df["Activity"] == pair[1]]["Count"].values[0]  # type: ignore
            if occurrence_a != occurrence_b:
                target_df.loc[i] = [pair[0], pair[1], "false"]
                break
        target_df.loc[i] = [pair[0], pair[1], "true"]
        i = i + 1

    return target_df


# Exclusive Choice
def get_exclusive_choice_relaion(celonis: CelonisConnectionManager) -> DataFrame:
    """Caculates which pairs of Activity are exclusive choice.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        A dataframe that contains for pairs of Activities whether
        they are exclusive choice.
    """
    target_df = DataFrame(columns=["Activity A", "Activity B", "Rel"])
    cases = get_cases(celonis)["Cases"].to_list()  # type: ignore
    act_table = get_activities(celonis)
    activitiy_pairs = list(combinations(act_table["Activities"].to_list(), 2))  # type: ignore
    query = {
        "Case": """ "ACTIVITIES"."case:concept:name" """,
        "Activity": """  "ACTIVITIES"."concept:name" """,
        "Count": """ COUNT ( "ACTIVITIES"."concept:name" ) """,
    }
    df = celonis.get_dataframe_from_celonis(query)  # type: ignore
    i = 0
    for pair in activitiy_pairs:  # type: ignore
        for case in cases:  # type: ignore
            case_df = df[df["Case"] == case]  # type: ignore
            occurrence_a = case_df[case_df["Activity"] == pair[0]]["Count"].values[0]  # type: ignore
            occurrence_b = case_df[case_df["Activity"] == pair[1]]["Count"].values[0]  # type: ignore
            if occurrence_a > 0 and occurrence_b > 0:
                target_df.loc[i] = [pair[0], pair[1], "false"]
                break
        target_df.loc[i] = [pair[0], pair[1], "true"]
        i = i + 1

    return target_df


# Never together
# No way this is faster
def get_never_together_relation(celonis: CelonisConnectionManager) -> DataFrame:
    """Caculates which pairs of Activity never occurr together.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        A dataframe that contains for pairs of Activities whether
        they are never together in a trace
    """
    target_df = DataFrame(columns=["Activity A", "Activity B", "Rel"])
    act_table = get_activities(celonis)
    activitiy_pairs = list(combinations(act_table["Activities"].to_list(), 2))  # type: ignore
    i = 0
    for pair in activitiy_pairs:  # type: ignore
        # Returns 1 if both acts are in case, 0 if not
        query = {
            "Count": f"""MATCH_ACTIVITIES ("ACTIVITIES"."concept:name", NODE [{pair[0]}, {pair[1]}])"""
        }
        pair_df = celonis.get_dataframe_from_celonis(query)  # type: ignore
        if (pair_df["Count"] == 1).any():  # type: ignore
            target_df.loc[i] = [pair[0], pair[1], "false"]
        else:
            target_df.loc[i] = [pair[0], pair[1], "true"]
        i = i + 1

    return target_df


# Directly Follows + Counter
def get_directly_follows_relation_and_count(
    celonis: CelonisConnectionManager,
) -> DataFrame:
    """Gets the directly follows relation and count.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        A pandas dataframe that contains a statement whether the
        dirctly follows relation is true and the count for each
    """
    dfg_query = {
        "Source": """ SOURCE("ACTIVITIES"."concept:name")""",
        "Target": """ TARGET("ACTIVITIES"."concept:name")""",
        "Rel": """  CASE WHEN
                    COUNT(SOURCE ("ACTIVITIES"."concept:name")) > 0
                    THEN 'true' ELSE 'false'
                    END""",
        "Count": """ COUNT(SOURCE("ACTIVITIES"."concept:name"))""",
    }

    return celonis.get_dataframe_from_celonis(dfg_query)  # type: ignore

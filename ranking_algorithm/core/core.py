import math

import pandas as pd

from . import settings


def create_decision_matrix(data: pd.DataFrame = None) -> pd.DataFrame:
    """Create decision matrix for ranking algorithm

    Args:
        data (pd.DataFrame, optional): spaces data. Defaults to None.

    Returns:
        pd.DataFrame: the created decision matrix
    """
    # Read spaces data file
    processed_combinations_data = (
        pd.read_json(settings.PROC_SPACES_DATA_PATH)
        if data is None
        else pd.DataFrame(data)
    )

    matrix = pd.DataFrame(
        columns=["total_time_range", "num_spaces", "num_cancellable_spaces"],
        index=processed_combinations_data.columns,
    )

    # Loop to take only value of specific attribute
    for comb, details in processed_combinations_data.items():
        for det, value in details.items():
            if det in ["total_time_range", "num_spaces", "num_cancellable_spaces"]:
                matrix[det][comb] = value

    decision_matrix = pd.DataFrame(matrix)

    # decision_matrix.to_pickle(settings.DECISION_MATRIX_PATH)
    return decision_matrix


def entropy_weights_method(
    goal_time: int, decision_matrix: pd.DataFrame = None
) -> pd.DataFrame:
    """Tunning the criteria weights using entropy method for ranking system

    Args:
        goal_time (int): the desired time span
        decision_matrix (pd.DataFrame, optional): spaces combinations details. Defaults to None.

    Returns:
        pd.DataFrame: weights dataframe
    """
    dmatrix = (
        pd.read_pickle(settings.DECISION_MATRIX_PATH)
        if decision_matrix is None
        else decision_matrix
    )

    # Substitute total_time_range by distance column
    dmatrix["distance"] = (dmatrix["total_time_range"] - goal_time).abs()
    dmatrix.drop(columns=["total_time_range"], inplace=True)

    # Start the algorithm
    rows, cols = dmatrix.shape
    k = 1.0 / math.log(rows)

    lnf = [[None] * cols for i in range(rows)]

    for i in range(0, rows):
        for j in range(0, cols):
            if dmatrix.iloc[i][j] == 0:
                lnfij = 0.0
            else:
                p = dmatrix.iloc[i][j] / dmatrix.iloc[:, j].sum()
                lnfij = math.log(p) * p * (-k)
            lnf[i][j] = lnfij
    lnf = pd.DataFrame(
        lnf, index=decision_matrix.index, columns=decision_matrix.columns
    )

    e = 1 - lnf.sum(axis=0)
    weights = [[None] * 1 for i in range(cols)]
    for j in range(0, cols):
        weightsj = e[j] / sum(e)
        weights[j] = weightsj

    weights = pd.DataFrame(weights)
    weights = weights.round(5)
    weights.index = dmatrix.columns
    weights.columns = ["weight"]
    return weights

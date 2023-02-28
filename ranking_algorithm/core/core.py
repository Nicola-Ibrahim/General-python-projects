def cal_std(combs_time_span: list[int], target: int) -> float:
    """Calculate the std for the spaces' combination time span

    Args:
        combs_time (list[int]): available time list for the spaces combinations
        target (int): the target time value to be obtained

    Returns:
        list[float]: list of z-scores for the spaces' combination
    """
    var = sum(pow(x - target, 2) for x in combs_time_span) / len(combs_time_span)
    std = math.sqrt(var)

    return std


def cal_zscores(combs_time_span: list[int], target: int) -> list[float]:
    """Calculate the z-scores for the spaces' combination

    Args:
        combs_time (list[int]): available time list for the spaces combinations
        target (int): the target time value to be obtained

    Returns:
        list[float]: list of z-scores for the spaces' combination
    """
    std = cal_std(combs_time_span)

    z_scores = [(time_span - target) / std for time_span in combs_time_span]

    return z_scores


def get_score(z_score: float, num_cancellable_spaces: int, num_spaces: int) -> float:
    """Get the score for a specific spaces combination

    Args:
        z_score (float): combination z_score value
        num_cancellable_spaces (int): combination num of cancellable spaces
        num_spaces (int): combination num of spaces

    Returns:
        float: score value
    """
    if z_score > 0:
        score = 1 / (
            (0.6 * num_cancellable_spaces) + (0.3 * num_spaces) + (0.1 * z_score)
        )

    else:
        score = (0.1 * z_score) / ((0.6 * num_cancellable_spaces) + (0.3 * num_spaces))

    return round(score, 3)


def cal_scores(
    z_scores: list[float], cancellable_spaces: list[int], spaces: list[int]
) -> list[float]:
    """Calculate the scores list for the spaces combinations

    Args:
        z_scores (list[float]): list of z_scores for the spaces' combination
        cancellable_spaces (list[int]): num of cancellable spaces for each the spaces' combination
        spaces (list[int]): num of spaces spaces for each the spaces' combination

    Returns:
        list[float]: _description_
    """

    scores = []

    for z_score, num_cancellable_spaces, num_spaces in zip(
        z_scores, cancellable_spaces, spaces
    ):

        scores.append(get_score(z_score, num_cancellable_spaces, num_spaces))

    return scores

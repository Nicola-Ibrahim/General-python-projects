import collections
import math
from itertools import chain, combinations


def get_combinations(spaces: list):
    return chain.from_iterable(combinations(spaces, r) for r in range(len(spaces) + 1))


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


def count_ones_sets(combination: list | tuple) -> int:
    """Count the number of lists containing sequence of one

    Args:
        combination (list | tuple): the chromosomes combination

    Returns:
        int: the number of list of ones

    Example:
        count_ones_sets([1, 0, 1, 0, 1, 0, 1, 1, 0]) -> count = 4
    """

    count = 0
    for i, j in zip(combination, combination[1:] + [0]):
        if i == 1 and j == 0:
            count += 1

    return count


def cal_ranks(
    z_scores: list[float], cancellable_spaces: list[int], spaces: list[int]
) -> list[float]:
    """Calculate the ranks list for the spaces combinations

    Args:
        z_scores (list[float]): list of z_scores for the spaces' combination
        cancellable_spaces (list[int]): num of cancellable spaces for each the spaces' combination
        spaces (list[int]): num of spaces spaces for each the spaces' combination

    Returns:
        list[float]: _description_
    """

    ranks = []

    for z_score, num_cancellable_spaces, num_spaces in zip(
        z_scores, cancellable_spaces, spaces
    ):
        rank = (0.1 * z_score) / (0.6 * num_cancellable_spaces + 0.3 * num_spaces)
        rank = round(rank, 3)
        ranks.append(rank)

    return ranks


z_scores = (-0.86, -0.43, -1.147, +1.01, -0.158, +0.339, +1.653)
cancellable_spaces = (1, 0, 1, 0, 1, 1, 1)
spaces = (1, 1, 1, 2, 2, 2, 3)

spaces_name = [
    "A1",
    "A2",
    "A3",
    ("A1", "A2"),
    ("A1", "A3"),
    ("A2", "A3"),
    ("A1", "A2", "A3"),
]

spaces_score = dict(zip(spaces_name, cal_ranks(z_scores, cancellable_spaces, spaces)))

print(sorted(spaces_score.items(), key=lambda x: x[1], reverse=True))

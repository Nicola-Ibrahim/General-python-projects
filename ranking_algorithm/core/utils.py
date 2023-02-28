import collections
import itertools
import json
from functools import wraps
from typing import Callable

from . import parsing, settings, utils


def encode_spaces_time_range(spaces_data: dict) -> dict:
    """Encode available dates' time for each space

    Args:
        spaces_data (dict): spaces' details
        time_span (int): the search range

    Returns:
        dict: encoded time for each space-date pair
    """
    encoded_time = collections.defaultdict(lambda: collections.defaultdict(dict))

    for space, details in spaces_data.items():
        for available_date in details["available_dates"]:

            date_as_key = available_date["start"].date().strftime("%d/%m/%Y")

            # If the date doesn't have encoded list of hour bits
            # Assign 0 bits list
            if not encoded_time[space][date_as_key].get("enc"):
                encoded_time[space][date_as_key]["enc"] = [0] * 24

            # If the date doesn't have time range
            # Assign 0 to time range
            if not encoded_time[space][date_as_key].get("time_range"):
                encoded_time[space][date_as_key]["time_range"] = 0

            # Find time range each day gives
            time_range = available_date["end"].hour - available_date["start"].hour
            encoded_time[space][date_as_key]["time_range"] += time_range

            # Convert time range to a Slicer
            time_slice = slice(
                available_date["start"].hour, available_date["end"].hour + 1, 1
            )

            # Flip bits where there is free time
            encoded_time[space][date_as_key]["enc"][time_slice] = [1] * time_range

    return encoded_time


def save_to_json(func: Callable[[str], dict]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        encoded_time_range = func(*args, **kwargs)

        # Save to json file
        with open(
            settings.BASE_DIR / "fixtures/reservations_encoded_data.json", mode="w"
        ) as f:
            json.dump(encoded_time_range, f, indent=4, cls=parsing.DateTimeEncoder)

        return encoded_time_range

    return wrapper


@save_to_json
def get_encoded_spaces_time_range(file_path: str) -> dict:

    # Read spaces data file

    with open(settings.BASE_DIR / file_path, mode="r") as f:
        spaces_data = json.load(f, object_hook=parsing.decode_date_time)

    # Encode the spaces; time range
    encoded_time_range = utils.encode_spaces_time_range(spaces_data=spaces_data)

    return encoded_time_range


def get_space_combinations(spaces: list):
    combs = list(
        itertools.chain.from_iterable(
            itertools.combinations(spaces, r) for r in range(len(spaces) + 1)
        )
    )
    # Remove the first empty element [(),]
    return combs[1:]


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

import collections
import itertools
import json
from functools import wraps
from typing import Callable

import numpy as np
import pandas as pd

from . import parsing, settings


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


def read_json_file(file_path):
    with open(file_path, mode="r") as f:
        file = json.load(f, object_hook=parsing.decode_date_time)

    return file


def save_to_json(file_path):
    def inner(func: Callable[[str], dict]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            encoded_time_range = func(*args, **kwargs)

            # Save to json file
            if settings.SAVE_FILES_FLAG:
                with open(file_path, mode="w") as f:
                    json.dump(
                        encoded_time_range, f, indent=4, cls=parsing.DateTimeEncoder
                    )

            return encoded_time_range

        return wrapper

    return inner


def encode_spaces_time_range(spaces_data: dict) -> dict:
    """Encode available dates' time for each space

    Args:
        spaces_data (dict): spaces' details
        time_span (int): the search range

    Returns:
        dict: encoded time for each space-date pair
    """
    encoded_time_range = collections.defaultdict(
        lambda: collections.defaultdict(
            lambda: collections.defaultdict(lambda: collections.defaultdict(dict))
        )
    )

    for space, details in spaces_data.items():
        for available_date in details["available_dates"]:

            date_as_key = available_date["start"].date().strftime("%d/%m/%Y")

            # Assign 0 bits list
            if not encoded_time_range[space]["dates"][date_as_key]["enc"]:
                encoded_time_range[space]["dates"][date_as_key]["enc"] = [
                    0
                ] * settings.NUM_OF_ENCODED_BITS

            end_time = available_date["end"].hour
            if available_date["end"].hour >= 23 and available_date["end"].minute > 0:
                end_time = available_date["end"].hour + 1

            # Flip bits where there is free time
            for i in range(available_date["start"].hour, end_time):
                encoded_time_range[space]["dates"][date_as_key]["enc"][i] = 1

            # Assign 0 value to time range

            encoded_time_range[space]["dates"][date_as_key]["time_range"] = sum(
                encoded_time_range[space]["dates"][date_as_key]["enc"]
            )

        encoded_time_range[space]["cancellable"] = details["cancellable"]

    return encoded_time_range


# @save_to_json(settings.PRE_PROC_SPACES_TIME_PATH)
def get_encoded_spaces_time_range() -> dict:

    # Read spaces data file
    with open(settings.RAW_SPACES_DATA_PATH, mode="r") as f:
        spaces_data = json.load(f, object_hook=parsing.decode_date_time)

    # Encode the spaces; time range
    encoded_time_range = encode_spaces_time_range(spaces_data=spaces_data)

    return encoded_time_range


def create_space_combinations(spaces: list) -> list:
    """Create combinations from the available spaces

    Args:
        spaces (list): spaces list

    Returns:
        list: list of created combinations
    """
    combinations = list(
        itertools.chain.from_iterable(
            itertools.combinations(spaces, r) for r in range(len(spaces) + 1)
        )
    )
    # Remove the first empty element [(),]
    combinations = combinations[1:]

    return combinations


def get_cancellable_percent(cancellables: list) -> float:
    """Get the percentage of cancellable spaces from the combination

    Args:
        cancellables (dict): cancellable values

    Returns:
        float: cancellable percentage value
    """
    return sum(cancellables) / len(cancellables)


def bitwise_time_ranges(time_ranges: np.ndarray) -> list:
    """Do bitwise operator (OR) for binary time ranges

    Args:
        time_ranges (np.ndarray): time ranges for each combination

    Returns:
        list: squashed time ranges
    """
    result = np.zeros(shape=[1, settings.NUM_OF_ENCODED_BITS], dtype=int).flatten()
    for time_range in time_ranges:
        result |= np.array(time_range)

    return result.tolist()


def get_unique_dates(values):
    # Get unique dates
    dates = set()
    for details in values:
        dates.update(list(details["dates"].keys()))

    dates = sorted(dates)

    return dates


def merge_combination_time(combination_details: dict) -> dict:
    """Merge combination spaces' time range

    Args:
        combination_details (dict): spaces' detail in each combination

    Returns:
        dict: merged encoded time range
    """

    comb_keys = list(combination_details.keys())

    # If there is only one space in the combination
    if len(comb_keys) < 2:
        # Return the sames corresponding space details to the combination
        return list(combination_details.values())[0]["dates"]

    # If there is many spaces in the combination
    # Then, squash the spaces dates into one combination

    encoded_time_range = collections.defaultdict(lambda: collections.defaultdict(dict))

    dates = get_unique_dates(combination_details.values())
    for date in dates:
        summing_date = [
            combination_details[key]["dates"][date]["enc"]
            for key in combination_details.keys()
        ]

        encoded_time_range[date]["enc"] = bitwise_time_ranges(summing_date)

        if not encoded_time_range[date]["time_range"] and isinstance(
            encoded_time_range[date]["time_range"], dict
        ):
            encoded_time_range[date]["time_range"] = 0

        encoded_time_range[date]["time_range"] += sum(encoded_time_range[date]["enc"])
    return encoded_time_range


def squash_spaces_combination_details(encoded_spaces_data: dict) -> dict:
    """Squash available dates' time for each space

    Args:
        spaces_data (dict): encoded spaces' details

    Returns:
        dict: encoded time for each combination
    """

    combinations = create_space_combinations(encoded_spaces_data.keys())
    max_combination_size = len(combinations[-1])

    encoded_time_range = collections.defaultdict(
        lambda: collections.defaultdict(lambda: collections.defaultdict(dict))
    )

    for comb in combinations:

        comb_to_str = ",".join(comb)

        # Get the cancellable spaces
        encoded_time_range[comb_to_str][
            "cancellable_spaces_percentage"
        ] = get_cancellable_percent(
            [encoded_spaces_data[space]["cancellable"] for space in comb]
        )

        encoded_time_range[comb_to_str]["num_cancellable_spaces"] = sum(
            [encoded_spaces_data[space]["cancellable"] for space in comb]
        )

        # Get the spaces
        encoded_time_range[comb_to_str]["spaces_percentage"] = (
            len(comb) / max_combination_size
        )

        encoded_time_range[comb_to_str]["num_spaces"] = len(comb)

        # Merging spaces' time in each combination
        encoded_time_range[comb_to_str]["dates"] = merge_combination_time(
            {i: encoded_spaces_data[i] for i in comb}
        )

        # Get total time range\
        for date in encoded_time_range[comb_to_str]["dates"]:
            if not encoded_time_range[comb_to_str]["total_time_range"]:
                encoded_time_range[comb_to_str]["total_time_range"] = 0

            encoded_time_range[comb_to_str]["total_time_range"] += encoded_time_range[
                comb_to_str
            ]["dates"][date]["time_range"]

    return encoded_time_range


# @save_to_json(settings.PROC_SPACES_DATA_PATH)
def get_encoded_spaces_combinations(data: dict) -> dict:
    """Get the encoded combination of spaces

    Returns:
        dict: An encoded combination of spaces
    """
    # Read spaces data file
    encoded_spaces_data = (
        read_json_file(settings.PRE_PROC_SPACES_TIME_PATH) if data is None else data
    )

    # Encode the spaces; time range
    encoded_time_range = squash_spaces_combination_details(
        encoded_spaces_data=encoded_spaces_data
    )

    return encoded_time_range


import collections
import json

import parsing
import utils


def encode_time_range(spaces_data: dict) -> dict:
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


def run(base_path: str):
    with open(base_path / "fixture/reservations_dummy_data.json", mode="r") as f:
        spaces_data = json.load(f, object_hook=parsing.decode_date_time)

    encoded_time = encode_time_range(spaces_data=spaces_data)

    # Save to json file
    with open(base_path / "fixture/reservations_encoded_data.json", mode="w") as f:
        json.dump(encoded_time, f, indent=4, cls=parsing.DateTimeEncoder)

    combinations = utils.get_space_combinations(encoded_time.keys())
    print(combinations)

import json

from parsing import decode_date_time





def get_time_span(data: dict):

    # Create combinations from the available spaces
    combs = list(get_combinations(data.keys()))
    print(combs)

    # for space, value in data.items():
    #     print(space)
    #     for date in value["dates"]:
    #         print(date["end"] - date["start"])


def main():
    with open("./reservations_dummy_data.json", mode="r") as f:
        data = json.load(f, object_hook=decode_date_time)

    get_time_span(data)


if __name__ == "__main__":
    main()

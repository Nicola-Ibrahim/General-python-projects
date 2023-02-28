from . import utils


def run():
    encoded_time_range = utils.get_encoded_spaces_time_range(
        file_path="fixtures/reservations_dummy_data.json"
    )
    print(encoded_time_range)
    # combinations = utils.get_space_combinations(encoded_time.keys())
    # print(combinations)

    # spaces_name = [
    #     "A1",
    #     "A2",
    #     "A3",
    #     ("A1", "A2"),
    #     ("A1", "A3"),
    #     ("A2", "A3"),
    #     ("A1", "A2", "A3"),
    # ]

    # spaces_score = dict(zip(spaces_name, cal_scores(z_scores, cancellable_spaces, spaces)))

    # print(sorted(spaces_score.items(), key=lambda x: x[1], reverse=True))

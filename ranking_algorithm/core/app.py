from . import rank, utils


def run():
    goal_time = 8
    encoded_time_range = utils.get_encoded_spaces_time_range()
    space_combinations = utils.get_encoded_spaces_combinations(encoded_time_range)
    decision_matrix = rank.create_decision_matrix(
        goal_time=goal_time, data=space_combinations
    )
    # weights = tunning.entropy_weights_method(
    #     goal_time=goal_time, decision_matrix=decision_matrix
    # )
    # print(weights)

    # weights = [69.4, 21.0, 9.6]
    # weights = [70.5, 20.5, 9.0]
    # weights = [70.5, 20.5, 9.0]
    # weights = [71.7, 21.7, 6.6]  # CR = 3.9%
    # weights = [72.7, 20.0, 7.3]  # CR = 1%
    weights = [69.2, 23.1, 7.7]  # CR = 0%
    # weights = [74.7, 13.4, 11.9]  # CR = 0% (num_spaces == distance)
    t = rank.Topsis(decision_matrix, weights, criteria=[False, False, False])

    t.get_rank()

    # print(tunning.AHP_weights_method([5, 7, 5]))

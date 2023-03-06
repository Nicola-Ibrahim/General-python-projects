from . import core, topsis, utils


def run():
    encoded_time_range = utils.get_encoded_spaces_time_range()
    space_combinations = utils.get_encoded_spaces_combinations(encoded_time_range)
    decision_matrix = core.create_decision_matrix(space_combinations)
    weights = core.entropy_weights_method(
        goal_time=102, decision_matrix=decision_matrix
    )
    # weights = [0.2, 0.1, 0.7]
    print(weights)
    t = topsis.Topsis(decision_matrix, weights, criteria=[False, False, False])

    print(t.get_rank())

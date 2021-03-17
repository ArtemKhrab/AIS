from Puzzle import Puzzle
from sys import maxsize
import time


def recursive_best_first_search(initial_state):
    node = RBFS_search(Puzzle(state=initial_state, parent=None, action=None, path_cost=0, needs_hueristic=True),
                       f_limit=maxsize)

    return node[0].find_solution(), node[1]


def RBFS_search(node, f_limit):
    global result
    successors = []
    if node.goal_test():
        return node, None
    children = node.generate_child()
    if not len(children):
        return None, maxsize
    count = -1
    for child in children:
        count += 1
        successors.append((child.evaluation_function, count, child))
    while len(successors):
        successors.sort()
        best_node = successors[0][2]
        if best_node.evaluation_function > f_limit:
            return None, best_node.evaluation_function
        alternative = successors[1][0]
        result, best_node.evaluation_function = RBFS_search(best_node, min(f_limit, alternative))
        successors[0] = (best_node.evaluation_function, successors[0][1], best_node)
        if result is not None:
            break
    return result, node.h1()


if __name__ == '__main__':
    states = [[1, 3, 4, 8, 6, 2, 7, 0, 5], [2, 8, 1, 0, 4, 3, 7, 6, 5], [2, 8, 1, 4, 6, 3, 0, 7, 5]]

    for state in states:
        Puzzle.num_of_instances = 0
        t0 = time.time()
        RBFS = recursive_best_first_search(state)
        t1 = time.time() - t0
        print('RBFS:', RBFS[0])
        print("H1:", RBFS[1])
        print('space:', Puzzle.num_of_instances)
        print('time:', t1)

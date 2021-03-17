from Puzzle import Puzzle
from sys import maxsize
import time
from queue import Queue
from tabulate import tabulate


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


def breadth_first_search(initial_state):
    start_node = Puzzle(initial_state, None, None, 0)
    h1 = start_node.h1()
    if start_node.goal_test():
        return start_node.find_solution(), h1
    q = Queue()
    q.put(start_node)
    explored = []
    while not(q.empty()):
        node = q.get()
        print(q.qsize())
        explored.append(node.state)
        children = node.generate_child()
        for child in children:
            if child.state not in explored:
                if child.goal_test():
                    return child.find_solution(), h1
                q.put(child)
    return


def iterative_deep_search(initial_state, depth_limit):
    depth = 0
    node = Puzzle(initial_state, None, None, 0)
    h1 = node.h1()
    if node.goal_test():
        return node.find_solution(), h1
    queue = [[node, depth]]
    explored = []
    del node
    while not(queue.__len__() == 0):
        node, depth = queue.pop(0)
        explored.append(node.state)
        children = node.generate_child()
        depth += 1
        for i, child in enumerate(children):
            if child.state not in explored and depth < depth_limit:
                if child.goal_test():
                    return child.find_solution(), h1
                queue.insert(i, [child, depth])

    return


if __name__ == '__main__':
    states_str = ["1, 3, 4, 8, 6, 2, 7, 0, 5", "2, 8, 1, 0, 4, 3, 7, 6, 5", "2, 8, 1, 4, 6, 3, 0, 7, 5"]
    states = [[1, 3, 4, 8, 6, 2, 7, 0, 5], [2, 8, 1, 0, 4, 3, 7, 6, 5], [2, 8, 1, 4, 6, 3, 0, 7, 5]]
    results = []

    for state, start_state_str in zip(states, states_str):

        Puzzle.num_of_instances = 0
        t0 = time.time()
        rbfs = recursive_best_first_search(state)
        t1 = time.time() - t0
        results.append(["RBFS", rbfs[1], start_state_str, "1, 2, 3, 8, 0, 4, 7, 6, 5",
                        t1, Puzzle.num_of_instances, rbfs[0]])
        del t1

        # Puzzle.num_of_instances = 0
        # t0 = time.time()
        # bfs = breadth_first_search(state)
        # t1 = time.time() - t0
        # results.append(["BFS", bfs[1], t1, Puzzle.num_of_instances])
        # del t1

        Puzzle.num_of_instances = 0
        t0 = time.time()
        ids = iterative_deep_search(state, 25)
        t1 = time.time() - t0
        if ids is not None:
            results.append(["IDS", ids[1], start_state_str, "1, 2, 3, 8, 0, 4, 7, 6, 5",
                            t1, Puzzle.num_of_instances, ids[0]])
        else:
            results.append(["IDS", "Not Found", start_state_str, "1, 2, 3, 8, 0, 4, 7, 6, 5",
                            t1, Puzzle.num_of_instances, ""])
        del t1

    print(tabulate(results, headers=["Alg", "H1", "Input State", "Goal State", "Time", "Nodes", "Moves"]))

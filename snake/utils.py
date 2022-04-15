from abc import ABCMeta, abstractmethod


class AStarNode:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self.h = 0  # heuristic cost from this node to the final node
        self.g = 0  # cost form the beginning to this node
        self.f = self.g + self.h
        self.cost_from_parent = 0  # cost from parent node to this node

    @abstractmethod
    def heuristic(self, goal_node) -> float:
        pass

    @abstractmethod
    def get_successors(self) -> list:
        pass


class AStar:
    def __init__(self) -> None:
        self._open_nodes = list()
        self._closed_nodes = list()
        self._start_node = None
        self._goal_node = None

    def set_starting_node(self, node: AStarNode) -> None:
        if len(self._open_nodes) > 0:
            raise("Trying to set the starting node when the Open List is not empty")

        self._start_node = node
        self._open_nodes.append(node)

    def find(self, goal_node: AStarNode) -> bool:
        while len(self._open_nodes) > 0:
            # find the node with the least f in the open node list
            minimum_open_node = self._open_nodes[0]
            for each_open_node in self._open_nodes:
                if each_open_node.f < minimum_open_node.f:
                    minimum_open_node = each_open_node

            # remove this from the open node list
            self._open_nodes.remove(minimum_open_node)
            self._closed_nodes.append(minimum_open_node)

            # generate select nodes successors
            successors_nodes = minimum_open_node.get_successors()

            for each_successor_node in successors_nodes:
                if each_successor_node == goal_node:
                    self._goal_node = each_successor_node  # this node already has the information of the parent
                    return True

                # this successor node is not the goal node
                each_successor_node.g = minimum_open_node.g + each_successor_node.cost_from_parent
                each_successor_node.h = each_successor_node.heuristic(goal_node=goal_node)
                each_successor_node.f = each_successor_node.g + each_successor_node.h

                # if this node is already in the open list with less f, skip it
                already_checked = False
                for each_open_node in self._open_nodes:
                    if each_open_node == each_successor_node and each_open_node.f <= each_successor_node.f:
                        already_checked = True
                        break

                # if this node is in the closed list with less, skip it
                for each_closed_node in self._closed_nodes:
                    # print(f"{each_closed_node} {each_successor_node} {each_closed_node.f} {each_successor_node.f} equallity {each_closed_node == each_successor_node}")
                    if each_closed_node == each_successor_node and each_closed_node.f <= each_successor_node.f:
                        already_checked = True
                        break

                if already_checked is False:
                    # this node is not final but may be a solution node, add it to the open nodes list
                    self._open_nodes.append(each_successor_node)

        print("No solution found.")
        return False

    def backtracking(self) -> list:
        """ Return the solution of nodes """
        nodes = [self._goal_node]
        middle_node = self._goal_node
        while middle_node != self._start_node:
            for each_closed_node in self._closed_nodes:
                if middle_node.parent == each_closed_node:
                    middle_node = each_closed_node
                    nodes.append(each_closed_node)
                    break

        return nodes

"""
Quokka Maze
===========

This file represents the quokka maze, a graph of locations where a quokka is
trying to find a new home.

Please help the quokkas find a path from their current home to their
destination such that they have sufficient food along the way!

*** Assignment Notes ***

This is the main file that will be interacted with during testing.
All functions to implement are marked with a `TODO` comment.

Please implement these methods to help the quokkas find their new home!
"""

from typing import List, Union

from vertex import Vertex


class QuokkaMaze:
    """
    Quokka Maze
    -----------

    This class is the undirected graph class that will contain all the
    information about the locations between the Quokka colony's current home
    and their final destination.

    We _will_ be performing some minor adversarial testing this time, so make
    sure you're performing checks and ensuring that the graph is a valid simple
    graph!

    ===== Functions =====

        * block_edge(u, v) - removes the edge between vertex `u` and vertex `v`
        * fix_edge(u, v) - fixes the edge between vertex `u` and `v`. or adds an
            edge if non-existent
        * find_path(s, t, k) - find a SIMPLE path from veretx `s` to vertex `t`
            such that from any location with food along this simple path we
            reach the next location with food in at most `k` steps
        * exists_path_with_extra_food(s, t, k, x) - returns whether it’s
            possible for the quokkas to make it from s to t along a simple path
            where from any location with food we reach the next location with
            food in at most k steps, by placing food at at most x new locations

    ===== Notes ======

    * We _will_ be adversarially testing, so make sure you check your params!
    * The ordering of vertices in the `vertex.edges` does not matter.
    * You MUST check that `k>=0` and `x>=0` for the respective functions
        * find_path (k must be greater than or equal to 0)
        * exists_path_with_extra_food (k and x must be greater than or equal to
            0)
    * This is an undirected graph, so you don't need to worry about the
        direction of traversing during your path finding.
    * This is a SIMPLE GRAPH, your functions should ensure that it stays that
        way.
    * All vertices in the graph SHOULD BE UNIQUE! IT SHOULD NOT BE POSSIBLE
        TO ADD DUPLICATE VERTICES! (i.e the same vertex instance)
    """

    def __init__(self) -> None:
        """
        Initialises an empty graph with a list of empty vertices.
        """
        self.vertices = []

    def add_vertex(self, v: Vertex) -> bool:
        """
        Adds a vertex to the graph.
        Returns whether the operation was successful or not.

        :param v - The vertex to add to the graph.
        :return true if the vertex was correctly added, else false
        """
        # TODO implement me, please?
        if v is None:
            return False

        find = False
        for i in range(len(self.vertices)):
            if self.vertices[i] == v:
                find = True

        if find is False:
            self.vertices.append(v)
            return True
        else:
            return False

    def fix_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Fixes the edge between two vertices, u and v.
        If an edge already exists, then this operation should return False.

        :param u - A vertex
        :param v - Another vertex
        :return true if the edge was successfully fixed, else false.
        """

        # TODO implement me please.

        if u is None:
            return False
        if v is None:
            return False

        find_u = False
        find_v = False
        vu = None
        vv = None

        for i in range(len(self.vertices)):
            if self.vertices[i] == u:
                find_u = True
                vu = self.vertices[i]
            if self.vertices[i] == v:
                find_v = True
                vv = self.vertices[i]

        if find_v & find_u is True:
            for i in range(len(vu.edges)):
                if vu.edges[i] == vv:
                    return False
            vu.add_edge(vv)
            vv.add_edge(vu)
            return True
        else:
            return False

    def block_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Blocks the edge between two vertices, u and v.
        Removes the edge if it exists.
        If not, it should be unsuccessful.

        :param u - A vertex
        :param v - Another vertex.
        :return true if the edge was successfully removed, else false.
        """

        # TODO implement me, please!
        if u is None:
            return False
        if v is None:
            return False

        if u not in v.edges and v not in u.edges:
            return False
        if u == v:
            return False

        u.rm_edge(v)
        v.rm_edge(u)
        return True

    def find_path(
            self,
            s: Vertex,
            t: Vertex,
            k: int
    ) -> Union[List[Vertex], None]:
        """
        find_path returns a SIMPLE path between `s` and `t` such that from any
        location with food along this path we reach the next location with food
        in at most `k` steps

        :param s - The start vertex for the quokka colony
        :param t - The destination for the quokka colony
        :param k - The maximum number of hops between locations with food, so
        that the colony can survive!
        :returns
            * The list of vertices to form the simple path from `s` to `t`
            satisfying the conditions.
            OR
            * None if no simple path exists that can satisfy the conditions, or
            is invalid.

        Example:
        (* means the vertex has food)
                    *       *
            A---B---C---D---E

            1/ find_path(s=A, t=E, k=2) -> returns: [A, B, C, D, E]

            2/ find_path(s=A, t=E, k=1) -> returns: None
            (because there isn't enough food!)

            3/ find_path(s=A, t=C, k=4) -> returns: [A, B, C]

        """
        # TODO implement me please
        if k < 0:
            return None
        if s == None:
            return None
        if t == None:
            return None

        for v in self.vertices:
            v.visited = False
            v.n_visited = False
            v.count = 0
        queue: List[List[Vertex]] = []
        count: int = 0

        queue.append([s])
        s.visited = True
        s.n_visited = True

        while queue:
            path = queue.pop(0)  # dequeue
            curr = path[-1]
            count = curr.count

            for i in curr.edges:
                if i == t and count < k:
                    path.append(i)
                    return path

            if curr == t:
                return path

            for adjacent in curr.edges:
                if adjacent.visited == False:
                    if adjacent.has_food == True:
                        adjacent.count = 0
                        count = adjacent.count
                    else:
                        adjacent.count = curr.count + 1
                        count = adjacent.count
                    if count < k:
                        new_path = list(path)
                        new_path.append(adjacent)
                        queue.append(new_path)
                        adjacent.visited = True
        return None

    # def dfs_find_path(self, v: Vertex, t: Vertex, count: int, k: int) -> bool:
    #     if count <= k and v == t:
    #         return True
    #     if count == k and v.has_food == False:
    #         return False
    #     if v.has_food == True:
    #         count = 0
    #     for i in v.edges:
    #         if i.n_visited == False:
    #             count += 1
    #             i.n_visited = True
    #             return self.dfs_find_path(i, t, count, k)
    #     return True

    #     if k < 0:
    #         return None
    #
    #     if s is None:
    #         return None
    #     if t is None:
    #         return None
    #
    #     supply = k
    #     res = []
    #     start = None
    #     end = None
    #
    #     for i in range(len(self.vertices)):
    #         self.vertices[i].visited = False
    #
    #     for i in range(len(self.vertices)):
    #         if self.vertices[i] == s:
    #             start = s
    #         if self.vertices[i] == t:
    #             end = t
    #
    #     cur = []
    #
    #     if start and end is not None:
    #         start.visited = True
    #         cur.append(start)
    #         cur = self.dfs(k, supply, cur, start, end)
    #         res = cur
    #
    #     return res
    #
    # def dfs(self, k: int, supply: int, ls: [], v: Vertex, end: Vertex) -> []:
    #     for x in range(len(v.edges)):
    #         if v.edges[x] == end:
    #             ls.append(end)
    #             return ls
    #     if k == 0:
    #         return None
    #     for i in range(len(v.edges)):
    #         if not v.edges[i].visited:
    #             v.edges[i].visited = True
    #             if v.edges[i].has_food:
    #                 k = supply
    #             k = k - 1
    #             ls.append(v.edges[i])
    #             return self.dfs(k, supply, ls, v.edges[i], end)
    #     return None

    def exists_path_with_extra_food(
            self,
            s: Vertex,
            t: Vertex,
            k: int,
            x: int
    ) -> bool:
        """
        Determines whether it is possible for the quokkas to make it from s to
        t along a SIMPLE path where from any location with food we reach the
        next location with food in at most k steps, by placing food at at most
        x new locations.

        :param s - The start vertex for the quokka colony
        :param t - The destination for the quokka colony
        :param k - The maximum number of hops between locations with food, so
        that the colony can survive!
        :param x - The number of extra foods to add.
        :returns
            * True if with x added food we can complete the simple path
            * False otherwise.

        Example:
        (* means the vertex has food)
                            *
            A---B---C---D---E

            1/ exists_with_extra_food(A, E, 2, 0) -> returns: False
                (because we can't get from A to E with k=2 and 0 extra food)

            2/ exists_with_extra_food(A, E, 2, 1) -> returns: True
                (Yes, if we put food on `C` then we can get to E with k=2)

            3/ exists_with_extra_food(A, E, 1, 6) -> returns: True
                (Yes, if we put food on `B`, `C`, `D` then we reach E!)

        """

        # TODO implement me please
        if k < 0:
            return False
        if s == None:
            return False
        if t == None:
            return False

        for v in self.vertices:
            v.visited = False
            v.count = 0
        queue: List[List[Vertex]] = []
        count: int = 0

        s.visited = True
        s.food = x
        queue.append([s])

        while queue:
            path = queue.pop(0)  # dequeue
            curr = path[-1]
            count = curr.count
            x = curr.food
            for i in curr.edges:
                if i == t and count < k:
                    return True
            for adjacent in curr.edges:
                if adjacent.visited == False:
                    adjacent.food = curr.food
                    if adjacent.has_food == True:
                        adjacent.count = 0
                        count = adjacent.count
                    else:
                        adjacent.count = curr.count + 1
                        count = adjacent.count

                    if count >= k and x == 0:
                        break
                    if count >= k and x > 0:
                        adjacent.food -= 1
                        adjacent.count = 0
                        count = 0
                    if count < k:
                        new_path = list(path)
                        new_path.append(adjacent)
                        queue.append(new_path)
                        adjacent.visited = True
        return False
    #     if k < 0:
    #         return False
    #
    #     if s is None:
    #         return False
    #     if t is None:
    #         return False
    #
    #     for i in range(len(self.vertices)):
    #         self.vertices[i].visited = False
    #
    #     food = x
    #     supply = k
    #
    #     start = s
    #     end = t
    #
    #     for i in range(len(self.vertices)):
    #         if self.vertices[i] == s:
    #             start = s
    #         if self.vertices[i] == t:
    #             end = t
    #
    #     if start and end is not None:
    #         start.visited = True
    #         return self.dfs1(k, supply, food, start, end)
    #
    # def dfs1(self, k: int, supply: int, food: int, v: Vertex, end: Vertex) -> bool:
    #     for x in range(len(v.edges)):
    #         if v.edges[x] == end:
    #             return True
    #     if k == 0:
    #         if food != 0:
    #             k = supply
    #             food = food - 1
    #         else:
    #             return False
    #     for i in range(len(v.edges)):
    #         if not v.edges[i].visited:
    #             v.edges[i].visited = True
    #             if v.edges[i].has_food:
    #                 k = supply
    #             k = k - 1
    #             return self.dfs1(k, supply, food, v.edges[i], end)
    #     return False

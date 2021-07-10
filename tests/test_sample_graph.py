import unittest

from vertex import Vertex
from graph import QuokkaMaze


def should_be_equal(got, expected, func, message="Incorrect result returned"):
    """
    Simple Assert Helper Function
    """

    assert expected == got, \
        f"[{func}] MSG: {message} [Expected: {expected}, got: {got}]"


def should_be_true(got, func, message="Incorrect result returned"):
    """
    Simple assert helper
    """

    assert got is not None, \
        f"[{func}] MSG: {message} [Expected True, but got {got}]"

    assert got is True, \
        f"[{func}] MSG: {message} [Expected True, but got {got}]"


def should_be_false(got, func, message="Incorrect result returned"):
    """
    Simple false checker
    """

    assert got is not None, \
        f"[{func}] MSG: {message} [Expected False, but got {got}]"

    assert got is False, \
        f"[{func}] MSG: {message} [Expected False, but got {got}]"


def check_edges(
    u,
    v,
    exists
):
    if exists:
        assert u in v.edges, "Vertex not found in edge list"
        assert v in u.edges, "Vertex not found in edge list"
    else:
        assert u not in v.edges, "Vertex found in edge list when it shouldn't"
        assert v not in u.edges, "Vertex found in edge list when it shouldn't"


def check_path_should_match(
    got,
    expected,
    func="maze.find_path",
    message="Returned incorrect path"
):
    """
    Checks the equality of the path returned.
    """

    # Check length
    assert got is not None, "Returned a `None` response when it shouldn't be."

    should_be_equal(
        len(got),
        len(expected),
        func,
        "Path length did not match expected!"
    )

    # For each vertex, check path matches
    for idx in range(len(expected)):
        should_be_equal(
            got[idx],
            expected[idx],
            func,
            message + f"(index: {idx} failed)"
        )


class TestSampleGraph(unittest.TestCase):

    def test_can_add_vertex(self):
        """
        Can we add a vertex?
        """

        bert_the_vert = Vertex(True)

        m = QuokkaMaze()

        should_be_true(
            m.add_vertex(bert_the_vert),
            "maze.add_vertex",
            "Failed to add valid vertex"
        )

        should_be_equal(
            len(m.vertices),
            1,
            "maze.add_vertex"
        )

        # Can't add the same vertex twice!
        should_be_false(
            m.add_vertex(bert_the_vert),
            "maze.add_vertex",
            "You added a vertex that should not have been added"
        )

        should_be_equal(
            len(m.vertices),
            1,
            "maze.add_vertex"
        )

    def test_can_fix_edge(self):
        """
        Can we add an edge?
        """

        A = Vertex(True)
        C = Vertex(True)
        E = Vertex(True)

        m = QuokkaMaze()

        should_be_true(
            m.add_vertex(C),
            "maze.add_vertex",
            "Failed to add valid vertex"
        )

        should_be_true(
            m.add_vertex(E),
            "maze.add_vertex",
            "Failed to add valid vertex"
        )

        should_be_true(
            m.add_vertex(A),
            "maze.add_vertex",
            "Failed to add valid vertex"
        )

        should_be_true(
            m.fix_edge(A, E),
            "maze.fix_edge"
        )

        should_be_true(
            m.fix_edge(C, E),
            "maze.fix_edge"
        )

        # check the edges
        check_edges(A, E, True)
        check_edges(C, E, True)
        check_edges(A, C, False)

        # now add the edge between A and C
        should_be_true(
            m.fix_edge(A, C),
            "maze.fix_edge"
        )

        check_edges(A, C, True)

    def test_can_block_edge(self):
        """
        Can we block/remove an edge?
        """

        A = Vertex(True)
        B = Vertex(True)
        C = Vertex(True)

        A.name = "A"
        B.name = "B"
        C.name = "C"
        m = QuokkaMaze()

        should_be_true(
            m.add_vertex(C),
            "maze.add_vertex"
        )

        should_be_true(
            m.add_vertex(A),
            "maze.add_vertex"
        )

        should_be_true(
            m.add_vertex(B),
            "maze.add_vertex"
        )

        should_be_true(
            m.fix_edge(A, B),
            "maze.fix_edge"
        )
        should_be_true(
            m.fix_edge(A, C),
            "maze.fix_edge"
        )
        should_be_true(
            m.fix_edge(B, C),
            "maze.fix_edge"
        )

        check_edges(A, B, True)
        check_edges(A, C, True)
        check_edges(C, B, True)

        should_be_true(
            m.block_edge(A, B),
            "maze.fix_edge"
        )
        should_be_true(
            m.block_edge(C, B),
            "maze.fix_edge"
        )

    def test_find_path_comment_example(self):
        """
        Checks that we can find the path as shown in comments.
        """

        #           *         *
        # A -- B -- C -- D -- E

        A = Vertex(False)
        B = Vertex(False)
        C = Vertex(True)
        D = Vertex(False)
        E = Vertex(True)

        m = QuokkaMaze()

        should_be_true(m.add_vertex(A), "maze.add_vertex")
        should_be_true(m.add_vertex(B), "maze.add_vertex")
        should_be_true(m.add_vertex(C), "maze.add_vertex")
        should_be_true(m.add_vertex(D), "maze.add_vertex")
        should_be_true(m.add_vertex(E), "maze.add_vertex")

        should_be_true(m.fix_edge(A, B), "maze.fix_edge")
        should_be_true(m.fix_edge(B, C), "maze.fix_edge")
        should_be_true(m.fix_edge(C, D), "maze.fix_edge")
        should_be_true(m.fix_edge(D, E), "maze.fix_edge")

        # Example 1: find_path A, E, 2 => returns [A, B, C, D, E]

        check_path_should_match(
            m.find_path(A, E, 2),
            [A, B, C, D, E],
        )

        # Example 2 - find path k=1, should return None!

        should_be_true(
            m.find_path(A, E, 1) is None,
            "maze.find_path",
            "Returned not `None` path when no valid path exists"
        )

        # Example 3 - large K
        check_path_should_match(
            m.find_path(A, C, 4),
            [A, B, C],
        )

    def test_find_path(self):
        A = Vertex(False)
        B = Vertex(False)
        C = Vertex(True)
        D = Vertex(False)
        E = Vertex(True)
        F = Vertex(False)

        m = QuokkaMaze()

        should_be_true(m.add_vertex(A), "maze.add_vertex")
        should_be_true(m.add_vertex(B), "maze.add_vertex")
        should_be_true(m.add_vertex(C), "maze.add_vertex")
        should_be_true(m.add_vertex(D), "maze.add_vertex")
        should_be_true(m.add_vertex(E), "maze.add_vertex")
        should_be_true(m.add_vertex(F), "maze.add_vertex")

        should_be_true(m.fix_edge(A, B), "maze.fix_edge")
        should_be_true(m.fix_edge(B, C), "maze.fix_edge")
        should_be_true(m.fix_edge(C, D), "maze.fix_edge")
        should_be_true(m.fix_edge(D, E), "maze.fix_edge")
        should_be_true(m.fix_edge(A, F), "maze.fix_edge")


        check_path_should_match(
            m.find_path(B, E, 2),
            [B, C, D, E],
        )

        # check_path_should_match(
        #     m.find_path(A, F, 1),
        #     [A, F],
        # )



    def test_exists_path_sample_comments(self):
        """
        Checks that the example in the comment can be run.
        """

        #                     *
        # A -- B -- C -- D -- E

        A = Vertex(False)
        B = Vertex(False)
        C = Vertex(False)
        D = Vertex(False)
        E = Vertex(True)

        m = QuokkaMaze()

        should_be_true(m.add_vertex(A), "maze.add_vertex")
        should_be_true(m.add_vertex(B), "maze.add_vertex")
        should_be_true(m.add_vertex(C), "maze.add_vertex")
        should_be_true(m.add_vertex(D), "maze.add_vertex")
        should_be_true(m.add_vertex(E), "maze.add_vertex")

        should_be_true(m.fix_edge(A, B), "maze.fix_edge")
        should_be_true(m.fix_edge(B, C), "maze.fix_edge")
        should_be_true(m.fix_edge(C, D), "maze.fix_edge")
        should_be_true(m.fix_edge(D, E), "maze.fix_edge")

        # Example 1 - A E 2 0
        should_be_false(
            m.exists_path_with_extra_food(A, E, 2, 0),
            "maze.exists_path_with_extra_food",
            "Cannot reach path with extra food, should be false."
        )

        # Example 2 - A E 2 1 -> true
        should_be_true(
            m.exists_path_with_extra_food(A, E, 2, 1),
            "maze.exists_path_with_extra_food",
            "Able reach path with extra added food, should be true."
        )

        # Example 3
        should_be_true(
            m.exists_path_with_extra_food(A, E, 1, 6),
            "maze.exists_path_with_extra_food",
            "Able to reach path with extra added food, should be true."
        )

    def test_exists_path1(self):
        A = Vertex(False)
        B = Vertex(False)
        C = Vertex(False)
        D = Vertex(False)
        E = Vertex(False)
        F = Vertex(False)
        J = Vertex(False)
        I = Vertex(True)
        H = Vertex(False)
        G = Vertex(True)
        A.name = "A"
        B.name = "B"
        E.name = "E"
        G.name = "G"
        C.name = "C"
        D.name = "D"
        F.name = "F"
        J.name = "J"
        I.name = "I"
        H.name = "H"

        m = QuokkaMaze()

        should_be_true(m.add_vertex(A), "maze.add_vertex")
        should_be_true(m.add_vertex(B), "maze.add_vertex")
        should_be_true(m.add_vertex(E), "maze.add_vertex")
        should_be_true(m.add_vertex(G), "maze.add_vertex")
        should_be_true(m.add_vertex(C), "maze.add_vertex")
        should_be_true(m.add_vertex(D), "maze.add_vertex")
        should_be_true(m.add_vertex(H), "maze.add_vertex")
        should_be_true(m.add_vertex(I), "maze.add_vertex")
        should_be_true(m.add_vertex(F), "maze.add_vertex")
        should_be_true(m.add_vertex(J), "maze.add_vertex")

        should_be_true(m.fix_edge(A, B), "maze.fix_edge")
        should_be_true(m.fix_edge(A, G), "maze.fix_edge")
        should_be_true(m.fix_edge(B, C), "maze.fix_edge")
        should_be_true(m.fix_edge(C, D), "maze.fix_edge")
        should_be_true(m.fix_edge(D, E), "maze.fix_edge")
        should_be_true(m.fix_edge(E, F), "maze.fix_edge")
        should_be_true(m.fix_edge(F, J), "maze.fix_edge")
        should_be_true(m.fix_edge(J, I), "maze.fix_edge")
        should_be_true(m.fix_edge(I, H), "maze.fix_edge")
        should_be_true(m.fix_edge(H, G), "maze.fix_edge")

        should_be_false(
            m.exists_path_with_extra_food(A, D, 1, 1),
            "maze.exists_path_with_extra_food",
            "Able to reach path with extra added food, should be false."
        )

    def test_exists_path2(self):
        A = Vertex(False)
        B = Vertex(False)
        E = Vertex(True)
        G = Vertex(False)
        W = Vertex(True)
        Z = Vertex(False)
        H = Vertex(False)
        I = Vertex(False)

        A.name = "A"
        B.name = "B"
        E.name = "E"
        G.name = "G"
        W.name = "W"
        Z.name = "Z"
        H.name = "H"
        I.name = "I"

        m = QuokkaMaze()

        should_be_true(m.add_vertex(A), "maze.add_vertex")
        should_be_true(m.add_vertex(B), "maze.add_vertex")
        should_be_true(m.add_vertex(E), "maze.add_vertex")
        should_be_true(m.add_vertex(G), "maze.add_vertex")
        should_be_true(m.add_vertex(W), "maze.add_vertex")
        should_be_true(m.add_vertex(Z), "maze.add_vertex")
        should_be_true(m.add_vertex(H), "maze.add_vertex")
        should_be_true(m.add_vertex(I), "maze.add_vertex")

        should_be_true(m.fix_edge(A, B), "maze.fix_edge")
        should_be_true(m.fix_edge(B, E), "maze.fix_edge")
        should_be_true(m.fix_edge(E, G), "maze.fix_edge")
        should_be_true(m.fix_edge(G, W), "maze.fix_edge")
        should_be_true(m.fix_edge(W, Z), "maze.fix_edge")
        should_be_true(m.fix_edge(E, H), "maze.fix_edge")
        should_be_true(m.fix_edge(H, I), "maze.fix_edge")

        should_be_false(
            m.exists_path_with_extra_food(Z, I, 1, 0),
            "maze.exists_path_with_extra_food",
            "should be false."
        )

        should_be_false(
            m.exists_path_with_extra_food(Z, I, 1, 1),
            "maze.exists_path_with_extra_food",
            "should be false."
        )

        should_be_true(
            m.exists_path_with_extra_food(Z, I, 1, 2),
            "maze.exists_path_with_extra_food",
            "should be true."
        )

        should_be_true(
            m.exists_path_with_extra_food(A, I, 2, 0),
            "maze.exists_path_with_extra_food",
            "should be true."
        )
        print("---")

        should_be_false(
            m.exists_path_with_extra_food(A, I, 1, 0),
            "maze.exists_path_with_extra_food",
            "should be false."
        )

        should_be_false(
            m.exists_path_with_extra_food(A, I, 1, 1),
            "maze.exists_path_with_extra_food",
            "should be false."
        )

        should_be_true(
            m.exists_path_with_extra_food(A, I, 1, 2),
            "maze.exists_path_with_extra_food",
            "should be true."
        )



from docstring_coverage.main import *


def test_counter():
    a = Counter(1, 1)
    b = Counter(5, 3)
    target = a + b
    expected = Counter(6, 4)

    assert target == expected


def test_coverage():
    a = Coverage()
    a.add(doc_func, Type.FUNCTION)
    a.add(nodoc_func, Type.FUNCTION)

    b = Coverage()
    b.add(doc_func, Type.FUNCTION)

    target = a + b
    target.report()


def doc_func():
    """has doc"""
    pass


def nodoc_func():
    """ """
    pass

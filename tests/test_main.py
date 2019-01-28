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
    counter = target.counters[Type.FUNCTION.name]

    assert counter.all == 3
    assert counter.true == 2


def doc_func():
    """has doc"""
    pass

def nodoc_func():
    """ """
    pass

def test_package_A():
    coverage = walk('tests/sample_project/package_A', 'csv', True)
    assert coverage.counters[Type.FUNCTION.name].all == 1
    assert coverage.counters[Type.FUNCTION.name].true == 1
    assert coverage.counters[Type.MODULE.name].all == 1
    assert coverage.counters[Type.MODULE.name].true == 1
    assert coverage.counters[Type.CLASS.name].all == 0
    assert coverage.counters[Type.CLASS.name].true == 0


def test_package_B():
    print()
    coverage = walk('tests/sample_project/package_B', 'str', True)
    assert coverage.counters[Type.FUNCTION.name].all == 3
    assert coverage.counters[Type.FUNCTION.name].true == 1
    assert coverage.counters[Type.MODULE.name].all == 3
    assert coverage.counters[Type.MODULE.name].true == 0
    assert coverage.counters[Type.CLASS.name].all == 1
    assert coverage.counters[Type.CLASS.name].true == 1

def test_sample_project():
    print()
    coverage = walk('tests/sample_project', 'str', True)
    coverage.report()
    assert coverage.counters[Type.FUNCTION.name].all == 5
    assert coverage.counters[Type.FUNCTION.name].true == 3
    assert coverage.counters[Type.MODULE.name].all == 7
    assert coverage.counters[Type.MODULE.name].true == 3
    assert coverage.counters[Type.CLASS.name].all == 2
    assert coverage.counters[Type.CLASS.name].true == 2


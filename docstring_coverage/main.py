import argparse
import enum
import importlib
import inspect
import pkgutil
import pydoc
import sys


class Type(enum.Enum):
    MODULE = 1
    CLASS = 2
    FUNCTION = 3


class Counter():
    def __init__(self, all=0, true=0):
        self.all = all
        self.true = true

    def __add__(self, other):
        return Counter(all=self.all + other.all,
                       true=self.true + other.true)

    def __repr__(self):
        return '<Counter: {0}/{1}>'.format(self.true, self.all)

    def __eq__(self, other):
        return self.all == other.all and self.true == other.true

    def ratio_str(self):
        ratio = self.ratio()
        if ratio is None:
            return '-'
        return '{0:.2f}%'.format(ratio * 100)

    def ratio(self):
        if self.all < 1:
            return None
        return self.true / self.all

    def add(self, object):
        self.all += 1
        self.true += has_doc(object)


class Coverage():
    def __init__(self, counters=None, name=None):
        if counters is not None:
            self.counters = counters
        else:
            self.counters = {}
            for t in Type.__members__:
                self.counters[t] = Counter()

        self.name = name

    def __add__(self, other):
        """
        :param other(Coverage):
        :return:
            Coverage
        """
        merge = {}

        for t in Type.__members__:
            merge[t] = self.counters[t] + other.counters[t]

        return Coverage(counters=merge)

    def report(self, output='str'):
        for t in Type.__members__:
            counter = self.counters[t]
            if output == 'str':
                print('{0:<10} {1:>3} / {2:>3} {3}'.format(
                    t.lower(), counter.true, counter.all, counter.ratio_str()
                ))
            if output == 'csv':
                print(','.join((self.name, t.lower(),
                                str(counter.true), str(counter.all),
                                counter.ratio_str())))

    def add(self, object, type_):
        """
        :param object(object): 
        :param type_(Type): 
        :return:
            None
        """
        self.counters[type_.name].add(object)


def has_doc(object):
    """
    target object has document or not.

    :param object: module, function,
    :return:
        int: 0 or 1
    """
    if not hasattr(object, '__doc__'):
        raise Exception()
    if object.__doc__ is None:
        return 0
    return int(object.__doc__.strip() != "")


def count_module(object, output, is_all):
    """
    Reference: pydoc.HTMLDoc.docmodule

    :param object(object): module
    :return:
    """
    name = object.__name__  # ignore the passed-in name
    try:
        all = object.__all__
    except AttributeError:
        all = None

    classes, cdict = [], {}
    for key, value in inspect.getmembers(object, inspect.isclass):
        # if __all__ exists, believe it.  Otherwise use old heuristic.
        if (all is not None or
                (inspect.getmodule(value) or object) is object):
            if pydoc.visiblename(key, all, object):
                classes.append((key, value))
                cdict[key] = cdict[value] = '#' + key
    for key, value in classes:
        for base in value.__bases__:
            key, modname = base.__name__, base.__module__
            module = sys.modules.get(modname)
            if modname != name and module and hasattr(module, key):
                if getattr(module, key) is base:
                    if not key in cdict:
                        cdict[key] = cdict[base] = modname + '.html#' + key

    funcs, fdict = [], {}
    for key, value in inspect.getmembers(object, inspect.isroutine):
        # if __all__ exists, believe it.  Otherwise use old heuristic.
        if (all is not None or
                inspect.isbuiltin(value) or inspect.getmodule(value) is object):
            if pydoc.visiblename(key, all, object):
                funcs.append((key, value))
                fdict[key] = '#-' + key
                if inspect.isfunction(value): fdict[value] = fdict[key]

    coverage = Coverage(name=name)

    coverage.add(object, Type.MODULE)
    for _, obj in classes:
        coverage.add(obj, Type.CLASS)

    for _, obj in funcs:
        coverage.add(obj, Type.FUNCTION)

    return coverage


def walk(root_path, output='str', is_all=False):
    sys.path.insert(0, root_path)
    packages = pkgutil.walk_packages([root_path])

    coverages = []
    coverage_sum = Coverage()
    for importer, modname, ispkg in packages:
        print('modname', modname)
        spec = pkgutil._get_spec(importer, modname)

        object = importlib._bootstrap._load(spec)
        counter = count_module(object, output=output, is_all=is_all)

        if (is_all and output == 'str'):
            print('--------')
            print(counter.name)

        if is_all:
            counter.report(output)

        coverages.append(counter)
        coverage_sum += counter

    return coverage_sum


def main(root_path, output, is_all):
    coverage = walk(root_path, output, is_all)
    coverage.report(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path", type=str)
    parser.add_argument("--output", dest='output', default='str', type=str,
                        help="[str,csv]")
    parser.add_argument("--all", dest='all', action='store_true', default=False,
                        help="Print all module coverage")
    parser.add_argument("--ignore", type=list, nargs='*')
    args = parser.parse_args()
    walk(args.project_path, args.output, args.all)

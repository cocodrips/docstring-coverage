import argparse
import importlib
import pkgutil
import sys
import pydoc
import inspect


class Counter():
    def __init__(self,
                 module_all=0, module_true=0,
                 class_all=0, class_true=0,
                 func_all=0, func_true=0):
        self.module_all = module_all
        self.module_true = module_true

        self.class_all = class_all
        self.class_true = class_true

        self.func_all = func_all
        self.func_true = func_true

        self.name = None

    def __add__(self, other):
        """
        :param other(Counter):
        :return:
            Counter
        """
        return Counter(
            module_all=self.module_all + other.module_all,
            module_true=self.module_true + other.module_true,

            class_all=self.class_all + other.class_all,
            class_true=self.class_true + other.class_true,

            func_all=self.func_all + other.func_all,
            func_true=self.func_true + other.func_true,
        )

    def report(self):
        print(f'''
module: {self.module_true} / {self.module_all}
function: {self.func_true} / {self.func_all} 
class: {self.class_true} / {self.class_all} 
        ''')

    def class_(self, object):
        self.class_all += 1
        self.class_true += has_doc(object)

    def func_(self, object):
        self.func_all += 1
        self.func_true += has_doc(object)

    def module_(self, object):
        self.module_all += 1
        self.module_true += has_doc(object)


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


def count_module(object):
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

    print('--------')
    print(name)
    # print('class:', classes)
    # print('function:', funcs)

    cnt = Counter()
    cnt.module_(object)
    for _, obj in classes:
        cnt.class_(obj)

    for _, obj in funcs:
        cnt.func_(obj)
    # cnt.report()
    return cnt


def walk(root_path):
    sys.path.insert(0, root_path)
    packages = pkgutil.walk_packages([root_path])

    counters = []
    counter_sum = Counter()
    for importer, modname, ispkg in packages:
        spec = pkgutil._get_spec(importer, modname)

        object = importlib._bootstrap._load(spec)
        counter = count_module(object)
        counter.report()
        counters.append(counter)
        counter_sum = counter_sum + counter

    counter_sum.report()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path", type=str)
    parser.add_argument("--ignore", type=list, nargs='*')
    args = parser.parse_args()
    walk(args.project_path)

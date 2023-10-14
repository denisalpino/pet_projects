class TreeBuilder:
    """Instances of the TreeBuilder class are reentrant context managers
    that allow you to build a tree-like data structure (tree) step-by-step.
    """

    def __init__(self):
        self.__structure = [[]]

    def __enter__(self):
        self.__structure.append([])

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.__structure[-1]:
            self.__structure[-2].append(self.__structure[-1])
        del self.__structure[-1]

    def add(self, obj):
        """Takes an arbitrary object (leaf) as an argument and adds it to the current node of the tree"""
        self.__structure[-1].append(obj)

    def structure(self):
        """Returns the tree structure in the form of nested lists"""
        return self.__structure[0]
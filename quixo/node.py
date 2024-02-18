from dataclasses import dataclass

from quixo.function import Function
from quixo.value_point import ValuePoint


class Node:
    def __init__(self, id: int, content: Function | ValuePoint):
        self._id = id
        self._is_terminal = True if type(content) is ValuePoint else False
        self._content = content

    def __str__(self):
        return f"Id:{self._id}, {self._content}"

    def __repr__(self):
        return f"<{self._id}, {self._content}>"

    @property
    def id(self) -> int:
        """
        Return id
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """
        Set id
        """
        self._id = id


    @property
    def is_terminal(self) -> bool:
        """
        Return true if node is a value point(leaf)
        """
        return self._is_terminal

    @property
    def is_function(self) -> bool:
        """
        Return true if node is a function node
        """
        return not self._is_terminal

    @property
    def function(self) -> Function:
        """
        Return the function
        """
        assert type(self._content) is Function, f"Requested Function, but found {type(self._content)}"
        return self._content

    @property
    def value_point(self) -> ValuePoint:
        """
        Return the value point
        """
        assert type(self._content) is ValuePoint, f"Requested ValuePoint, but found {type(self._content)}"
        return self._content



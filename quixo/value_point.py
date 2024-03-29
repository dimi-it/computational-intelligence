from typing import Optional, Sequence, Tuple

from quixo.decorator import classproperty


class ValuePoint:
    def __init__(self, value: Optional[Sequence[int]] = None):
        self._value = value
        if not self.is_nil():
            assert len(self._value) == 2, f"Value has len {len(self._value)} instead of 2"
            self._value = tuple(self._value)

    def __str__(self):
        if self.is_nil():
            return "NIL"
        else:
            return f"P{self._value[0]}{self._value[1]}"

    def is_nil(self) -> bool:
        """
        Return true if value point is NIL
        """
        return self._value is None

    @property
    def point(self) -> Tuple[int, int]:
        """
        Return the value point position tuple
        """
        assert not self.is_nil(), "ValuePoint is None"
        return self._value

    @classproperty
    def NIL(cls) -> 'ValuePoint':
        """
        Generate a NIL value point
        """
        return ValuePoint(None)

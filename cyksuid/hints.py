from typing import Callable, Union

Bytes = bytes
StrOrBytes = Union[str, Bytes]
IntOrFloat = Union[int, float]

TimeFunc = Callable[[], IntOrFloat]
RandFunc = Callable[[int], bytes]

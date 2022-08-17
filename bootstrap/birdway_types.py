from abc import ABC, abstractmethod


__all__ = ["Void", "Bool", "Int", "Float", "Str", "File"]


class Type(ABC):
    @abstractmethod
    def is_primitive(self):
        ...

    @abstractmethod
    def is_iterable(self):
        ...

    @abstractmethod
    def is_sliceable(self):
        ...

    @abstractmethod
    def item(self):
        ...

    @abstractmethod
    def sliced(self):
        ...


class Primitive(Type):
    def __eq__(lhs, rhs):
        return type(lhs) == type(rhs)

    def is_primitive(self):
        return True

    def is_iterable(self):
        return False

    def is_sliceable(self):
        return False

    def item(self):
        return None

    def sliced(self):
        return None


class Void(Primitive):
    def __repr__(self):
        return "Void"


class Bool(Primitive):
    def __repr__(self):
        return "Bool"


class Int(Primitive):
    def __repr__(self):
        return "Int"


class Float(Primitive):
    def __repr__(self):
        return "Float"


class Str(Primitive):
    def __repr__(self):
        return "Str"

    def is_iterable(self):
        return True

    def is_sliceable(self):
        return True

    def item(self):
        return Str

    def sliced(self):
        return Str


class File(Primitive):
    def __repr__(self):
        return "File"


class Composite(Type):
    def is_primitive(self):
        return False


class Nullable(Composite):
    def __init__(self, data):
        self.__data = data

    def __repr__(self):
        return f"{str(self.__data)}?"

    def __eq__(lhs, rhs):
        if isinstance(rhs, Nullable):
            return lhs.__data == rhs.__data
        else:
            return False

    @property
    def data(self):
        return self.__data

    def is_iterable(self):
        return self.__data.is_iterable()

    def is_sliceable(self):
        return self.__data.is_sliceable()

    def item(self):
        return self.__data.item()

    def sliced(self):
        return self.__data.sliced()


class Tuple(Composite):
    def __init__(self, *types):
        self.__types = types

    def __eq__(lhs, rhs):
        if isinstance(rhs, Tuple):
            return lhs.__types == rhs.__types
        else:
            return False

    @property
    def types(self):
        return self.__types

    def is_iterable(self):
        return False

    def is_sliceable(self):
        return False

    def item(self):
        return None

    def sliced(self):
        return None


class List(Composite):
    def __init__(self, data):
        self.__data = data

    def __eq__(lhs, rhs):
        if isinstance(rhs, Union):
            return lhs.__data == rhs.__data
        else:
            return False

    @property
    def data(self):
        return self.__data

    def is_iterable(self):
        return True

    def is_sliceable(self):
        return True

    def item(self):
        return self.__data

    def sliced(self):
        return self


class Dictionary(Composite):
    def __init__(self, data, key):
        self.__data = data
        self.__key = key

    def __eq__(lhs, rhs):
        if isinstance(rhs, Union):
            return lhs.__data == rhs.__data and lhs.__key == rhs.__key
        else:
            return False

    @property
    def data(self):
        return self.__data

    @property
    def key(self):
        return self.__key

    def is_iterable(self):
        return True

    def is_sliceable(self):
        return True

    def item(self):
        return self.__key

    def sliced(self):
        return self


class Function(Composite):
    def __init__(self, result, *args):
        self.__result = result
        self.__args = args

    def __eq__(lhs, rhs):
        if isinstance(rhs, Union):
            return lhs.__result == rhs.__result and lhs.__args == rhs.__args
        else:
            return False

    @property
    def result(self):
        return self.__args

    @property
    def args(self):
        return self.__args

    def is_iterable(self):
        return False

    def is_sliceable(self):
        return False

    def item(self):
        return None

    def sliced(self):
        return None


class UserDefined(Type):
    def is_primitive(self):
        return False

    def is_iterable(self):
        return False

    def is_sliceable(self):
        return False

    def item(self):
        return None

    def sliced(self):
        return None


class Enum(UserDefined):
    def __init__(self, values_range):
        self.__range = values_range

    @property
    def range(self):
        return self.__range


class Struct(UserDefined):
    def __init__(self, **fields):
        self.__fields = fields

    @property
    def fields(self):
        return self.__fields

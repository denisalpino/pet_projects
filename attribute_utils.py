from itertools import cycle


class Selfie:
    """Instances of this class remember their previous states and are able
    to recover to the states they were in before. The state of an object
    is understood as a certain set of attributes and corresponding values.
    During its lifetime, an instance of the Selfie class can change its state
    in various ways, such as obtaining new attributes or changing the values
    of existing attributes
    """

    def __init__(self) -> None:
        self._states = {}
        self._counter = cycle()
        self._state = next(self._counter)

    def save_state(self):
        """This method is used to record the current state of the object. It should
        be noted that serialization from the pickle module isn't used because
        the internal implementation of pickle objects takes much more memory
        than regular dictionaries
        """
        self._states |= {self._state: self.__dict__.copy()}
        self._state = next(self._counter)

    def recover_state(self, num):
        """This method returns a new instance of Selfie having the required
        state. If num exceeds the sequence number of the last state,
        the instance with the last state is returned without raising an exception
        """
        instance = Selfie()
        instance.__dict__ = self._states[min(self._state - 1, num)]
        return instance

    def n_states(self):
        return self._state


class ProtectedObject:
    """This class prohibits obtaining and modifying the values of protected
    attributes of its instances, as well as deleting these attributes.
    AttributeError exception is raised when attempting to get or change
    the value of a protected attribute, as well as when attempting to delete
    an attribute
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)

    def __getattribute__(self, name):
        if name.startswith('_'):
            raise AttributeError('Доступ к защищенному атрибуту невозможен')
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            raise AttributeError('Доступ к защищенному атрибуту невозможен')
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name.startswith('_'):
            raise AttributeError('Доступ к защищенному атрибуту невозможен')
        object.__delattr__(self, name)


class FieldTracker:
    """A class whose inheritors get the ability to track the state of certain
    attributes of their instances of the class
    """

    def __init__(self):
        self._values = {
            field: getattr(self, field)
            for field in self.fields
        }

    def base(self, field):
        """Method that takes an attribute name as an argument and returns either
        the current value of this attribute, or the original (specified during
        definition) value of this attribute, if it has been changed
        """
        return self._values[field]

    def has_changed(self, field):
        """Method that takes an attribute name as an argument and returns True
        if the value of this attribute has been changed at least once,
        or False otherwise
        """
        return self._values[field] != getattr(self, field)

    def changed(self):
        """Method that returns a dictionary in which the keys are the names of
        the attributes that changed their values, and the values are their
        original values
        """
        return {
            field: self.base(field)
            for field in self.fields
            if self.has_changed(field)
        }

    def save(self):
        """Method that resets the tracking. After calling the method,
        all attributes are considered to have not changed their values before,
        and their current values are considered as initial values
        """
        for field in self.fields:
            self._values[field] = getattr(self, field)


class Versioned:
    """A class describing a descriptor that provides access to both the current
    attribute value and all previous ones, if the attribute value has ever
    changed. The descriptor is assigned to an attribute that has the same name
    as the variable to which the descriptor is assigned.
    """

    def __set_name__(self, cls, attr):
        self._attr = attr

    def __get__(self, instance, cls):
        if instance is None:
            return self
        if self._attr in instance.__dict__:
            return instance.__dict__[self._attr][-1]
        raise AttributeError('Атрибут не найден')

    def __set__(self, instance, value):
        instance.__dict__.setdefault(self._attr, []).append(value)

    def get_version(self, instance, n):
        """The method returns the nth integer value of the attribute
        of this class instance. For example, if the value of an attribute
        was set and then changed, the get_version() method can return both
        the set value (first-in-time) and the changed value (second-in-time)

        instance - an instance of the class in which the descriptor is defined;
        n - an integer
        """
        return instance.__dict__[self._attr][n - 1]

    def set_version(self, instance, n):
        """The method sets the nth value of the attribute as the current value.
        Calling the set_version() method does not equate to changing the value
        of an attribute. An attribute changes its value only if this operation
        is performed via dot notation or setattr() function.

        instance - an instance of the class in which the descriptor is defined;
        n - an integer
        """
        instance.__dict__[self._attr].append(self.get_version(instance, n))
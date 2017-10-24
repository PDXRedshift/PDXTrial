"""
classes.py
COSC122 Assignment 3 2017

This module provides classes that are to be used to complete the COSC122
Assignment 3. These have many careful restrictions placed on them, but do
provide a sufficient interface to solve the problems given.
"""


from utilities import StatCounter
from abc import ABC, abstractmethod


class Priority(object):
    """ A simple variation on ints so that we can count comparisons.
    """

    def __init__(self, priority):
        self.__priority = priority

    def __repr__(self):
        return repr(self.__priority)

    def __str__(self):
        return str(self.__priority)

    def __eq__(self, other):
        if not isinstance(other, Priority):
            raise ValueError("Priority objects can only be compared "
                             "to other Priority objects")
        StatCounter.inc('comparisons')
        return self.__priority == other.__priority

    def __le__(self, other):
        if not isinstance(other, Priority):
            raise ValueError("Priority objects can only be compared "
                             "to other Priority objects")
        StatCounter.inc('comparisons')
        return self.__priority <= other.__priority

    def __ne__(self, other):
        if other is None:
            StatCounter.inc('comparisons')
            return False
        if not isinstance(other, Priority):
            raise ValueError("Priority objects can only be compared "
                             "to other Priority objects")
        StatCounter.inc('comparisons')
        return self.__priority != other.__priority

    def __lt__(self, other):
        if not isinstance(other, Priority):
            raise ValueError("Priority objects can only be compared "
                             "to other Priority objects")
        StatCounter.inc('comparisons')
        return self.__priority < other.__priority

    def __gt__(self, other):
        if not isinstance(other, Priority):
            raise ValueError("Priority objects can only be compared "
                             "to other Priority objects")
        StatCounter.inc('comparisons')
        return self.__priority > other.__priority

    def __ge__(self, other):
        if not isinstance(other, Priority):
            raise ValueError("Priority objects can only be compared "
                             "to other Priority objects")
        StatCounter.inc('comparisons')
        return self.__priority >= other.__priority

    def __hash__(self):
        StatCounter.inc('hashes')
        return hash(self.__priority)


class Patient(object):

    def __init__(self, name, disease_severity, days_since_diagnosis):
        """ A patient object to hold all the information needed to
            store them in a patient queue.
        """
        self.name = name
        self.disease_severity = disease_severity
        self.days_since_diagnosis = days_since_diagnosis
        self.priority = Priority(self._calc_priority())

    def _calc_priority(self):
        return self.disease_severity * 100 + self.days_since_diagnosis**2

    def __repr__(self):
        return "Patient({}, {})".format(
            self.name, self.priority
        )


class PriorityQueue(ABC):

    @abstractmethod
    def enqueue(self, item):
        pass

    @abstractmethod
    def dequeue(self):
        pass

    def __str__(self):
        return "PQ[{}]".format(", ".join(str(p) for p in self.data))

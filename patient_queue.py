"""
File: patient_queue.py
Author: your name should probably go here

Maintain a patient queue that sorts patients based on the diseases
they have been diagnosed with, and the duration of time since the
diagnosis.
"""

from classes import PriorityQueue, Patient


class PatientHeapQueue(PriorityQueue):
    """ Implement a queue structure using a 0-indexed heap.
        This particular type of queue holds patient information.
    """

    def __init__(self, start_data=None, fast=False):
        """ Create the patient queue.
        """
        if start_data is None:
            start_data = []
        self.comparisons = 0
        self.data = []
        if fast:
            self._fast_heapify(start_data)
        else:
            self._heapify(start_data)

    def _swap(self, i, j):
        """ Swap the patients at positions i and j.
        """
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _parent_index(self, index):
        """ Determine the parent index of the current index.
            For a binary heap that is zero-indexed, this is
            p = (i - 1) // 2
        """
        return (index - 1) // 2

    def _child_indices(self, index):
        """ Calculate the child indices for the current index.
            For a binary heap that is zero-indexed, this is
            c1 = 2*i + 1
            c2 = 2*i + 2
        """
        return [
            2 * index + delta
            for delta in range(1, 2 + 1)
        ]

    def _max_child_priority_index(self, child_indices):
        """ Find the child among the given indices that has the highest priority.
            If an index is not valid, do not consider it. If none are valid, then
            return None. Assumes the child_indices are in order.
        """
        max_index = None
        for index in child_indices:
            if index >= len(self.data):
                break  # No more valid children
            if max_index is None:  # This is the first child, it's valid, so use it
                max_index = index
            else:
                self.comparisons += 1  # Don't worry, we do the comparison counting here
                if self.data[index].priority > self.data[max_index].priority:
                    max_index = index
        return max_index

    def _sift_up(self, index):
        """ Move the patient at the given index into the correct location
            further up in the heap by swapping with its parents if appropriate.
        """
        if index != 0:
            parent_index = self._parent_index(index)
            parent = self.data[parent_index]
            child = self.data[index]
            self.comparisons += 1
            if parent.priority < child.priority:
                self._swap(index, parent_index)
                self._sift_up(parent_index)

    def _sift_down(self, index):
        """ Move the patient at the given index into the correct location
            further down in the heap by swapping with its children if appropriate.
        """
        parent = self.data[index]
        child_indices = self._child_indices(index)
        child_index = self._max_child_priority_index(child_indices)
        if child_index is not None:
            child = self.data[child_index]
            self.comparisons += 1
            if child.priority > parent.priority:
                self._swap(index, child_index)
                self._sift_down(child_index)

    def _heapify(self, data):
        """ Turn the existing data into a heap in O(n log n) time.
        """
        for patient in data:
            self.enqueue(patient)

    def _fast_heapify(self, data):
        """ Turn the existing data into a heap in O(n) time.
        """
        for patient in data:
            assert isinstance(patient, Patient)
            self.data.append(patient)
        for index in range(len(self.data)-1, -1, -1):
            self._sift_down(index)
            

    def enqueue(self, patient):
        """ Add a patient to the queue.
        """
        # We first make sure that we're only including Patients
        assert isinstance(patient, Patient)
        self.data.append(patient)
        self._sift_up(len(self.data)-1)

    def dequeue(self):
        """ Take a patient off the queue and return the Patient object
        """
        first_value = self.data[0]
        if len(self.data) != 1:
            dequeued = self.data.pop()
            self.data[0] = dequeued
            self._sift_down(0)
        else:
            self.data.pop()
        return first_value


class EditablePatientHeapQueue(PatientHeapQueue):
    """ Implement a queue structure using a 0-indexed heap.
        This particular type of queue holds patient information.
        Additionally, we can remove patients not at the top of
        the heap in O(log n) time.
    """

    def __init__(self, start_data=None, fast=False):
        self.indices = {}  # name -> index;
                          # Keep track of where patients are stored
        for (i, person) in enumerate(start_data):
            self.indices[person.name] = i
        super().__init__(start_data, fast)

    def _swap(self, i, j):
        """ Swap patients at index i and j. Don't forget to change
            their position in self.indices as well!
        """
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.indices[self.data[i].name], self.indices[self.data[j].name] = i, j

    def remove(self, patient_name):
        """ Remove the particular patient from the heap. Remember,
            the index will tell you where the patient is in the heap
            and every sub-heap below an index forms a valid heap.
        """
        removed_index = self.indices[patient_name]
        del self.indices[patient_name]
        last_item = self.data[-1]
        if self.data[-1].name != patient_name:
            self.data[removed_index] = last_item
            last_item = self.data.pop()
            self.indices[last_item.name] = removed_index
            super()._sift_up(removed_index)
            super()._sift_down(removed_index)
        else:
            self.data.pop()

    def enqueue(self, patient):
        """ Add a patient to the queue. Let the superclass do
            most of the work.
        """
        assert isinstance(patient, Patient)
        self.indices[patient.name] = len(self.data)
        super().enqueue(patient)
        
    def dequeue(self):
        """ Remove a patient from the front of the queue and return them.
            Again, let the superclass do most of the work.
        """
        if len(self.indices) != 1:
            self.indices[self.data[-1].name] = 0
            del self.indices[self.data[0].name]
        else:
            del self.indices[self.data[0].name]
        dequeued = super().dequeue()
        return dequeued

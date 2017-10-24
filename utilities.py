"""
utilities.py
A collection of useful structures to complete this assignment.
"""

import random
import struct


GENE_LENGTH = 16


class StatCounter(object):
    """ This class is never initialised, it is just used to
        hold some useful information about comparisons.
    """

    __dict = {
        'comparisons': 0,
        'accesses': 0,
        'hashes': 0,
    }

    def __init__(self, *args, **kwargs):
        raise TypeError("The GeneCounter class should never be initialized!")

    @classmethod
    def inc(cls, name):
        cls.__dict[name] += 1

    @classmethod
    def get(cls, name):
        return cls.__dict[name]

    @classmethod
    def set(cls, name, value):
        cls.__dict[name] = value

    @classmethod
    def reset(cls, name):
        cls.__dict[name] = 0


class GeneSequenceGenerator(object):
    """ Generate a sequence of genes
    """

    def __init__(self, max_size=None):
        self.max_size = max_size if max_size is not None else float('inf')

    def __iter__(self):
        from classes import Gene
        i = 0
        while i < self.max_size:
            gene = ''
            for _ in range(GENE_LENGTH):
                gene += random.choice('acgt')
            yield Gene(gene)
            i += 1


def take(sequence, n):
    """ Take the first min(n, len(sequence)) items from sequence. """
    i = 0
    seq = iter(sequence)
    while seq and i < n:
        yield next(seq)
        i += 1


# To use the Gene Sequence Generator:
# >>> from utilities import *
# >>> genes = take(GeneSequenceGenerator(), 10)
# >>> print(list(genes))


def verify_heapness(heap, index=0):
    """ Make sure that the heap invariant is maintained.
    """
    child_indices = heap._child_indices(index)
    valid_child_indices = [i for i in child_indices if i < len(heap.data)]
    if not valid_child_indices:
        return True  # No children, no worries!
    parent_value = heap.data[index]
    for i in valid_child_indices:
        child_value = heap.data[i]
        if child_value.priority > parent_value.priority:
            return False
        verify_heapness(heap, index=i)
    return True


def run_tests(filename, priority_queue, fast=False, verbose=True):
    """ Using the test data in the file described by 'filename', run tests on the
        'priority_queue' class given. E.g.,
            run_tests('TestData/test_data-0-1-0-0.txt', PatientHeapQueue)
    """
    import_data, instructions = read_test_data(filename)
    queue = priority_queue(import_data, fast)
    always_heap_like = True
    for mode, data in instructions:
        if mode == 'enqueue':
            if verbose:
                print("Enqueueing {}".format(data))
            queue.enqueue(data)
        elif mode == 'dequeue':
            result = queue.dequeue()
            if verbose:
                print("Dequeued {}, which is {}".format(
                    result, "right" if result.name == data else "wrong"))
        elif mode == 'remove':
            if verbose:
                print("Removing {}".format(data))
            queue.remove(data)
        if not verify_heapness(queue):
            raise AssertionError("Heap invariant violated!")
    return queue


def read_test_data(filename):
    """ Read in the test data from the file given by filename.
    """
    import_data = []
    instructions = []
    with open(filename) as f:
        n_imports = int(f.readline())
        for _ in range(n_imports):
            line = f.readline().strip()
            import_data.append(create_patient(line))
        for line in f.readlines():
            instruction, information = line.split(maxsplit=1)
            if instruction == 'enqueue':  # Enqueue the patient
                instructions.append(('enqueue', create_patient(information)))
            elif instruction == 'dequeue':  # Dequeue a patient, should assert match with given name
                instructions.append(('dequeue', information.strip()))
            elif instruction == 'remove':  # Remove the named patient
                # information is just a name, not a patient
                instructions.append(('remove', information.strip()))
            else:
                raise NameError("Priority Queue instruction not understood.")
    return import_data, instructions


def create_patient(information):
    """ Create a patient from a line of information.
    """
    from classes import Patient
    name, disease_severity, days_since_diagnosis = information.strip().split(",")
    return Patient(name, int(disease_severity), int(days_since_diagnosis))

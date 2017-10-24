"""
tests.py
A module of unit tests to verify your answers to the
genetic similarity functions.
"""

import unittest
import math

from classes import Priority, Patient
from utilities import StatCounter, read_test_data, run_tests

from patient_queue import PatientHeapQueue, EditablePatientHeapQueue


TEST_FILE_FORMAT = "TestData/test_data-{imports}-{enqueues}-{dequeues}-{removes}.txt"


class HeapAssertions:

    def assertHeap(self, heap, bad_op, index=0):
        """ AssertHeap is an O(n) check that the heap is valid.
        """
        child_indices = heap._child_indices(index)
        valid_child_indices = [i for i in child_indices if i < len(heap.data)]
        if not valid_child_indices:
            return  # No children, no worries!
        parent_value = heap.data[index]
        for i in valid_child_indices:
            child_value = heap.data[i]
            if child_value.priority > parent_value.priority:
                raise AssertionError("Bad heap invariant after '{}':"
                                     "\n\tparent: {}\n\tchild: {}".format(
                                         bad_op, parent_value, child_value
                                     ))
            self.assertHeap(heap, bad_op, index=i)

    def assertIndices(self, heap):
        """ AssertIndices checks that the index dictionary is correct!
        """
        for name, index in heap.indices.items():
            if heap.data[index].name != name:
                raise AssertionError("Index is not pointing to the right place:"
                                     "\n\tExpected {} at index {}, but found {}."
                                     "".format(name, index, heap.data[index].name))


class BaseTestPatientQueue(unittest.TestCase, HeapAssertions):

    def setUp(self):
        """Runs before every test case"""
        for counter in {'comparisons', 'accesses', 'hashes', 'memory'}:
            StatCounter.reset(counter)

    def get_bounds(self, import_size, instructions, fast):
        lower_bound = 0
        upper_bound = 0
        if fast:
            lower_bound += import_size
            upper_bound += 2 * import_size + 1
        else:
            # set O(n log n) importing bounds
            lower_bound += import_size
            upper_bound += int(import_size *
                               (math.log2(import_size + 1))) // 2 + 1
        queue_size = import_size
        op_deltas = {'enqueue': 1, 'dequeue': -1, 'remove': -1}
        op_factors = {'enqueue': 1, 'dequeue': 1.5, 'remove': 1.75}
        for operation, _ in instructions:
            # Update the bounds for an O(log n) operation
            lower_bound += int(math.log2(queue_size) /
                               4) if queue_size > 0 else 0
            upper_bound += int(op_factors[operation]
                               * (math.log2(queue_size + 1))) + 1
            queue_size += op_deltas[operation]
        return lower_bound, upper_bound

    def run_test_file_instructions(self, filename, priority_queue, fast):
        """ Using the test data in the file described by 'filename', run tests on the
            'priority_queue' class given.
        """
        import_data, instructions = read_test_data(filename)
        queue = priority_queue(import_data, fast)
        saved_comps = StatCounter.get('comparisons')
        self.assertHeap(queue, ("fast-" if fast else "") + "heapify")
        StatCounter.set('comparisons', saved_comps)
        for mode, data in instructions:
            if mode == 'enqueue':
                queue.enqueue(data)
                saved_comps = StatCounter.get('comparisons')
                self.assertIn(data, queue.data)
                StatCounter.set('comparisons', saved_comps)
            elif mode == 'dequeue':
                result = queue.dequeue()
                self.assertEqual(data, result.name)
            elif mode == 'remove':
                queue.remove(data)
                saved_comps = StatCounter.get('comparisons')
                self.assertNotIn(data, queue.data)
                StatCounter.set('comparisons', saved_comps)
            saved_comps = StatCounter.get('comparisons')
            self.assertHeap(queue, mode)
            if priority_queue == EditablePatientHeapQueue:
                self.assertIndices(queue)
            StatCounter.set('comparisons', saved_comps)
        return queue

    def heap_test(self, test_file_name):
        """ Test that the heap correctly follows the instructions given in the test file.
        """
        self.run_test_file_instructions(test_file_name)

    def internal_comparisons_test(self, test_file_name):
        """ Test that the student has correctly counted the code against what
            we have counted. This does not mean that the count is correct, just
            that it was correctly counted.
        """
        queue = self.run_test_file_instructions(test_file_name)
        self.assertEqual(queue.comparisons, StatCounter.get('comparisons'))

    def comparisons_test(self, test_file_name):
        """ Test that the number of comparisons that the student made is
            within the expected bounds (provided by self.get_bounds)
        """
        lower_bound, upper_bound = self.get_bounds(
            *read_test_data(test_file_name))
        valid_count_range = range(lower_bound, upper_bound + 1)
        queue = self.run_test_file_instructions(test_file_name)
        self.assertIn(queue.comparisons, valid_count_range)


class TestPatientQueueEnqueue(BaseTestPatientQueue):
    """ Unit tests for enqueueing (which tests sift_up)
    """

    def test_tiny_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, removes=0)
        self.heap_test(test_file)

    def test_tiny_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, removes=0)
        self.internal_comparisons_test(test_file)

    def test_tiny_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, removes=0)
        self.comparisons_test(test_file)

    def test_small_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=0, removes=0)
        self.heap_test(test_file)

    def test_small_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=0, removes=0)
        self.internal_comparisons_test(test_file)

    def test_small_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=0, removes=0)
        self.comparisons_test(test_file)

    def test_medium_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=0, removes=0)
        self.heap_test(test_file)

    def test_medium_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=0, removes=0)
        self.internal_comparisons_test(test_file)

    def test_medium_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=0, removes=0)
        self.comparisons_test(test_file)

    def test_large_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=0, removes=0)
        self.heap_test(test_file)

    def test_large_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=0, removes=0)
        self.internal_comparisons_test(test_file)

    def test_large_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=0, removes=0)
        self.comparisons_test(test_file)

    def test_huge_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=0, removes=0)
        self.heap_test(test_file)

    def test_huge_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=0, removes=0)
        self.internal_comparisons_test(test_file)

    def test_huge_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=0, removes=0)
        self.comparisons_test(test_file)


class TestPatientQueueDequeue(BaseTestPatientQueue):
    """ Unit tests for dequeueing (which tests sift_down)
        This dataset actually tests both up and down, because you need
        to be able to enqueue to have stuff to dequeue!
    """

    def test_tiny_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=1, removes=0)
        self.heap_test(test_file)

    def test_tiny_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=1, removes=0)
        self.internal_comparisons_test(test_file)

    def test_tiny_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=1, removes=0)
        self.comparisons_test(test_file)

    def test_small_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=10, enqueues=10, dequeues=20, removes=0)
        self.heap_test(test_file)

    def test_small_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=10, enqueues=10, dequeues=20, removes=0)
        self.internal_comparisons_test(test_file)

    def test_small_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=10, enqueues=10, dequeues=20, removes=0)
        self.comparisons_test(test_file)

    def test_medium_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=75, removes=0)
        self.heap_test(test_file)

    def test_medium_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=75, removes=0)
        self.internal_comparisons_test(test_file)

    def test_medium_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=75, removes=0)
        self.comparisons_test(test_file)

    def test_large_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, removes=0)
        self.heap_test(test_file)

    def test_large_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, removes=0)
        self.internal_comparisons_test(test_file)

    def test_large_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, removes=0)
        self.comparisons_test(test_file)

    def test_huge_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=1500, removes=0)
        self.heap_test(test_file)

    def test_huge_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=1500, removes=0)
        self.internal_comparisons_test(test_file)

    def test_huge_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=1500, removes=0)
        self.comparisons_test(test_file)


class TestPatientQueueRemove(BaseTestPatientQueue):
    """ Unit tests for removing patients.
        This dataset actually tests everything, because why not.
    """

    def test_tiny_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, removes=1)
        self.heap_test(test_file)

    def test_tiny_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, removes=1)
        self.internal_comparisons_test(test_file)

    def test_tiny_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=1, dequeues=0, removes=1)
        self.comparisons_test(test_file)

    def test_small_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=5, removes=5)
        self.heap_test(test_file)

    def test_small_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=5, removes=5)
        self.internal_comparisons_test(test_file)

    def test_small_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=10, dequeues=5, removes=5)
        self.comparisons_test(test_file)

    def test_medium_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=50, removes=25)
        self.heap_test(test_file)

    def test_medium_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=50, removes=25)
        self.internal_comparisons_test(test_file)

    def test_medium_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=50, removes=25)
        self.comparisons_test(test_file)

    def test_large_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, removes=50)
        self.heap_test(test_file)

    def test_large_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, removes=50)
        self.internal_comparisons_test(test_file)

    def test_large_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150, removes=50)
        self.comparisons_test(test_file)

    def test_huge_remove(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=100, dequeues=1000, removes=100)
        self.heap_test(test_file)

    def test_huge_remove_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=100, dequeues=1000, removes=100)
        self.internal_comparisons_test(test_file)

    def test_huge_remove_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=100, dequeues=1000, removes=100)
        self.comparisons_test(test_file)


class TestTaskOne(TestPatientQueueEnqueue):

    def get_bounds(self, imports, instructions):
        return super().get_bounds(len(imports), instructions, fast=False)

    def run_test_file_instructions(self, filename):
        return super().run_test_file_instructions(filename, PatientHeapQueue, fast=False)


class TestTaskTwo(TestPatientQueueDequeue):

    def get_bounds(self, imports, instructions):
        return super().get_bounds(len(imports), instructions, fast=False)

    def run_test_file_instructions(self, filename):
        return super().run_test_file_instructions(filename, PatientHeapQueue, fast=False)


class TestTaskThree(TestPatientQueueDequeue):

    def get_bounds(self, imports, instructions):
        return super().get_bounds(len(imports), instructions, fast=True)

    def run_test_file_instructions(self, filename):
        return super().run_test_file_instructions(filename, PatientHeapQueue, fast=True)


class TestTaskFour(TestPatientQueueRemove):

    def get_bounds(self, imports, instructions):
        return super().get_bounds(len(imports), instructions, fast=True)

    def run_test_file_instructions(self, filename):
        return super().run_test_file_instructions(filename, EditablePatientHeapQueue, fast=True)


def all_tests_suite():
    suite = unittest.TestSuite()
    #suite.addTest(unittest.makeSuite(TestTaskOne))
    # uncomment the following lines when ready to test further tasks
    #suite.addTest(unittest.makeSuite(TestTaskTwo))
    #suite.addTest(unittest.makeSuite(TestTaskThree))
    suite.addTest(unittest.makeSuite(TestTaskFour))
    return suite


def main():
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(all_tests_suite())

if __name__ == '__main__':
    main()

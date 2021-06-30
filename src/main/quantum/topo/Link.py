"""This class represents a link between two nodes: n1 and n2"""
import numpy as np


class Link:
    count = 0

    # The constructor of the link. Parameters:
    # A given topology topo.
    # Two nodes (n1 and n2), which form the link.
    # The length l of the link.
    # assigned, which is true if there is one qubit at each end of the link.
    # entangled, which is true if the link corresponds to an entanglement, false otherwise.
    # s1 and s2, which are true if the corresponding extrema of the link have been swapped.

    def __init__(self, topo, n1, n2, length, assigned=False, entangled=False, s1=False, s2=False):
        Link.count += 1
        self.id = Link.count
        self.topo = topo,
        self.n1 = n1,
        self.n2 = n2,
        self.length = length,
        self.assigned = assigned,
        self.entangled = entangled,
        self.s1 = s1,
        self.s2 = s2

    # Checks if the given node n corresponds to either n1 or n2
    def contains(self, n):
        return n == self.n1 or n == self.n2

    # Checks if there was a swapping at the end of the link that contains node n.
    def swapped_at(self, n):
        return (n == self.n1 and self.s1) or (n == self.n2 and self.s2)

    # Checks if there was a swapping on the other end of the link that contains node n.
    def swapped_at_the_other_end_of(self, n):
        return (n == self.n1 and self.s2) or (n == self.n2 and self.s1)

    # Checks if either ends of the link have been swapped.
    def swapped(self):
        return self.s1 or self.s2

    # Logical inverse of swapped() function
    def not_swapped(self):
        return not self.swapped(self)

    # Given a node n, returns the node at the other end of the link.
    def the_other_end_of(self, n):
        if n == self.n1:
            return self.n2
        elif n == self.n2:
            return self.n1
        else:
            raise RuntimeError('No such node')

    # Returns the hashcode (id) of the link
    def hashcode(self):
        return self.id

    # Checks if two links are equal, false otherwise
    def equals(self, other):
        return (other is not None) and (type(other) is Link) and (other.id == self.id)

    # Assigns or removes qubits to the extrema of the link depending on the parameter "assign".
    # If assign == True, we assign qubits to the link. If assign == False, we do otherwise.
    def assign_or_remove_qubits(self, assign):
        if self.assigned == assign:
            return
        elif assign:
            self.n1.remaining_qubits -= 1
            self.n2.remaining_qubits -= 1
        else:
            self.n1.remaining_qubits += 1
            self.n2.remaining_qubits += 1
        self.assigned = assign
        assert (self.n1.remaining_qubits >= 0 and self.n1.remaining_qubits == self.n1.n_qubits)
        assert (self.n2.remaining_qubits >= 0 and self.n2.remaining_qubits == self.n2.n_qubits)

    # Assigns qubits to the link 
    def assign_qubits(self):
        if self.assigned:
            return
        self.n1.remaining_qubits -= 1
        self.n2.remaining_qubits -= 1
        self.assigned = True
        assert (self.n1.remaining_qubits >= 0 and self.n1.remaining_qubits == self.n1.n_qubits)
        assert (self.n2.remaining_qubits >= 0 and self.n2.remaining_qubits == self.n2.n_qubits)

    # Tries the execution of an entanglement in the link. First, it calculates the probability p of a successful
    # entanglement, which depends on the length of the channel and the physical parameter alpha. An entanglement is
    # successful if the link has qubits assigned to each end and if the probability p is greater than some uniformly
    # distributed number.
    def try_entanglement(self):
        p = np.exp(-self.topo.alpha * self.length)
        self.entangled = self.assigned and p >= np.random.uniform(0, 1)
        return self.entangled

    # "Deletes" an entanglement in this link.
    def clear_entanglement(self):
        if not self.assigned:
            return
        self.n1.remaining_qubits += 1
        self.n2.remaining_qubits += 1
        self.assigned, self.entangled = False, False
        assert (self.n1.remaining_qubits >= 0 and self.n1.remaining_qubits == self.n1.n_qubits)
        assert (self.n2.remaining_qubits >= 0 and self.n2.remaining_qubits == self.n2.n_qubits)

    # Checks if we can assign qubits to the link
    def assignable(self): return (not self.assigned) and (self.n1.remaining_qubits > 0) and (self.n2.remaining_qubits > 0)

    # To String method
    # To do: Figure out the string manipulation --> Do we need all that information? 
    def to_string(self):
        return str(self.id)

class Order:
    """Pedido: cliente y cantidad de producto."""

    def __init__(self, qtty, customer):
        self._customer = customer
        self._qtty = qtty

    def print(self):
        print(f"     Customer: {self._customer}")
        print(f"     Quantity: {self._qtty}")
        print("     ------------")


class Node:
    """Nodo de la lista enlazada: info (objeto) y next (siguiente nodo)."""

    def __init__(self, info=None):
        self.info = info
        self.next = None


class Queue:
    """Cola FIFO con lista enlazada. top = cabeza, tail = último nodo."""

    def __init__(self):
        self.top = None
        self.tail = None
        self._size = 0

    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def front(self):
        return None if self.is_empty() else self.top.info

    def enqueue(self, info):
        node = Node(info)
        if self.is_empty():
            self.top = node
        else:
            self.tail.next = node
        self.tail = node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        info = self.top.info
        self.top = self.top.next
        self._size -= 1
        if self.top is None:
            self.tail = None
        return info

    def get_nth(self, pos):
        """n-ésimo elemento (1 = primero) sin borrarlo; None si no es válido."""
        if pos < 1 or pos > self._size:
            return None
        node = self.top
        for _ in range(pos - 1):
            node = node.next
        return node.info

    def print_info(self):
        print("********* QUEUE DUMP *********")
        print(f"   Size: {self._size}")
        node, i = self.top, 1
        while node is not None:
            print(f"   ** Element {i}")
            node.info.print()
            node = node.next
            i += 1
        print("******************************")


def main():
    q = Queue()
    q.enqueue(Order(20, "cust1")); q.print_info()
    q.enqueue(Order(30, "cust2")); q.print_info()
    q.enqueue(Order(40, "cust3")); q.print_info()
    q.enqueue(Order(50, "cust3")); q.print_info()

    print("\n>> front():")
    q.front().print()

    print("\n>> get_nth(3):")
    q.get_nth(3).print()
    print(">> get_nth(9) =", q.get_nth(9))

    print("\n>> dequeue():")
    q.dequeue().print()
    q.print_info()
    q.dequeue(); q.dequeue(); q.dequeue()
    q.print_info()


if __name__ == "__main__":
    main()
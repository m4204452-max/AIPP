"""Simple Stack implementation with usage examples."""


class Stack:
    """Iterable-backed LIFO stack with safe access helpers."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Place item on top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item; raise if empty."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek into an empty stack")
        return self._items[-1]

    def is_empty(self):
        """Check whether the stack has no elements."""
        return len(self._items) == 0


def demo_stack():
    stack = Stack()
    print("Pushing 1, 2, 3")
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print("Top element:", stack.peek())
    print("Pop ->", stack.pop())
    print("Pop ->", stack.pop())
    print("Is empty?", stack.is_empty())
    print("Pop ->", stack.pop())
    print("Is empty now?", stack.is_empty())

    print("\nEdge cases:")
    try:
        stack.pop()
    except IndexError as exc:
        print("Pop error:", exc)

    try:
        stack.peek()
    except IndexError as exc:
        print("Peek error:", exc)


if __name__ == "__main__":
    demo_stack()

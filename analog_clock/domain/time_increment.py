class TimeIncrement:
    """
    Node representing a basic increment of time (e.g. 1 second, 1 minute).
    Implements a node for a doubly circular linked list.
    """
    def __init__(self, value: int):
        self.value = value
        
        # Bidirectional pointers
        self.next_increment = None
        self.previous_increment = None

    def __repr__(self):
        return f"TimeIncrement({self.value})"

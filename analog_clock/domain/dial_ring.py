from .time_increment import TimeIncrement

class DialRing:
    """
    Doubly Circular Linked List containing TimeIncrement nodes.
    Represents the dial of a clock (e.g., 60 minutes/seconds, 12 or 24 hours).
    """
    def __init__(self):
        self.active_node = None
        self.size = 0

    def add_increment(self, value: int):
        """Translating insert_at_end logic into domain logic."""
        new_increment = TimeIncrement(value)
        
        if self.active_node is None:
            self.active_node = new_increment
            new_increment.next_increment = self.active_node
            new_increment.previous_increment = self.active_node
        else:
            last_increment = self.active_node.previous_increment
            
            last_increment.next_increment = new_increment
            new_increment.next_increment = self.active_node
            
            new_increment.previous_increment = last_increment
            self.active_node.previous_increment = new_increment
            
        self.size += 1

    def build_ring(self, limit: int):
        """Helper to build a sequence from 0 up to limit - 1."""
        for val in range(limit):
            self.add_increment(val)

    def advance_to_next(self):
        """Moves the state to the next increment."""
        if self.active_node is not None:
            self.active_node = self.active_node.next_increment

    def reverse_to_previous(self):
        """Moves the state to the previous increment."""
        if self.active_node is not None:
            self.active_node = self.active_node.previous_increment

    def get_current_value(self) -> int:
        return self.active_node.value if self.active_node else 0

    def set_current_value(self, value: int):
        """Advances pointer until it finds the requested value."""
        if self.size == 0: return
        start_val = self.get_current_value()
        while self.get_current_value() != value:
            self.advance_to_next()
            if self.get_current_value() == start_val:
                break # Not found to avoid infinite loop

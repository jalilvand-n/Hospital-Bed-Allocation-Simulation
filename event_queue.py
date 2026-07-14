import heapq

class EventQueue:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        heapq.heappush(
            self.events,
            event
        )

    def get_next_event(self):
        return heapq.heappop(
            self.events
        )

    def is_empty(self):
        return len(self.events) == 0

    def __len__(self):
        return len(self.events)
    
    def peek(self):
        if self.events:
            return self.events[0]
        return None
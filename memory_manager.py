import collections

class MemoryManager:
    def __init__(self, total_memory_kb=256, page_size_kb=4):
        self.total_memory = total_memory_kb * 1024  # bytes
        self.page_size = page_size_kb * 1024  # bytes
        self.num_pages = self.total_memory // self.page_size

        self.frames = [None] * self.num_pages

        self.page_queue = collections.deque()  # FIFO
        self.page_usage = {}  # LRU: page_id -> last_access_time
        self.time = 0

        self.page_fault_log = []  # List of fault events

    def allocate_pages(self, container_id, num_pages):
        allocated = []
        for i in range(len(self.frames)):
            if self.frames[i] is None and len(allocated) < num_pages:
                self.frames[i] = (container_id, i)
                allocated.append(i)
            if len(allocated) == num_pages:
                break
        return allocated if len(allocated) == num_pages else None

    def access_page(self, container_id, page_number, algorithm='FIFO'):
        self.time += 1
        page_id = (container_id, page_number)
        if page_id in self.frames:
            if algorithm == 'LRU':
                self.page_usage[page_id] = self.time
            return True
        else:
            self.handle_page_fault(page_id, algorithm)
            return False

    def handle_page_fault(self, page_id, algorithm):
        # Log page fault
        fault_entry = {
            'time': self.time,
            'page_id': page_id,
            'algorithm': algorithm
        }

        # Find space or victim
        if None in self.frames:
            free_index = self.frames.index(None)
            self.frames[free_index] = page_id
        else:
            if algorithm == 'FIFO':
                victim = self.page_queue.popleft()
            elif algorithm == 'LRU':
                victim = min(self.page_usage, key=self.page_usage.get)
            else:
                victim = self.page_queue.popleft()

            victim_index = self.frames.index(victim)
            self.frames[victim_index] = page_id

            if algorithm == 'LRU':
                self.page_usage.pop(victim, None)

        # Record new page
        if algorithm == 'FIFO':
            self.page_queue.append(page_id)
        elif algorithm == 'LRU':
            self.page_usage[page_id] = self.time

        self.page_fault_log.append(fault_entry)

    def free_container_pages(self, container_id):
        for i, frame in enumerate(self.frames):
            if frame is not None and frame[0] == container_id:
                self.frames[i] = None
                if frame in self.page_queue:
                    self.page_queue.remove(frame)
                self.page_usage.pop(frame, None)

    def get_memory_state(self):
        return self.frames

    def get_page_fault_log(self):
        return self.page_fault_log

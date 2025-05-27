import random
import time

class MemoryManager:
    def __init__(self, total_pages=64):
        self.total_pages = total_pages
        self.free_pages = list(range(total_pages))  # free pages tracked here
        self.page_table = {}  # {cid: set(pages)} allocated pages per container
        self.fifo_queue = []  # list of (cid, page) for FIFO replacement
        self.lru_stack = []   # list of (cid, page) for LRU replacement
        self.page_fault_log = []  # log of page faults

    def allocate(self, cid, num_pages):
        if len(self.free_pages) < num_pages:
            return []  # Not enough free pages
        allocated = random.sample(self.free_pages, num_pages)
        for page in allocated:
            self.free_pages.remove(page)
        self.page_table[cid] = set(allocated)
        # Add allocated pages to replacement structures for proper tracking
        for page in allocated:
            self.fifo_queue.append((cid, page))
            self.lru_stack.append((cid, page))
        return allocated

    def deallocate(self, cid):
        if cid in self.page_table:
            for page in self.page_table[cid]:
                self.free_pages.append(page)
            del self.page_table[cid]

        # Remove pages belonging to cid from replacement queues
        self.fifo_queue = [(c, p) for c, p in self.fifo_queue if c != cid]
        self.lru_stack = [(c, p) for c, p in self.lru_stack if c != cid]

    def access_page(self, cid, page, algo='FIFO'):
        if cid not in self.page_table:
            self.page_table[cid] = set()

        if page in self.page_table[cid]:
            # Page hit, update LRU stack if needed
            if algo == 'LRU':
                self.lru_stack = [(c, p) for c, p in self.lru_stack if not (c == cid and p == page)]
                self.lru_stack.append((cid, page))
            return  # No page fault

        # Page fault happened - log it
        self.page_fault_log.append({
            'time': time.strftime("%H:%M:%S"),
            'cid': cid,
            'page': page,
            'algorithm': algo
        })

        if len(self.free_pages) > 0:
            # Assign a free page (we simulate physical memory allocation by picking one)
            assigned_page = self.free_pages.pop(0)
            self.page_table[cid].add(page)
            # Add to replacement queues
            if algo == 'FIFO':
                self.fifo_queue.append((cid, page))
            else:
                self.lru_stack.append((cid, page))
        else:
            # Need to replace a page
            if algo == 'FIFO' and self.fifo_queue:
                victim_cid, victim_page = self.fifo_queue.pop(0)
            elif algo == 'LRU' and self.lru_stack:
                victim_cid, victim_page = self.lru_stack.pop(0)
            else:
                # No pages to replace, just return
                return

            # Remove victim page from its container page table
            if victim_cid in self.page_table:
                self.page_table[victim_cid].discard(victim_page)

            # Add new page to current container
            self.page_table[cid].add(page)

            # Add the new page to replacement queues
            if algo == 'FIFO':
                self.fifo_queue.append((cid, page))
            else:
                self.lru_stack.append((cid, page))

    def get_memory_state(self):
        mem_map = [None] * self.total_pages
        # Map physical pages to container and page info
        for cid, pages in self.page_table.items():
            for p in pages:
                # Here p is the virtual page number; 
                # physical page number mapping is not fully simulated here
                # We'll mark physical page as belonging to cid
                # Since we don't have actual physical page numbers for pages, we map by index
                # For simplicity, assign by iterating the free pages assumption
                # This can be improved with a better data structure
                try:
                    idx = next(i for i in range(len(mem_map)) if mem_map[i] is None)
                except StopIteration:
                    idx = None
                if idx is not None:
                    mem_map[idx] = (cid, p)
        return mem_map

    def get_page_fault_log(self):
        return self.page_fault_log


class Container:
    def __init__(self, cid, mem_kb):
        self.cid = cid
        self.mem_kb = mem_kb
        self.pages = []  # allocated pages (virtual pages)
        self.running = False


class ContainerManager:
    def __init__(self):
        self.containers = {}
        self.next_id = 1
        self.memory_manager = MemoryManager()

    # Changed create_container to accept container_id (matching your Flask code)
    def create_container(self, container_id, mem_kb):
        cid = int(container_id) if str(container_id).isdigit() else self.next_id
        if cid in self.containers:
            return None  # container with this ID exists

        container = Container(cid, mem_kb)
        pages_needed = mem_kb // 4  # 4 KB per page
        allocated = self.memory_manager.allocate(container.cid, pages_needed)
        if allocated:
            container.pages = allocated
            self.containers[container.cid] = container
            # Only increment next_id if user did not specify numeric container_id
            if not str(container_id).isdigit():
                self.next_id += 1
            return container.cid
        return None

    def start_container(self, cid):
        cid = int(cid)
        if cid in self.containers:
            self.containers[cid].running = True

    def stop_container(self, cid):
        cid = int(cid)
        if cid in self.containers:
            self.containers[cid].running = False

    def allocate_memory(self, cid, page, algo='FIFO'):
        cid = int(cid)
        self.memory_manager.access_page(cid, page, algo)

    def terminate_container(self, cid):
        cid = int(cid)
        if cid in self.containers:
            self.memory_manager.deallocate(cid)
            del self.containers[cid]

    def get_memory_state(self):
        return self.memory_manager.get_memory_state()

    def get_page_fault_log(self):
        return self.memory_manager.get_page_fault_log()

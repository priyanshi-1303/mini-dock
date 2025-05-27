import random
import time

class ProcessSimulator:
    def __init__(self, container_manager, container_id, algorithm='FIFO'):
        self.container_manager = container_manager
        self.container_id = container_id
        self.algorithm = algorithm

    def run(self, access_count=20, max_page=None, delay=0.5):
        """
        Simulate the container accessing pages randomly.
        access_count: number of memory accesses
        max_page: max page number to access (default container pages)
        delay: wait time between accesses (seconds)
        """
        if max_page is None:
            container = self.container_manager.containers.get(self.container_id)
            if not container:
                print(f"Container {self.container_id} not found.")
                return
            max_page = container.num_pages
        
        print(f"Process simulator running on container {self.container_id} with {access_count} accesses.")
        
        for _ in range(access_count):
            page = random.randint(0, max_page - 1)
            self.container_manager.container_access_memory(self.container_id, page, self.algorithm)
            time.sleep(delay)

if __name__ == "__main__":
    from container_manager import ContainerManager

    manager = ContainerManager()
    cid = manager.create_container(64)
    manager.start_container(cid)

    simulator = ProcessSimulator(manager, cid, 'LRU')
    simulator.run()

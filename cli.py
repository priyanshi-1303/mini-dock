from container_manager import ContainerManager

def print_help():
    print("""
Commands:
  create <memory_kb>         - Create container with memory in KB (default 64)
  start <container_id>       - Start container
  stop <container_id>        - Stop and delete container
  access <container_id> <page_number> <algorithm> - Access page in container (algorithm: FIFO or LRU)
  mem                       - Show current memory frames
  help                      - Show this help
  exit                      - Exit CLI
""")

def main():
    manager = ContainerManager()
    print("Mini Docker CLI started. Type 'help' for commands.")
    
    while True:
        cmd = input(">> ").strip().split()
        if not cmd:
            continue

        command = cmd[0].lower()

        if command == 'create':
            mem = int(cmd[1]) if len(cmd) > 1 else 64
            cid = manager.create_container(mem)
            print(f"Created container {cid} with {mem} KB memory.")

        elif command == 'start':
            if len(cmd) < 2:
                print("Please provide container ID.")
                continue
            cid = int(cmd[1])
            manager.start_container(cid)

        elif command == 'stop':
            if len(cmd) < 2:
                print("Please provide container ID.")
                continue
            cid = int(cmd[1])
            manager.stop_container(cid)

        elif command == 'access':
            if len(cmd) < 4:
                print("Usage: access <container_id> <page_number> <algorithm>")
                continue
            cid = int(cmd[1])
            page = int(cmd[2])
            algo = cmd[3].upper()
            if algo not in ['FIFO', 'LRU']:
                print("Algorithm must be FIFO or LRU.")
                continue
            manager.container_access_memory(cid, page, algo)

        elif command == 'mem':
            mem_state = manager.get_memory_state()
            print("Memory Frames:")
            for idx, frame in enumerate(mem_state):
                print(f"Frame {idx}: {frame}")

        elif command == 'help':
            print_help()

        elif command == 'exit':
            print("Exiting Mini Docker CLI.")
            break

        else:
            print("Unknown command. Type 'help' for commands.")

if __name__ == "__main__":
    main()

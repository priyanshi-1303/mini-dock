import csv
import json
from datetime import datetime

def log_event(filename, event_dict):
    """
    Append event dictionary as JSON line to log file.
    """
    with open(filename, 'a') as f:
        f.write(json.dumps(event_dict) + '\n')

def export_logs_to_csv(json_log_file, csv_file):
    """
    Convert JSON log lines to CSV.
    """
    with open(json_log_file, 'r') as f:
        logs = [json.loads(line) for line in f]

    if not logs:
        print("No logs to export.")
        return

    keys = logs[0].keys()
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(logs)

def visualize_memory(frames):
    """
    Simple text visualization of memory frames.
    """
    print("Memory Visualization:")
    for idx, frame in enumerate(frames):
        if frame is None:
            status = "Free"
        else:
            status = f"C{frame[0]}_P{frame[1]}"
        print(f"[{idx}]: {status}", end='  ')
        if (idx + 1) % 8 == 0:
            print()
    print()

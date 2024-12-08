class Process:
    def __init__(self, process_id, arrival_time, burst_time, priority=None):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time

def add_process(processes, process_id, arrival_time, burst_time, priority=None):
    process = Process(process_id, arrival_time, burst_time, priority)
    processes.append(process)
    return process_id + 1

def display_processes(processes):
    print("Process ID | Arrival Time | Burst Time | Priority")
    for process in processes:
        print(f"P{process.process_id:8} | {process.arrival_time:12} | {process.burst_time:10} | {process.priority if process.priority is not None else '-'}")

def calculate_metrics(processes, timeline):
    total_wt, total_tat = 0, 0
    print("\nMetrics:")
    print("Process | Arrival Time | Burst Time | Completion Time | Waiting Time | Turn Around Time")

    for process in processes:
        events = [event for event in timeline if event['process_id'] == process.process_id]
        completion_time = events[-1]['end']
        turn_around_time = completion_time - process.arrival_time
        waiting_time = turn_around_time - process.burst_time

        total_tat += turn_around_time
        total_wt += waiting_time

        print(f"P{process.process_id:6} | {process.arrival_time:12} | {process.burst_time:10} | {completion_time:15} | {waiting_time:12} | {turn_around_time:16}")

    avg_wt = total_wt / len(processes)
    avg_tat = total_tat / len(processes)
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turn Around Time: {avg_tat:.2f}")

def round_robin(processes, time_quantum):
    timeline = []
    time = 0
    while any(process.remaining_time > 0 for process in processes):
        for process in processes:
            if process.remaining_time > 0:
                execution_time = min(time_quantum, process.remaining_time)
                timeline.append({'process_id': process.process_id, 'start': time, 'end': time + execution_time})
                process.remaining_time -= execution_time
                time += execution_time
    calculate_metrics(processes, timeline)

def priority_scheduling(processes):
    sorted_processes = sorted(processes, key=lambda p: p.priority if p.priority is not None else float('inf'))
    timeline = []
    time = 0
    for process in sorted_processes:
        timeline.append({'process_id': process.process_id, 'start': time, 'end': time + process.burst_time})
        time += process.burst_time
    calculate_metrics(processes, timeline)

def main():
    processes = []
    process_counter = 1

    while True:
        print("\n1. Add Process")
        print("2. Display Processes")
        print("3. Run Round Robin Scheduling")
        print("4. Run Priority Scheduling")
        print("5. Exit")

        choice = int(input("Choose an option: "))

        if choice == 1:
            arrival_time = int(input("Enter Arrival Time: "))
            burst_time = int(input("Enter Burst Time: "))
            priority = input("Enter Priority (leave blank if not applicable): ")
            priority = int(priority) if priority else None
            process_counter = add_process(processes, process_counter, arrival_time, burst_time, priority)
        elif choice == 2:
            display_processes(processes)
        elif choice == 3:
            time_quantum = int(input("Enter Time Quantum: "))
            round_robin(processes, time_quantum)
        elif choice == 4:
            priority_scheduling(processes)
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt

def simulate_scheduling(algorithm, num_cores, total_time, tasks):
    ready_queue = []
    completed_jobs = 0
    deadline_misses = 0
    busy_cycles = 0
    schedule = {i: [] for i in range(num_cores)}

    for current_time in range(total_time):
        for task in tasks:
            if current_time % task[2] == 0:
                ready_queue.append([task[0], task[1], current_time + task[3], task[2], task[3]])

        next_queue = []
        for job in ready_queue:
            if current_time == job[2] and job[1] > 0:
                deadline_misses += 1
            elif job[1] > 0:
                next_queue.append(job)
        ready_queue = next_queue

        if algorithm == 'RM':
            ready_queue.sort(key=lambda x: (x[3], x[0]))
        elif algorithm == 'DM':
            ready_queue.sort(key=lambda x: (x[4], x[0]))
        elif algorithm == 'EDF':
            ready_queue.sort(key=lambda x: (x[2], x[0]))

        queue_index = 0
        for core in range(num_cores):
            if queue_index < len(ready_queue):
                current_job = ready_queue[queue_index]
                schedule[core].append(current_job[0])
                current_job[1] -= 1
                busy_cycles += 1
                if current_job[1] == 0:
                    completed_jobs += 1
                    ready_queue.pop(queue_index)
                else:
                    queue_index += 1
            else:
                schedule[core].append('IDLE')
                
    cpu_utilization = (busy_cycles / (num_cores * total_time)) * 100
    return completed_jobs, deadline_misses, cpu_utilization, schedule

def plot_gantt_chart(algorithm, num_cores, schedule, tasks):
    fig, ax = plt.subplots(figsize=(12, 4))
    task_names = [task[0] for task in tasks]
    color_palette = ['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    colors = {name: color for name, color in zip(task_names, color_palette)}
    
    ax.set_title(f"{algorithm} Scheduling - {num_cores} Core(s)")
    ax.set_ylim(0, num_cores * 10 + 10)
    ax.set_xlim(0, len(schedule[0]))
    ax.set_yticks([5 + i * 10 for i in range(num_cores)])
    ax.set_yticklabels([f"Core {i+1}" for i in range(num_cores)])
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)

    for core in range(num_cores):
        start = 0
        while start < len(schedule[core]):
            value = schedule[core][start]
            end = start
            while end < len(schedule[core]) and schedule[core][end] == value:
                end += 1
            if value != 'IDLE':
                ax.broken_barh([(start, end - start)], (1 + core * 10, 8), facecolors=colors[value], edgecolor='black')
                ax.text(start + (end - start) / 2, 5 + core * 10, value, ha='center', va='center', color='white', fontsize=9)
            start = end
    plt.tight_layout()
    plt.savefig(f"{algorithm}_{num_cores}C.png", dpi=150)
    plt.close()

def main():
    with open('input.txt', 'r') as input_file:
        lines = input_file.read().splitlines()
    total_time, num_cores = map(int, lines[0].split())
    num_tasks = int(lines[1])
    
    tasks = []
    for i in range(num_tasks):
        parts = lines[2 + i].split()
        tasks.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))

    output_text = ""
    for algorithm in ['RM', 'DM', 'EDF']:
        completed, misses, utilization, schedule = simulate_scheduling(algorithm, num_cores, total_time, tasks)
        plot_gantt_chart(algorithm, num_cores, schedule, tasks)
        output_text += f"=========\nAlgorithm: {algorithm}\nCores: {num_cores}\nCompleted Jobs: {completed}\nDeadline Misses: {misses}\nCPU Utilization: {utilization:.2f}%\n"
        for core in range(num_cores):
            output_text += f"Core {core+1} Schedule:\n" + " ".join(schedule[core]) + "\n"
            
    with open('output.txt', 'w') as output_file:
        output_file.write(output_text)

    print("The simulation is done and the outputs have been saved")

if __name__ == '__main__':
    main()
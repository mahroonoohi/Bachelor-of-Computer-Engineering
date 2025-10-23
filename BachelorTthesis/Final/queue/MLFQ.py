def generate_mlfq_latex(processes, time_quantums):
    colors = ['red', 'blue', 'green', 'black', 'cyan']
    num_queues = len(time_quantums)

    latex_code = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{tikz}
\usepackage{longtable}
\usepackage{xcolor}
\begin{document}

\title{MLFQ Queue Process}
\author{}
\date{}
\maketitle

\section*{Process Arrival}
\begin{itemize}
"""

    # Process Arrival
    for i, (arrival_time, burst_time) in enumerate(processes):
        latex_code += f"    \\item Process {i + 1} arrives at time {arrival_time} with burst time {burst_time}\n"

    latex_code += r"""
\end{itemize}

\section*{Queue States}
\subsection*{Process Execution}
"""

    # Sort processes by arrival time
    sorted_processes = sorted(enumerate(processes), key=lambda x: x[1][0])

    current_time = 0
    remaining_burst_times = [burst_time for _, burst_time in processes]
    completion_times = [None] * len(processes)
    start_times = [-1] * len(processes)
    ready_queues = [[] for _ in range(num_queues)]
    arrival_idx = 0
    gantt_chart_steps = []

    while any(rt > 0 for rt in remaining_burst_times):
        # Add all processes that have arrived to the lowest priority queue
        while arrival_idx < len(sorted_processes) and sorted_processes[arrival_idx][1][0] <= current_time:
            process_index = sorted_processes[arrival_idx][0]
            ready_queues[-1].append(process_index)
            arrival_idx += 1

        # Check if all queues are empty
        if any(ready_queues):
            # Display the state of all queues only if any queue is non-empty
            latex_code += f"At time {current_time}, the state of the queues is:\n\n"
            for queue_idx in range(num_queues):
                latex_code += f"Priority Queue {queue_idx + 1}:\n\n"
                latex_code += r"\begin{center}\begin{tikzpicture}"

                for j, q_process_index in enumerate(ready_queues[queue_idx]):
                    color = colors[q_process_index % len(colors)]
                    latex_code += f"\\draw[thick, {color}] ({j * 1.5},0) rectangle ({(j + 1) * 1.5},1) node[pos=.5] {{P{q_process_index + 1}}};"

                latex_code += r"\end{tikzpicture}\end{center}" + "\n\n"

            # Process queues starting from the highest priority
            for queue_idx in range(num_queues - 1, -1, -1):
                if ready_queues[queue_idx]:
                    # Select the first process in the current queue for execution
                    process_index = ready_queues[queue_idx].pop(0)
                    latex_code += f"Process {process_index + 1} is selected for execution from Priority Queue {queue_idx + 1}.\n\n"

                    if remaining_burst_times[process_index] > 0:
                        if start_times[process_index] == -1:
                            start_times[process_index] = max(current_time, sorted_processes[process_index][1][
                                0])  # Correct start time based on arrival

                        time_quantum = time_quantums[queue_idx]
                        actual_burst = min(time_quantum, remaining_burst_times[process_index])
                        start_time = current_time
                        current_time += actual_burst
                        remaining_burst_times[process_index] -= actual_burst

                        if remaining_burst_times[process_index] == 0:
                            completion_times[process_index] = current_time
                        else:
                            if queue_idx > 0:
                                # Move to the higher-priority queue if not finished and not the highest priority queue
                                ready_queues[queue_idx - 1].append(process_index)
                            else:
                                # If it's the highest priority queue, re-queue it at the end
                                ready_queues[queue_idx].append(process_index)

                        gantt_chart_steps.append((process_index + 1, start_time, current_time))

                        # Display the textual Gantt chart after this execution step
                        latex_code += r"""
\subsection*{Gantt Chart after this step}
\begin{center}
\begin{tabular}{|l|l|}
\hline
Process & Execution Interval \\
\hline
"""

                        for p_id, start_time, end_time in gantt_chart_steps:
                            latex_code += f"P{p_id} & [{start_time}, {end_time}) \\\\\n"
                            latex_code += r"\hline" + "\n"

                        latex_code += r"""
\end{tabular}
\end{center}

"""
                    break  # Exit queue processing loop to avoid checking lower priority queues
        else:
            current_time += 1  # Increment time if all queues are empty, but don't show this time step

    latex_code += r"""
\end{document}
"""

    return latex_code


# Example usage
processes = []  # List of (arrival_time, burst_time) tuples
is_invalid = False
while not is_invalid:
    processes_count = int(input("Enter number of processes(between 1 and 8): "))
    if 8 >= processes_count >= 1:
        is_invalid = True
    else:
        print("Please enter a valid number of processes.")

for i in range(processes_count):
    arrival_time = int(input(f"Enter arrival time for process {i + 1} (>=0): "))
    while arrival_time < 0:
        print("Please enter a valid arrival time.")
        arrival_time = int(input(f"Enter arrival time for process {i + 1} (>=0): "))

    burst_time = int(input(f"Enter burst time for process {i + 1} (>=1): "))
    while burst_time < 1:
        print("Please enter a valid burst time.")
        burst_time = int(input(f"Enter burst time for process {i + 1} (>=1): "))

    processes.append((arrival_time, burst_time))

num_queues = int(input("Enter number of priority queues: "))
time_quantums = []
for i in range(num_queues):
    time_quantum = int(input(f"Enter time quantum for queue {i + 1}: "))
    time_quantums.append(time_quantum)

latex_code = generate_mlfq_latex(processes, time_quantums)

# Save to file
with open("mlfq_queue.tex", "w") as f:
    f.write(latex_code)

print("LaTeX code generated and saved to mlfq_queue.tex")

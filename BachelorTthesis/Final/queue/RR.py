def generate_rr_latex(processes, time_quantum):
    colors = ['red', 'blue', 'green', 'black', 'cyan']

    latex_code = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{tikz}
\usepackage{longtable}
\usepackage{xcolor}
\begin{document}

\title{RR Queue Process}
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
    ready_queue = []
    arrival_idx = 0
    gantt_chart_steps = []

    while any(rt > 0 for rt in remaining_burst_times):
        # Add all processes that have arrived to the ready queue
        new_arrivals = []
        while arrival_idx < len(sorted_processes) and sorted_processes[arrival_idx][1][0] <= current_time:
            process_index = sorted_processes[arrival_idx][0]
            new_arrivals.append(process_index)
            arrival_idx += 1

        ready_queue = new_arrivals + ready_queue  # New arrivals are added first

        if ready_queue:
            # Display current queue
            latex_code += f"At time {current_time}, the queue is:\n\n"
            latex_code += r"\begin{center}\begin{tikzpicture}"

            for j, q_process_index in enumerate(ready_queue):
                color = colors[q_process_index % len(colors)]
                latex_code += f"\\draw[thick, {color}] ({j * 1.5},0) rectangle ({(j + 1) * 1.5},1) node[pos=.5] {{P{q_process_index + 1}}};"

            latex_code += r"\end{tikzpicture}\end{center}" + "\n\n"

            # Select the first process in the ready queue for execution
            process_index = ready_queue.pop(0)
            latex_code += f"Process {process_index + 1} is selected for execution.\n\n"

            if remaining_burst_times[process_index] > 0:
                if start_times[process_index] == -1:
                    start_times[process_index] = max(current_time, sorted_processes[process_index][1][
                        0])  # Correct start time based on arrival

                actual_burst = min(time_quantum, remaining_burst_times[process_index])
                start_time = current_time
                current_time += actual_burst
                remaining_burst_times[process_index] -= actual_burst

                if remaining_burst_times[process_index] == 0:
                    completion_times[process_index] = current_time
                else:
                    ready_queue.append(process_index)  # Add the process back to the end of the queue if not finished

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

        else:
            current_time += 1  # Increment time if no process is ready

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

time_quantum = int(input("Enter time quantum: "))

latex_code = generate_rr_latex(processes, time_quantum)

# Save to file
with open("rr_queue.tex", "w") as f:
    f.write(latex_code)

print("LaTeX code generated and saved to rr_queue.tex")

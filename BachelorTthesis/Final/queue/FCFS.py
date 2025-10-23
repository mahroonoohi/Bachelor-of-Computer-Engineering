def generate_fcfs_latex(processes):
    colors = ['red', 'blue', 'green', 'black', 'cyan']

    latex_code = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{tikz}
\usepackage{longtable}
\usepackage{xcolor}
\begin{document}

\title{FCFS Queue Process}
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
\subsection*{Arrival of Processes}
"""

    # Sort processes by arrival time
    sorted_processes = sorted(enumerate(processes), key=lambda x: x[1][0])

    queue = []
    current_time = 0
    for i, (arrival_time, burst_time) in sorted_processes:
        current_time = max(current_time, arrival_time)
        queue.append((i, burst_time))

        latex_code += f"Process {i + 1} arrives at time {arrival_time}:\n\n"
        latex_code += r"\begin{center}\begin{tikzpicture}"

        # Show new process on the left of the queue
        color = colors[i % len(colors)]
        latex_code += f"\\draw[thick, {color}] (-2.5,0) rectangle (-1.25,0.5) node[pos=.5, scale=0.8] {{P{i + 1}}};"

        for j, (process_index, _) in enumerate(queue):
            color = colors[process_index % len(colors)]
            latex_code += f"\\draw[thick, {color}] ({(j + 1) * 1.5},0) rectangle ({(j + 2) * 1.5},1) node[pos=.5] {{P{process_index + 1}}};"

        latex_code += r"\end{tikzpicture}\end{center}" + "\n\n"

    latex_code += r"""
\subsection*{Exit of Processes}
"""

    # Queue State at Exit
    completion_times = []
    current_time = 0
    for i, (process_index, burst_time) in enumerate(queue):
        arrival_time = processes[process_index][0]
        start_time = max(current_time, arrival_time)
        current_time = start_time + burst_time
        completion_times.append(current_time)

        latex_code += f"Process {process_index + 1} exits at time {current_time}:\n\n"
        latex_code += r"\begin{center}\begin{tikzpicture}"

        for j, (remaining_process_index, _) in enumerate(queue[i + 1:]):
            color = colors[remaining_process_index % len(colors)]
            latex_code += f"\\draw[thick, {color}] ({(j + 1) * 1.5},0) rectangle ({(j + 2) * 1.5},1) node[pos=.5] {{P{remaining_process_index + 1}}};"

        # Show exited element on the right of the queue
        color = colors[process_index % len(colors)]
        latex_code += f"\\draw[thick, {color}] ({(len(queue) - i) * 1.5 + 2.5},0) rectangle ({(len(queue) - i + 1) * 1.5 + 2.5},0.5) node[pos=.5, scale=0.8] {{P{process_index + 1}}};"

        if i == len(queue) - 1:
            latex_code += r"\node at (0,0.5) {Empty};"

        latex_code += r"\end{tikzpicture}\end{center}" + "\n\n"

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

latex_code = generate_fcfs_latex(processes)

# Save to file
with open("fcfs_queue.tex", "w") as f:
    f.write(latex_code)

print("LaTeX code generated and saved to fcfs_queue.tex")

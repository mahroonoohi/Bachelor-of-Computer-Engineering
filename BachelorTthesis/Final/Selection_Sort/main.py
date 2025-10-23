def selection_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
            steps.append((list(arr), i, min_idx, j))
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append((list(arr), i, min_idx, -1))  # -1 indicates no comparison
    return steps

def generate_latex(arr, steps, color_key, color_min, color_compared):
    latex_code = """
\\documentclass{article}
\\usepackage[margin=0.5in]{geometry}
\\usepackage{xcolor}
\\usepackage{tikz}
\\usepackage{amsmath}
\\usepackage{ifthen}
\\usetikzlibrary{shapes, arrows.meta, positioning}
\\begin{document}
\\begin{center}
\\Large\\textbf{Selection Sort Step-by-Step}
\\end{center}
\\vspace{1cm}
Sorting array:\\\\
\\begin{center}
"""

    total_width = len(arr) * 1.2

    # Define custom colors
    latex_code += f"\\definecolor{{keycolor}}{{HTML}}{{{color_key.lstrip('#')}}}\n"
    latex_code += f"\\definecolor{{mincolor}}{{HTML}}{{{color_min.lstrip('#')}}}\n"
    latex_code += f"\\definecolor{{compared}}{{HTML}}{{{color_compared.lstrip('#')}}}\n"

    for step, (current_arr, key_idx, min_idx, comp_idx) in enumerate(steps):
        latex_code += "\\begin{tikzpicture}[scale=0.8, every node/.style={font=\\normalsize}]\n"
        latex_code += "\\node[above] at (0, 1.5) {\\textbf{Step %d}};\n" % (step + 1)
        for i, val in enumerate(current_arr):
            if i == key_idx:
                latex_code += f"\\node[draw, fill=keycolor, rectangle, minimum size=1cm, anchor=north] at ({i*1.2 - total_width/2 + 0.6}, 0) {{\\textbf{{{val}}}}};\n"
            elif i == min_idx:
                latex_code += f"\\node[draw, fill=mincolor, rectangle, minimum size=1cm, anchor=north] at ({i*1.2 - total_width/2 + 0.6}, 0) {{\\textbf{{{val}}}}};\n"
            elif i == comp_idx:
                latex_code += f"\\node[draw, fill=compared, rectangle, minimum size=1cm, anchor=north] at ({i*1.2 - total_width/2 + 0.6}, 0) {{\\textbf{{{val}}}}};\n"
            else:
                latex_code += f"\\node[draw, fill=gray!10, rectangle, minimum size=1cm, anchor=north] at ({i*1.2 - total_width/2 + 0.6}, 0) {{\\textbf{{{val}}}}};\n"
        latex_code += "\\end{tikzpicture}\n"
        latex_code += "\\\\[0.5cm]\n"  # Add space between steps

    latex_code += """
\\end{center}
\\end{document}
"""
    return latex_code

n = int(input("Enter the size of the array: "))
arr = []
for i in range(n):
    element = int(input(f"Enter element {i+1}: "))
    arr.append(element)

color_key = input("Enter the color code for key element (e.g., #2a9d8f): ")
color_min = input("Enter the color code for minimum element (e.g., #e76f51): ")
color_compared = input("Enter the color code for compared element (e.g., #e63946): ")

steps = selection_sort(arr)

latex_output = generate_latex(arr, steps, color_key, color_min, color_compared)

file_name = "selection_sort_step_by_step.tex"
with open(file_name, "w") as f:
    f.write(latex_output)

print(f"Selection sort step-by-step LaTeX code written to {file_name}")

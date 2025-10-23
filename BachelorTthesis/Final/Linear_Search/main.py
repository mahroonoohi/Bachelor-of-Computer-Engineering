def linear_search(arr, target):
    steps = []
    for i in range(len(arr)):
        if arr[i] == target:
            steps.append((i, True))
            return i, steps
        else:
            steps.append((i, False))
    return -1, steps

def generate_latex(arr, steps, target, color_found, color_not_found):
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
\\Large\\textbf{Linear Search Step-by-Step}
\\end{center}
\\vspace{1cm}
Searching for \\textbf{""" + str(target) + """} in array:\\\\
\\begin{center}
"""

    total_width = len(arr) * 1.2

    # Define custom colors
    latex_code += f"\\definecolor{{found}}{{HTML}}{{{color_found.lstrip('#')}}}\n"
    latex_code += f"\\definecolor{{notfound}}{{HTML}}{{{color_not_found.lstrip('#')}}}\n"

    for step, (index, found) in enumerate(steps):
        latex_code += "\\begin{tikzpicture}[scale=0.8, every node/.style={font=\\normalsize}]\n"
        latex_code += "\\node[above] at (0, 1.5) {\\textbf{Step %d}};\n" % (step + 1)
        for i, val in enumerate(arr):
            if i == index:
                color = 'found' if found else 'notfound'
                latex_code += f"\\node[draw, fill={color}, rectangle, minimum size=1cm, anchor=north] at ({i*1.2 - total_width/2 + 0.6}, 0) {{\\textbf{{{val}}}}};\n"
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

target = int(input("Enter the target number to search for: "))
color_found = input("Enter the color code for found element (e.g., green or #2a9d8f): ")
color_not_found = input("Enter the color code for not found element (e.g., red or #e63946): ")

index, steps = linear_search(arr, target)

latex_output = generate_latex(arr, steps, target, color_found, color_not_found)

file_name = "linear_search_step_by_step.tex"
with open(file_name, "w") as f:
    f.write(latex_output)

print(f"Linear search step-by-step LaTeX code written to {file_name}")

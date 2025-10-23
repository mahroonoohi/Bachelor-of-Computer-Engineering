class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current
    
    def generate_latex_for_state(self):
        if not self.head:
            return ""
        
        latex_code = ""
        current = self.head
        node_counter = 1
        
        while current:
            latex_code += f"    \\node[list,on chain] (N{node_counter}) {{\\nodepart{{second}} {current.value}}};\n"
            current = current.next
            node_counter += 1
        
        for i in range(node_counter - 2):
            latex_code += f"    \\path[*->] let \\p1 = (N{i+1}.three), \\p2 = (N{i+1}.center) in (\\x1,\\y2) edge [bend left] ($(N{i+2}.one)+(0,0.2)$);\n"
            latex_code += f"    \\path[*->] ($(N{i+2}.one)+(0.1,0.1)$) edge [bend left] ($(N{i+1}.three)+(0,-0.05)$);\n"
        
        return latex_code
    
    def generate_combined_latex(self, steps):
        latex_code = r"\documentclass[10pt,a4paper]{article}" + "\n"
        latex_code += r"\usepackage[T1]{fontenc}" + "\n"
        latex_code += r"\usepackage{tikz}" + "\n"
        latex_code += r"\usepackage[margin=1cm]{geometry}" + "\n"
        latex_code += r"\usetikzlibrary{calc,shapes.multipart,chains,arrows,positioning}" + "\n"
        latex_code += r"\tikzset{list/.style={very thick, rectangle split, rectangle split parts=3, draw, rectangle split horizontal, minimum size=18pt, inner sep=5pt, text=black, rectangle split part fill={blue!20, red!20, blue!20}}, ->, start chain=going right, very thick}" + "\n"
        latex_code += r"\begin{document}" + "\n"
        
        for i, step in enumerate(steps):
            latex_code += f"\\section*{{Step {i + 1}}}\n"
            latex_code += r"\begin{tikzpicture}" + "\n"
            latex_code += step
            latex_code += r"\end{tikzpicture}" + "\n"
        
        latex_code += r"\end{document}"
        
        return latex_code

dll = DoublyLinkedList()
steps = []

try:
    while True:
        value = int(input("Enter a value to append to the doubly linked list (or type 'done' to finish): "))
        dll.append(value)
        steps.append(dll.generate_latex_for_state())
except ValueError:
    pass  # Exit loop when 'done' is typed

combined_latex_code = dll.generate_combined_latex(steps)

with open("doubly_linked_list_steps.tex", "w") as file:
    file.write(combined_latex_code)

print("Step-by-step LaTeX code generated and saved to doubly_linked_list_steps.tex")

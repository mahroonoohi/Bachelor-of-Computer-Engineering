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
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        new_node.prev = current
    
    def insert_at_index(self, index, value):
        if index < 0:
            raise IndexError("Index must be a non-negative integer.")
        
        length = 0
        current = self.head
        while current is not None:
            length += 1
            current = current.next
        
        if index > length:
            raise IndexError(f"Index out of range. Maximum allowable index is {length}")
        
        new_node = Node(value)
        
        if index == 0:
            if self.head:
                new_node.next = self.head
                self.head.prev = new_node
            self.head = new_node
            return
        
        current = self.head
        current_index = 0
        
        while current is not None and current_index < index - 1:
            current = current.next
            current_index += 1
        
        new_node.next = current.next
        new_node.prev = current
        
        if current.next:
            current.next.prev = new_node
        current.next = new_node
    
    def generate_latex_for_state(self):
        if not self.head:
            return ""
        
        latex_code = ""
        current = self.head
        node_counter = 1
        
        # Generate nodes
        while current:
            latex_code += f"    \\node[list,on chain] (N{node_counter}) {{\\nodepart{{second}} {current.value}}};\n"
            current = current.next
            node_counter += 1
        
        # No need to add Null nodes here
        
        # Generate edges
        for i in range(node_counter - 2):
            latex_code += f"    \\path[*->] let \\p1 = (N{i+1}.three), \\p2 = (N{i+1}.center) in (\\x1,\\y2) edge [bend left] ($(N{i+2}.one)+(0,0.2)$);\n"
            latex_code += f"    \\path[*->] ($(N{i+2}.one)+(0.1,0.1)$) edge [bend left] ($(N{i+1}.three)+(0,-0.05)$);\n"
        
        return latex_code
    
    def generate_combined_latex(self, before_code, after_code):
        latex_code = r"\documentclass[10pt,a4paper]{article}" + "\n"
        latex_code += r"\usepackage[T1]{fontenc}" + "\n"
        latex_code += r"\usepackage{tikz}" + "\n"
        latex_code += r"\usepackage[margin=1cm]{geometry}" + "\n"
        latex_code += r"\usetikzlibrary{calc,shapes.multipart,chains,arrows,positioning}" + "\n"
        latex_code += r"\tikzset{list/.style={very thick, rectangle split, rectangle split parts=3, draw, rectangle split horizontal, minimum size=18pt, inner sep=5pt, text=black, rectangle split part fill={blue!20, red!20, blue!20}}, ->, start chain=going right, very thick}" + "\n"
        latex_code += r"\begin{document}" + "\n"
        latex_code += r"\section*{Doubly Linked List Before Insertion}" + "\n"
        latex_code += r"\begin{tikzpicture}" + "\n"
        latex_code += before_code
        latex_code += r"\end{tikzpicture}" + "\n"
        latex_code += r"\section*{Doubly Linked List After Insertion}" + "\n"
        latex_code += r"\begin{tikzpicture}" + "\n"
        latex_code += after_code
        latex_code += r"\end{tikzpicture}" + "\n"
        latex_code += r"\end{document}"
        
        return latex_code

dll = DoublyLinkedList()
dll.append(12)
dll.append(99)
latex_code_before = dll.generate_latex_for_state()

try:
    new_value = int(input("Enter the value of the new node: "))
    index = int(input("Enter the index at which to insert the new node: "))

    dll.insert_at_index(index, new_value)
    
    latex_code_after = dll.generate_latex_for_state()
    combined_latex_code = dll.generate_combined_latex(latex_code_before, latex_code_after)

    with open("doubly_linked_list_combined.tex", "w") as file:
        file.write(combined_latex_code)

    print("Combined LaTeX code generated and saved to doubly_linked_list_combined.tex")
except IndexError as e:
    print(e)

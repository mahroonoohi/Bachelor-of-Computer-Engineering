class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None

class SingleLinkedList:
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
    
    def delete_at_index(self, index):
        if index < 0:
            raise IndexError("Index must be a non-negative integer.")
        
        if self.head is None:
            raise IndexError("Deletion from an empty list is not allowed.")
        
        current = self.head
        
        if index == 0:
            self.head = self.head.next
            return
        
        current_index = 0
        
        while current.next is not None and current_index < index - 1:
            current = current.next
            current_index += 1
        
        if current.next is None:
            raise IndexError(f"Index out of range. Maximum allowable index is {current_index}")
        
        current.next = current.next.next
    
    def delete_by_value(self, value):
        if self.head is None:
            raise ValueError("Deletion from an empty list is not allowed.")
        
        current = self.head
        
        if current.value == value:
            self.head = self.head.next
            return
        
        while current.next is not None and current.next.value != value:
            current = current.next
        
        if current.next is None:
            raise ValueError(f"Value {value} not found in the list.")
        
        current.next = current.next.next
    
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
        
        # Generate edges
        for i in range(1, node_counter - 1):
            latex_code += f"    \\path[*->] let \\p1 = (N{i}.three), \\p2 = (N{i}.center) in (\\x1,\\y2) edge [bend left] ($(N{i+1}.one)+(0.1,0.06)$);\n"
        
        return latex_code
    
    def generate_combined_latex(self, before_code, after_code):
        latex_code = r"\documentclass[10pt,a4paper]{article}" + "\n"
        latex_code += r"\usepackage[T1]{fontenc}" + "\n"
        latex_code += r"\usepackage{tikz}" + "\n"
        latex_code += r"\usepackage[margin=1cm]{geometry}" + "\n"
        latex_code += r"\usetikzlibrary{calc,shapes.multipart,chains,arrows,positioning}" + "\n"
        latex_code += r"\tikzset{list/.style={very thick, rectangle split, rectangle split parts=3, draw, rectangle split horizontal, minimum size=18pt, inner sep=5pt, text=black, rectangle split part fill={blue!20, red!20, green!20}}, ->, start chain=going right, very thick}" + "\n"
        latex_code += r"\begin{document}" + "\n"
        latex_code += r"\section*{Singly Linked List Before Deletion}" + "\n"
        latex_code += r"\begin{tikzpicture}" + "\n"
        latex_code += before_code
        latex_code += r"\end{tikzpicture}" + "\n"
        latex_code += r"\section*{Singly Linked List After Deletion}" + "\n"
        latex_code += r"\begin{tikzpicture}" + "\n"
        latex_code += after_code
        latex_code += r"\end{tikzpicture}" + "\n"
        latex_code += r"\end{document}"
        
        return latex_code

dll = SingleLinkedList()
dll.append(12)
dll.append(99)
dll.append(100)
dll.append(250)
dll.append(120)
dll.append(1)
dll.append(-10)

latex_code_before = dll.generate_latex_for_state()

try:
    operation = input("Enter 'delete_index' to delete a node by index or 'delete_value' to delete a node by value: ").strip().lower()
    
    if operation == 'delete_index':
        index = int(input("Enter the index of the node to delete: "))
        dll.delete_at_index(index)
    elif operation == 'delete_value':
        value = int(input("Enter the value of the node to delete: "))
        dll.delete_by_value(value)
    else:
        raise ValueError("Invalid operation. Please enter 'delete_index' or 'delete_value'.")

    latex_code_after = dll.generate_latex_for_state()
    combined_latex_code = dll.generate_combined_latex(latex_code_before, latex_code_after)

    with open("Single_linked_list_deletion.tex", "w") as file:
        file.write(combined_latex_code)

    print("Combined LaTeX code generated and saved to Single_linked_list_combined.tex")
except (IndexError, ValueError) as e:
    print(e)

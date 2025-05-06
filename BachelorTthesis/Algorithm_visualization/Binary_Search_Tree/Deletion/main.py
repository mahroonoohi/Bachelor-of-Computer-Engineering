class BinaryTreeNode:
    def __init__(self, name, left=None, right=None):
        self.name = name
        self.left = left
        self.right = right

def add_node(root, value):
    if root is None:
        return BinaryTreeNode(value)

    if value < root.name:
        root.left = add_node(root.left, value)
    else:
        root.right = add_node(root.right, value)

    return root

def find_min(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete_node(root, value):
    if root is None:
        return root
    
    if value < root.name:
        root.left = delete_node(root.left, value)
    elif value > root.name:
        root.right = delete_node(root.right, value)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        
        min_larger_node = find_min(root.right)
        root.name = min_larger_node.name
        root.right = delete_node(root.right, min_larger_node.name)
    
    return root

def generate_latex_binary_tree(node, new_node=None, is_step=False, is_root=False):
    if not node:
        return ""

    node_prefix = "\\" if is_root else ""
    color = "purple" if (is_step and node.name == new_node) else "green!30"
    latex_code = f"{node_prefix}node [fill={color}] {{{node.name}}}"

    children = []
    if node.left or node.right:
        if node.left:
            children.append(f"child {{{generate_latex_binary_tree(node.left, new_node, is_step=is_step)}}}")
        else:
            children.append(f"child[fill=none] {{edge from parent[draw=none]}}")
        if node.right:
            children.append(f"child {{{generate_latex_binary_tree(node.right, new_node, is_step=is_step)}}}")
        else:
            children.append(f"child[fill=none] {{edge from parent[draw=none]}}")

    return f"{latex_code} {' '.join(children)}"

def generate_latex_document(root):
    latex_code = r"""
\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{tikz}
\usepackage[margin=1cm]{geometry}
\begin{document}
\section*{Final Binary Search Tree}
This document presents the final binary search tree (BST) after performing a series of node deletions. The BST maintains its properties, where each node has a left child with a smaller value and a right child with a larger value.

% Subsection explaining the deletion algorithm used
\subsection*{Deletion Algorithm}
The following algorithm was used to delete nodes from the binary search tree:
\begin{center}
\begin{tikzpicture}[level distance=15mm, sibling distance=20mm]
    \tikzstyle{every node}=[circle,inner sep=1pt, minimum size=8mm]
    \tikzstyle{level 1}=[sibling distance=40mm]
    \tikzstyle{level 2}=[sibling distance=20mm]
    \tikzstyle{level 3}=[sibling distance=15mm]
    \tikzstyle{level 4}=[sibling distance=10mm]
"""
    latex_code += "    " + generate_latex_binary_tree(root, is_root=True) + ";\n"
    latex_code += r"""
\end{tikzpicture}
\end{center}
\end{document}
"""
    return latex_code

def generate_latex_document_steps(steps):
    latex_code = r"""
\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{tikz}
\usepackage[margin=1cm]{geometry}
\begin{document}
\section*{Step-by-Step Deletion Process in a Binary Search Tree (BST)}
This document presents the step-by-step process of deleting nodes from a Binary Search Tree (BST). Each step includes a visualization of the tree before and after the deletion of a specific node. Nodes are removed according to BST deletion rules, ensuring that the tree's properties are maintained.

\subsection*{Process Overview}
For each deletion operation:
\begin{itemize}
    \item The tree before deletion is shown, with the node to be deleted highlighted in \textcolor{red}{red}.
    \item The tree after deletion is displayed, illustrating the new structure of the BST.
\end{itemize}

"""

    for step in steps:
        before, after = step
        latex_code += r"""
\begin{figure}[h!]
\centering
"""
        latex_code += r"""
\begin{minipage}{0.8\textwidth}
    \centering
    \begin{tikzpicture}[level distance=15mm, sibling distance=20mm]
        \tikzstyle{every node}=[circle,inner sep=1pt, minimum size=8mm]
        \tikzstyle{level 1}=[sibling distance=40mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 2}=[sibling distance=20mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 3}=[sibling distance=15mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 4}=[sibling distance=10mm, set style={{every node}+=[fill=green!30]}]
        """ + before + ";" + r"""
    \end{tikzpicture}
    \caption{Tree before deletion (Node to delete in red)}
\end{minipage}
\vspace{5cm}
"""
        latex_code += r"""
\begin{minipage}{0.8\textwidth}
    \centering
    \begin{tikzpicture}[level distance=15mm, sibling distance=20mm]
        \tikzstyle{every node}=[circle,inner sep=1pt, minimum size=8mm]
        \tikzstyle{level 1}=[sibling distance=40mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 2}=[sibling distance=20mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 3}=[sibling distance=15mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 4}=[sibling distance=10mm, set style={{every node}+=[fill=green!30]}]
        """ + after + ";" + r"""
    \end{tikzpicture}
    \caption{Tree after deletion}
\end{minipage}
\vspace{1cm}
"""
        
        latex_code += r"""
\end{figure}
\newpage
"""

    latex_code += r"""
\end{document}
"""
    return latex_code

def main():
    root = BinaryTreeNode(50)
    root = add_node(root, 30)
    root = add_node(root, 70)
    root = add_node(root, 20)
    root = add_node(root, 40)
    root = add_node(root, 60)
    root = add_node(root, 80)

    steps = []

    method = input("Do you want to see the final tree or the step-by-step representation? (final/steps): ").strip().lower()
    
    while True:
        operation = input("Enter operation (delete) or type 'done' to finish: ").strip().lower()
        if operation == 'done':
            break

        if operation != 'delete':
            print("Invalid operation. Please enter 'delete' or 'done'.")
            continue

        input_value = input("Enter a number: ").strip()

        try:
            value = int(input_value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if operation == 'delete':
            before_state = generate_latex_binary_tree(root, new_node=value, is_step=True, is_root=True)

            root = delete_node(root, value)
            print(f"Node {value} deleted from the BST.")
            
            after_state = generate_latex_binary_tree(root, is_step=False, is_root=True)
            steps.append((before_state, after_state))

    if method == 'final':
        latex_document = generate_latex_document(root)
        filename = "binary_search_tree_final.tex"
    elif method == 'steps':
        latex_document = generate_latex_document_steps(steps)
        filename = "binary_search_tree_deletion_steps.tex"
    else:
        print("Invalid method selected.")
        return
    
    with open(filename, "w") as file:
        file.write(latex_document)

    print(f"LaTeX code has been generated and saved to {filename}")

if __name__ == "__main__":
    main()

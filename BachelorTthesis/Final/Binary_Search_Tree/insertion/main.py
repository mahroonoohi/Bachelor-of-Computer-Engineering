class BinaryTreeNode:
    def __init__(self, name, left=None, right=None):
        self.name = name
        self.left = left
        self.right = right

def insert_into_bst(root, value):
    if root is None:
        return BinaryTreeNode(value)
    if value < root.name:
        root.left = insert_into_bst(root.left, value)
    else:
        root.right = insert_into_bst(root.right, value)
    return root

def add_node(root, value):
    if root is None:
        return BinaryTreeNode(value)

    if value < root.name:
        root.left = add_node(root.left, value)
    else:
        root.right = add_node(root.right, value)

    return root

def generate_latex_binary_tree(node, new_node=None, is_root=False, is_step=False):
    if not node:
        return ""

    node_prefix = "\\" if is_root else ""
    color = "pink" if (is_step and node.name == new_node) else "green!30"
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
This document presents the final binary search tree (BST) generated through a sequence of node insertions. The tree is constructed by adding nodes in accordance with BST properties, where each node has a left child with a smaller value and a right child with a larger value.

\subsection*{Tree Construction Algorithm}
The binary search tree was constructed using the following algorithm:
\begin{enumerate}
    \item \textbf{Initialization:} Start with an empty tree.
    \item \textbf{Insert Root Node:} The first node inserted becomes the root of the tree.
    \item \textbf{Insert Subsequent Nodes:} For each new node:
    \begin{itemize}
        \item Compare the value of the new node with the current node.
        \item If the new node's value is less, move to the left child; if greater, move to the right child.
        \item Repeat the comparison until finding an appropriate empty position.
    \end{itemize}
    \item \textbf{Recursive Insertion:} Continue recursively inserting nodes to maintain the BST properties.
\end{enumerate}

\subsection*{Final Tree Visualization}
The final binary search tree, after all nodes have been inserted, is visualized below:

\begin{center}
\begin{tikzpicture}[level distance=15mm, sibling distance=20mm]
    \tikzstyle{every node}=[circle,inner sep=1pt, minimum size=8mm]
    \tikzstyle{level 1}=[sibling distance=60mm]
    \tikzstyle{level 2}=[sibling distance=20mm]
    \tikzstyle{level 3}=[sibling distance=15mm]
    \tikzstyle{level 4}=[sibling distance=10mm]

% The following code generates the final binary search tree (BST) after all insertions.

""" + "    " + generate_latex_binary_tree(root, is_root=True) + ";\n" + r"""
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

\section*{Step-by-Step Tree Construction}
This document provides a step-by-step view of the binary search tree (BST) construction process. Each step illustrates the tree's state after a new node is inserted.

\subsection*{Algorithm for Tree Construction}
The binary search tree was constructed using the following steps:
\begin{enumerate}
    \item \textbf{Empty Tree Initialization:} Begin with an empty tree.
    \item \textbf{Node Insertion:} For each node insertion:
    \begin{itemize}
        \item Start at the root and compare the new node's value with the current node.
        \item Move left if the new value is smaller, or right if it is larger.
        \item Insert the new node into the first available position that maintains the BST property.
    \end{itemize}
    \item \textbf{Recursive Traversal:} Insert nodes recursively to ensure that each node's left subtree contains values less than the node and the right subtree contains values greater.
\end{enumerate}

\subsection*{Step-by-Step Visualization}
The following figures show the BST after each insertion step. Each step highlights the newly added node in pink to indicate the changes made.

"""
    for i in range(0, len(steps), 3):
        latex_code += r"""
\begin{figure}[h!]
\centering
"""
        for j in range(i, min(i + 3, len(steps))):
            latex_code += r"""
\begin{minipage}{0.8\textwidth}
    \centering
    \begin{tikzpicture}[level distance=15mm, sibling distance=20mm]
        \tikzstyle{every node}=[circle,inner sep=1pt, minimum size=8mm]
        \tikzstyle{level 1}=[sibling distance=60mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 2}=[sibling distance=20mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 3}=[sibling distance=15mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 4}=[sibling distance=10mm, set style={{every node}+=[fill=green!30]}]
        """ + steps[j] + ";" + r"""
    \end{tikzpicture}
    \caption{Step """ + str(j + 1) + r"""}
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
    root = insert_into_bst(root, 30)
    root = insert_into_bst(root, 70)
    root = insert_into_bst(root, 20)
    root = insert_into_bst(root, 40)
    root = insert_into_bst(root, 60)
    root = insert_into_bst(root, 80)

    steps = []
    
    method = input("Do you want to see the final tree or the step-by-step representation? (final/steps): ").strip().lower()
    
    print("Enter numbers to insert into the BST. Type 'done' to finish.")

    while True:
        input_value = input("Enter a number (or type 'done' to finish): ").strip()
        if input_value.lower() == 'done':
            break

        try:
            value = int(input_value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        new_node = value
        root = add_node(root, value)
        print(f"Node {value} added to the BST.")
        
        if method == 'steps':
            latex_code = generate_latex_binary_tree(root, new_node=new_node, is_step=True, is_root=True)
            steps.append(latex_code)

    if method == 'final':
        latex_document = generate_latex_document(root)
        filename = "binary_search_tree_final.tex"
    elif method == 'steps':
        latex_document = generate_latex_document_steps(steps)
        filename = "binary_search_tree_insertion_steps.tex"
    else:
        print("Invalid method selected.")
        return
    
    with open(filename, "w") as file:
        file.write(latex_document)

    print(f"LaTeX code has been generated and saved to {filename}")

if __name__ == "__main__":
    main()

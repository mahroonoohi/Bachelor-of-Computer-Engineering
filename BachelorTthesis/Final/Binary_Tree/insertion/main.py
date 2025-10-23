class BinaryTreeNode:
    def __init__(self, name, left=None, right=None):
        self.name = name
        self.left = left
        self.right = right

def insert_level_order(root, key, steps):
    """Inserts an element into the binary tree in level order."""
    if not root:
        return BinaryTreeNode(key)
    
    queue = [root]
    
    while queue:
        temp = queue.pop(0)
        
        if not temp.left:
            temp.left = BinaryTreeNode(key)
            steps.append(generate_latex_binary_tree(root, is_root=True))
            return root
        else:
            queue.append(temp.left)
        
        if not temp.right:
            temp.right = BinaryTreeNode(key)
            steps.append(generate_latex_binary_tree(root, is_root=True))
            return root
        else:
            queue.append(temp.right)
    
    return root

def generate_latex_binary_tree(node, is_root=False):
    if not node:
        return ""

    node_prefix = "\\" if is_root else ""
    latex_code = f"{node_prefix}node {{{node.name}}}"
    
    children = []
    if node.left or node.right:
        if node.left:
            children.append(f"child {{{generate_latex_binary_tree(node.left)}}}")
        else:
            children.append(f"child[fill=none] {{edge from parent[draw=none]}}")
        if node.right:
            children.append(f"child {{{generate_latex_binary_tree(node.right)}}}")
        else:
            children.append(f"child[fill=none] {{edge from parent[draw=none]}}")
    
    return f"{latex_code} {' '.join(children)}"

def generate_latex_document_steps(steps):
    latex_code = r"""
\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{tikz}
\usepackage[margin=1cm]{geometry}
\begin{document}
\section*{Binary Tree Construction Steps}
This document illustrates the step-by-step construction of a binary tree. Each step shows the tree after the insertion of a new node, demonstrating how the tree evolves over time.

\subsection*{Algorithm Description}
The binary tree is constructed using a level-order insertion method. This means that new nodes are added starting from the top level, filling in from left to right. If a node has a left and right child, the insertion continues to the next level. The process repeats until all nodes are inserted into the tree.

\subsection*{Step-by-Step Visualization}
The following figures represent the state of the binary tree after each insertion step. The captions describe the order of the steps. Nodes are represented by circles, and the connections between them indicate the parent-child relationships.
"""

    for i in range(0, len(steps), 4):
        latex_code += r"""
\begin{figure}[h!]
\centering
"""
        for j in range(i, min(i + 4, len(steps))):
            if j == 0:
                caption_text = "Initial Tree"
            else:
                caption_text = f"Step {j + 1}"

            latex_code += r"""
\begin{minipage}{0.8\textwidth}
    \centering
    \begin{tikzpicture}[level distance=10mm]
        \tikzstyle{every node}=[fill=green!75,circle,inner sep=1pt, minimum size=8mm]
        \tikzstyle{level 1}=[sibling distance=40mm, set style={{every node}+=[fill=green!60]}]
        \tikzstyle{level 2}=[sibling distance=20mm, set style={{every node}+=[fill=green!45]}]
        \tikzstyle{level 3}=[sibling distance=15mm, set style={{every node}+=[fill=green!30]}]
        \tikzstyle{level 4}=[sibling distance=10mm, set style={{every node}+=[fill=green!15]}]
        """ + steps[j] + ";" + r"""
    \end{tikzpicture}
    \caption{""" + caption_text + r"""}
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
    root = BinaryTreeNode("A")
    root.left = BinaryTreeNode("B")
    root.right = BinaryTreeNode("C")
    root.left.left = BinaryTreeNode("D")
    root.left.right = BinaryTreeNode("E")
    root.right.right = BinaryTreeNode("F")

    steps = [generate_latex_binary_tree(root, is_root=True)]
    print("Initial tree created.")

    while True:
        action = input("Do you want to add a node? (yes/no): ").strip().lower()
        if action == 'no':
            break

        if action == 'yes':
            new_value = input("Enter the value for the new node: ").strip()
            root = insert_level_order(root, new_value, steps)
            print(f"Node {new_value} added in level order.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    latex_document = generate_latex_document_steps(steps)
    filename = "binary_tree_insertion_steps.tex"

    with open(filename, "w") as file:
        file.write(latex_document)

    print(f"LaTeX code for binary tree insertion steps has been generated and saved to {filename}")

if __name__ == "__main__":
    main()

class BinarySearchTreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def search_bst(node, target, steps):
    if not node:
        return False

    steps.append(generate_latex_binary_tree(node, target=target, is_root=True))
    
    if node.value == target:
        return True

    if target < node.value:
        return search_bst(node.left, target, steps)
    else:
        return search_bst(node.right, target, steps)

def generate_latex_binary_tree(node, target=None, is_root=False):
    if not node:
        return ""

    node_prefix = "\\" if is_root else ""

    if node.value == target:
        latex_code = f"{node_prefix}node[fill=magenta!60] {{{node.value}}}"
    else:
        latex_code = f"{node_prefix}node {{{node.value}}}"
    
    children = []
    if node.left or node.right:
        if node.left:
            children.append(f"child {{{generate_latex_binary_tree(node.left, target=target)}}}")
        else:
            children.append(f"child[fill=none] {{edge from parent[draw=none]}}")
        if node.right:
            children.append(f"child {{{generate_latex_binary_tree(node.right, target=target)}}}")
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
\section*{Binary Search Tree Search Process}
This document presents the step-by-step search process in a Binary Search Tree (BST). The search operation is visualized for each step, with the target node highlighted in \textcolor{magenta}{magenta} if found. The steps show how the search operation proceeds through the tree based on the BST properties.
"""

    latex_code += r"""
\subsection*{Initial Tree Structure}
The initial structure of the BST before the search begins is shown below:
\begin{figure}[h!]
\centering
\begin{minipage}{0.8\textwidth}
    \centering
    \begin{tikzpicture}[level distance=10mm]
        \tikzstyle{every node}=[fill=green!75,circle,inner sep=1pt, minimum size=8mm]
        \tikzstyle{level 1}=[sibling distance=40mm, set style={{every node}+=[fill=green!60]}]
        \tikzstyle{level 2}=[sibling distance=20mm, set style={{every node}+=[fill=green!45]}]
        """ + steps[0] + ";" + r"""
    \end{tikzpicture}
    \caption{Initial Tree Structure}
\end{minipage}
\vspace{1cm}
\end{figure}
"""

    latex_code += r"""
\newpage
\subsection*{Search Steps}
Each step below represents a node comparison during the search operation. The tree is visualized at each step, and the current node being compared to the target is highlighted. If the target node is found, it is highlighted in \textcolor{magenta}{magenta}.
"""

    for i in range(1, len(steps)):
        latex_code += r"""
\begin{figure}[h!]
\centering
\begin{minipage}{0.8\textwidth}
    \centering
    \begin{tikzpicture}[level distance=10mm]
        \tikzstyle{every node}=[fill=green!75,circle,inner sep=1pt, minimum size=8mm]
        \tikzstyle{level 1}=[sibling distance=40mm, set style={{every node}+=[fill=green!60]}]
        \tikzstyle{level 2}=[sibling distance=20mm, set style={{every node}+=[fill=green!45]}]
        """ + steps[i] + ";" + r"""
    \end{tikzpicture}
    \caption{Step """ + str(i) + r""": Node comparison}
\end{minipage}
\vspace{1cm}
\end{figure}
"""

    latex_code += r"""
\newpage
\end{document}
"""
    return latex_code

def main():
    root = BinarySearchTreeNode(10)
    root.left = BinarySearchTreeNode(5)
    root.right = BinarySearchTreeNode(20)
    root.left.left = BinarySearchTreeNode(3)
    root.left.right = BinarySearchTreeNode(7)
    root.right.left = BinarySearchTreeNode(15)
    root.right.right = BinarySearchTreeNode(25)

    target = int(input("Enter the value to search for: ").strip())
    steps = []
    found = search_bst(root, target, steps)
    
    if found:
        print(f"Node {target} found in the tree.")
    else:
        print(f"Node {target} not found in the tree.")

    latex_document = generate_latex_document_steps(steps)
    filename = "bst_search_steps.tex"

    with open(filename, "w") as file:
        file.write(latex_document)

    print(f"LaTeX code for binary search tree steps has been generated and saved to {filename}")

if __name__ == "__main__":
    main()

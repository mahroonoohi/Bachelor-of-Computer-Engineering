class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def inorder(temp):
    if not temp:
        return []
    return inorder(temp.left) + [temp.data] + inorder(temp.right)

def generate_latex_binary_tree(node, is_root=False):
    if not node:
        return ""

    node_prefix = "\\" if is_root else ""
    latex_code = f"{node_prefix}node {{{node.data}}}"
    
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

% Explanation about the algorithm
\section*{Binary Tree Deletion Algorithm}
In this document, we illustrate the deletion process of a binary tree. The algorithm used for deleting a node involves the following steps:

\begin{itemize}
    \item \textbf{Finding the Node:} We first perform a level-order traversal (breadth-first search) to locate the node to be deleted and the deepest node in the tree.
    \item \textbf{Replacing Data:} We replace the data of the node to be deleted with the data of the deepest node.
    \item \textbf{Deleting Deepest Node:} We then delete the deepest node from the tree.
\end{itemize}

\section*{Deletion Steps}
The following figures illustrate the binary tree at various steps of the deletion process.

"""

    for i in range(0, len(steps), 4):
        latex_code += r"""
\begin{figure}[h!]
\centering
"""
        for j in range(i, min(i + 4, len(steps))):
            caption_text = "Step " + str(j + 1)
            if j == 0:
                caption_text += " (Initial tree)"
                
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




def delete_deepest(root, d_node, steps):
    q = [root]
    while q:
        temp = q.pop(0)
        if temp is d_node:
            temp = None
            return
        if temp.right:
            if temp.right is d_node:
                temp.right = None
                return
            else:
                q.append(temp.right)
        if temp.left:
            if temp.left is d_node:
                temp.left = None
                return
            else:
                q.append(temp.left)

def deletion(root, key, steps):
    if root is None:
        return None
    if root.left is None and root.right is None:
        if root.data == key:
            return None
        else:
            return root
    key_node = None
    q = [root]
    temp = None
    while q:
        temp = q.pop(0)
        if temp.data == key:
            key_node = temp
        if temp.left:
            q.append(temp.left)
        if temp.right:
            q.append(temp.right)
    if key_node:
        x = temp.data
        key_node.data = x
        delete_deepest(root, temp, steps)
        steps.append(generate_latex_binary_tree(root, is_root=True))
    return root

def main():
    root = Node(10)
    root.left = Node(11)
    root.left.left = Node(7)
    root.left.right = Node(12)
    root.right = Node(9)
    root.right.left = Node(15)
    root.right.right = Node(8)

    steps = [generate_latex_binary_tree(root, is_root=True)]
    print("Initial tree created.")

    while True:
        user_input = input("Enter the value of the node to delete (or 'stop' to end): ").strip()
        if user_input.lower() == 'stop':
            break

        try:
            value_to_delete = int(user_input)
            root = deletion(root, value_to_delete, steps)
            print(f"Node {value_to_delete} deleted.")
        except ValueError:
            print("Invalid input. Please enter a valid integer or 'stop'.")

    latex_document = generate_latex_document_steps(steps)
    filename = "binary_tree_deletion_steps.tex"

    with open(filename, "w") as file:
        file.write(latex_document)

    print(f"LaTeX code for binary tree operations steps has been generated and saved to {filename}")

if __name__ == "__main__":
    main()
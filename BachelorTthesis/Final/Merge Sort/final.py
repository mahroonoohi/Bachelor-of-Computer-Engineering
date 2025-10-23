from pylatex import Document, Section, TikZ, Figure, NoEscape

def draw_array(tikz, arr, title, width, height, color_map=None, show_values=True):
    """
    Draw the array and highlight the elements based on their colors.

    Parameters:
    tikz: The TikZ object to draw with.
    arr (list): The list of elements to draw.
    title (str): The title of the array.
    width (float): The width of each array cell.
    height (float): The height of each array cell.
    color_map (dict): A dictionary mapping array indices to colors.
    show_values (bool): Whether to show the values of the elements.
    """
    title_font_size = height * 10
    tikz.append(NoEscape(r'\node at (0,%f) {\textbf{\fontsize{%f}{%f}\selectfont %s}};' % (height * 1.5, title_font_size, title_font_size * 1.2, title)))

    for i, val in enumerate(arr):
        color = color_map.get(i, 'white') if color_map else 'white'
        tikz.append(NoEscape(r'\fill[%s] (%f, 0) rectangle (%f, -%f);' % (color, width * i, width * (i + 1), height)))
        tikz.append(NoEscape(r'\draw (%f, 0) rectangle (%f, -%f);' % (width * i, width * (i + 1), height)))
        if show_values:
            tikz.append(NoEscape(r'\node at (%f, -%f) {\fontsize{%f}{%f}\selectfont %d};' % (width * (i + 0.5), height / 2, height * 8, height * 6, val)))
            tikz.append(NoEscape(r'\node at (%f, %f) {\fontsize{%f}{%f}\selectfont %d};' % (width * (i + 0.5), height / 4, height * 8, height * 6, i)))

def merge_sort_visualize(arr, width, height, doc, color_map):
    divide_steps = []
    merge_steps = []

    original_arr = arr.copy()  # Copy of the original array to use for displaying values in division steps

    def merge_sort(arr, left, right, level):
        if left < right:
            mid = (left + right) // 2

            merge_sort(arr, left, mid, level + 1)
            merge_sort(arr, mid + 1, right, level + 1)

            # Division step (show original values, not sorted)
            color_map_step = {i: 'leftcolor' if left <= i <= mid else 'rightcolor' for i in range(left, right + 1)}
            divide_steps.append((original_arr.copy(), f'Split [{left}, {right}]', color_map_step, level))

            merge(arr, left, mid, right)

            # Merge step (show values and colors)
            color_map_step = {i: 'mergecolor' for i in range(left, right + 1)}
            merge_steps.append((arr.copy(), f' Merge [{left}, {right}]', color_map_step, level))

    def merge(arr, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid

        L = [0] * n1
        R = [0] * n2

        for i in range(0, n1):
            L[i] = arr[left + i]

        for j in range(0, n2):
            R[j] = arr[mid + 1 + j]

        i = 0
        j = 0
        k = left

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    merge_sort(arr, 0, len(arr) - 1, 0)

    # Sort steps based on level
    divide_steps.sort(key=lambda x: x[3])
    merge_steps.sort(key=lambda x: x[3], reverse=True)  # Reverse sorting for merge steps

    # Add steps to the document
    #with doc.create(Section('')):
        # Add division steps
    with doc.create(Section('Division Steps')):
        for arr, title, color_map_step, level in divide_steps:
            with doc.create(Figure(position='h!')) as fig:
                with fig.create(TikZ()) as tikz:
                    draw_array(tikz, arr, title, width, height, color_map=color_map_step, show_values=True)

        # Add merge steps in reverse order
        with doc.create(Section('Merge Steps')):
            for arr, title, color_map_step, level in merge_steps:
                with doc.create(Figure(position='h!')) as fig:
                    with fig.create(TikZ()) as tikz:
                        draw_array(tikz, arr, title, width, height, color_map=color_map_step, show_values=True)

def create_visualization(arr, width, height, color_map):
    doc = Document()
    doc.preamble.append(NoEscape(r'\usepackage{geometry}'))
    doc.preamble.append(NoEscape(r'\geometry{a4paper, left=0.5in, top=0.5in}'))
    doc.preamble.append(NoEscape(r'\usepackage{tikz}'))
    doc.preamble.append(NoEscape(r'\usepackage{xcolor}'))

    # Define the colors in LaTeX
    for color_name, color_code in color_map.items():
        doc.preamble.append(NoEscape(r'\definecolor{%s}{HTML}{%s}' % (color_name, color_code.lstrip('#'))))

    with doc.create(Section('Merge Sort Visualization')):
        doc.append(NoEscape(r"""
        \section*{Introduction}
        Merge sort is one of the most efficient sorting algorithms. It works on the principle of Divide and Conquer based on the idea of breaking down a list into several sub-lists until each sublist consists of a single element and merging those sublists in a manner that results into a sorted list.
        """))
        merge_sort_visualize(arr, width, height, doc, color_map)
    doc.generate_pdf('merge_sort_visualization', clean_tex=False)

# Get input from the user
input_array = input("Enter a list of numbers separated by spaces: ")
width = float(input("Enter the width of each array cell: "))
height = float(input("Enter the height of each array cell: "))
color_left = input("Enter the color code for the left half of the array (e.g., #FF0000): ")
color_right = input("Enter the color code for the right half of the array (e.g., #0000FF): ")
color_merge = input("Enter the color code for the merged array (e.g., #00FF00): ")

# Convert input string to a list of integers
arr = list(map(int, input_array.split()))

# Create a dictionary of colors
color_map = {
    'leftcolor': color_left,
    'rightcolor': color_right,
    'mergecolor': color_merge
}

# Create the LaTeX document with visualizations
create_visualization(arr, width, height, color_map)

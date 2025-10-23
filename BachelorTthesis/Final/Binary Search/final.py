
from pylatex import Document, Section, TikZ, Figure, NoEscape
def create_visualization(arr, target, width, height, left_color, right_color, mid_color, bg_color, target_color):
    """
    Create a LaTeX document with visualizations of the binary search process.

    Parameters:
    arr (list): The list of elements to search through.
    target (int): The element to search for.
    width (float): The width of each array cell.
    height (float): The height of each array cell.
    left_color (str): The color for the left index.
    right_color (str): The color for the right index.
    mid_color (str): The color for the mid index.
    bg_color (str): The background color of the array.
    target_color (str): The color for the target element when found.
    """
    # Create a new LaTeX document
    doc = Document()

    # Set up margins (left, top, right, bottom)
    doc.preamble.append(NoEscape(r'\usepackage[a4paper, left=0.5in, top=0.5in]{geometry}'))

    with doc.create(Section('Binary Search Visualization')):
        doc.append(NoEscape(r"""
        \section*{Introduction}
        Binary search is an efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing in half the portion of the list that could contain the item, until you've narrowed down the possible locations to just one. 
        """))
        # Define colors
        doc.preamble.append(NoEscape(r'\usepackage{xcolor}'))
        doc.preamble.append(NoEscape(r'\definecolor{leftcolor}{HTML}{%s}' % left_color.lstrip('#')))
        doc.preamble.append(NoEscape(r'\definecolor{rightcolor}{HTML}{%s}' % right_color.lstrip('#')))
        doc.preamble.append(NoEscape(r'\definecolor{midcolor}{HTML}{%s}' % mid_color.lstrip('#')))
        doc.preamble.append(NoEscape(r'\definecolor{bgcolor}{HTML}{%s}' % bg_color.lstrip('#')))
        doc.preamble.append(NoEscape(r'\definecolor{targetcolor}{HTML}{%s}' % target_color.lstrip('#')))

        # Initial array
        with doc.create(Figure(position='h!')) as initial_fig:
            with initial_fig.create(TikZ()) as tikz:
                draw_array(tikz, arr, 'Initial Array', width, height, None, None, None, False, None)
            #initial_fig.add_caption('Initial array as input by the user')

        # Sorted array
        arr.sort()
        with doc.create(Figure(position='h!')) as sorted_fig:
            with sorted_fig.create(TikZ()) as tikz:
                draw_array(tikz, arr, 'Sorted Array', width, height, None, None, None, False, None)
            #sorted_fig.add_caption('Array after sorting')

        # Binary search steps
        left, right = 0, len(arr) - 1
        step = 1
        target_index = None
        while left <= right:
            mid = left + (right - left) // 2

            with doc.create(Figure(position='h!')) as step_fig:
                with step_fig.create(TikZ()) as tikz:
                    draw_array(tikz, arr, f'Step {step}', width, height, left, right, mid, False, None)
                #step_fig.add_caption(f'Step {step} of the binary search')

            if arr[mid] == target:
                target_index = mid
                break
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

            step += 1

        # Final step to highlight the found target element
        if target_index is not None:
            with doc.create(Figure(position='h!')) as final_fig:
                with final_fig.create(TikZ()) as tikz:
                    draw_array(tikz, arr, 'Final Step', width, height, None, None, None, True, target_index)
                #final_fig.add_caption('Final step highlighting the found target element')

    doc.generate_pdf('binary_search_visualization', clean_tex=False)


def draw_array(tikz, arr, title, width, height, left=None, right=None, mid=None, target_found=False, target_index=None):
    """
    Draw the array and highlight the elements based on the binary search step.

    Parameters:
    tikz: The TikZ object to draw with.
    arr (list): The list of elements to draw.
    title (str): The title of the array.
    width (float): The width of each array cell.
    height (float): The height of each array cell.
    left (int): The left index in the binary search.
    right (int): The right index in the binary search.
    mid (int): The mid index in the binary search.
    target_found (bool): Whether the target has been found.
    target_index (int): The index of the target element if found.
    """
    # Define font size multipliers
    value_font_size = height * 8
    index_font_size = height * 8
    label_font_size = height * 8
    title_font_size = height * 10

    tikz.append(NoEscape(r'\node at (0,%f) {\textbf{\fontsize{%f}{%f}\selectfont %s}};' % (height * 1.5, title_font_size, title_font_size * 1.2, title)))

    for i, val in enumerate(arr):
        if target_found and target_index == i:
            # Fill the target element's cell with target color
            tikz.append(NoEscape(r'\fill[targetcolor] (%f, 0) rectangle (%f, -%f);' % (width * i, width * (i + 1), height)))
        else:
            tikz.append(NoEscape(r'\fill[bgcolor] (%f, 0) rectangle (%f, -%f);' % (width * i, width * (i + 1), height)))
        
        tikz.append(NoEscape(r'\draw (%f, 0) rectangle (%f, -%f);' % (width * i, width * (i + 1), height)))
        tikz.append(NoEscape(r'\node at (%f, -%f) {\fontsize{%f}{%f}\selectfont %d};' % (width * (i + 0.5), height / 2, value_font_size, value_font_size * 0.8, val)))
        index_vertical_offset = height / 5
        tikz.append(NoEscape(r'\node at (%f, %f) {\fontsize{%f}{%f}\selectfont %d};' % (width * (i + 0.5), height / 5 + index_vertical_offset, index_font_size, index_font_size * 0.8, i)))

    if left is not None and right is not None and mid is not None and not target_found:
        # Calculate the radius of the circles based on the height of the array cells
        radius = height / 2  # You can adjust this proportion as needed

        # Draw circles around left, right, and mid elements at the same vertical position
        tikz.append(NoEscape(r'\draw[leftcolor, very thick] (%f, %f) circle (%f);' % (width * (left + 0.5), -height / 2, radius)))
        tikz.append(NoEscape(r'\draw[rightcolor, very thick] (%f, %f) circle (%f);' % (width * (right + 0.5), -height / 2, radius)))
        tikz.append(NoEscape(r'\draw[midcolor, very thick] (%f, %f) circle (%f);' % (width * (mid + 0.5), -height / 2, radius)))

        # Check for overlap and adjust positions for labels
        positions = {}
        for idx, color, label in [(left, 'leftcolor', 'Left'), (right, 'rightcolor', 'Right'), (mid, 'midcolor', 'Mid')]:
            if idx is not None:
                pos = width * (idx + 0.5)
                if pos in positions:
                    positions[pos].append(label)
                else:
                    positions[pos] = [label]

        # Adjust vertical spacing between labels
        vertical_spacing = radius  # You can adjust this proportion as needed

        # Draw labels for left, right, and mid elements
        for pos, labels in positions.items():
            for i, label in enumerate(labels):
                tikz.append(NoEscape(r'\node[below] at (%f, %f) {\fontsize{%f}{%f}\selectfont %s};' % (pos, -height * 1 - i * vertical_spacing, label_font_size, label_font_size * 0.8, label)))

# Get input from the user
input_array = input("Enter a list of numbers separated by spaces: ")
target = int(input("Enter the number to search for: "))
width = float(input("Enter the width of each array cell: "))
height = float(input("Enter the height of each array cell: "))
left_color = input("Enter the color code for the left index (e.g., #FF0000): ")
right_color = input("Enter the color code for the right index (e.g., #0000FF): ")
mid_color = input("Enter the color code for the mid index (e.g., #00FF00): ")
bg_color = input("Enter the background color code of the array (e.g., #FFFF00): ")
target_color = input("Enter the color code for the target element (e.g., #00FF00): ")

# Convert input string to a list of integers
arr = list(map(int, input_array.split()))

# Create the LaTeX document with visualizations
create_visualization(arr, target, width, height, left_color, right_color, mid_color, bg_color, target_color)
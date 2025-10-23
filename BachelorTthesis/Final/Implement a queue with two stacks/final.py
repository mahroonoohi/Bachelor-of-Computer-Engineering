from pylatex import Document, Section, TikZ, NoEscape
from pylatex.utils import escape_latex

class QueueWithStacks:
    def __init__(self, custom_color):
        self.stack1 = []
        self.stack2 = []
        self.doc = Document()
        self.custom_color = custom_color.lstrip('#')
        self.create_document()
        self.cell_width = 1  
        self.cell_height = 1  

    def create_document(self):
        self.doc.preamble.append(NoEscape(r'\usepackage{tikz}'))
        self.doc.preamble.append(NoEscape(r'\usetikzlibrary{shapes.multipart}'))
        self.doc.preamble.append(NoEscape(r'\usepackage[a4paper, left=1in, top=1in]{geometry}'))
        self.doc.preamble.append(NoEscape(rf'\definecolor{{mystackcolor}}{{HTML}}{{{self.custom_color}}}'))

        self.doc.append(NoEscape(r'''
        \section*{Implementing a Queue Using Two Stacks}
        A queue follows the First In First Out (FIFO) principle, while a stack follows the Last In First Out (LIFO) principle. We aim to mimic the behavior of a queue using two stacks.
        \subsection*{Solution Approach}
        For enqueue operation, simply push the element to stack1.
        For dequeue operation, if stack2 is empty, transfer all elements from stack1 to stack2. Then pop from stack2.
        '''))

    def set_cell_dimensions(self, width, height):
        self.cell_width = width
        self.cell_height = height

    def enqueue(self, x):
        self.stack1.append(x)
        self.add_step(f"Enqueue({x})")

    def dequeue(self):
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
            self.add_step("Transferred stack1 to stack2")
        if self.stack2:
            result = self.stack2.pop()
            self.add_step(f"Dequeue(): {result}")
            return result
        else:
            self.add_step("Dequeue(): Queue is empty")
            return "Queue is empty"

    def add_step(self, operation):
        with self.doc.create(Section(operation)):
            with self.doc.create(TikZ()):
                self.draw_stack(self.stack1, "stack1", x_shift=0)
                self.draw_stack(self.stack2, "stack2", x_shift=4)
        self.doc.append(NoEscape(r"\vspace{1cm}"))

    def get_font_size(self):
        # Font size relative to cell dimensions
        return min(self.cell_width, self.cell_height) * 10

    def draw_stack(self, stack, name, x_shift):
        max_height = max(len(self.stack1), len(self.stack2))
        font_size = self.get_font_size()
        for i in range(max_height):
            value = stack[len(stack) - 1 - i] if i < len(stack) else ""
            fill_color = "mystackcolor" if value != "" else "white"
            
            # Preparing the LaTeX string
            node_str = (
                rf'\node[draw, fill={fill_color}, rectangle, minimum width={self.cell_width}cm, '
                rf'minimum height={self.cell_height}cm] at ({x_shift}, {-i * self.cell_height}) '
                rf'{{\fontsize{{{font_size}pt}}{{{font_size}pt}}\selectfont {escape_latex(str(value))}}};'
            )
            # Appending the node string to the document
            self.doc.append(NoEscape(node_str))

        # Preparing the label for the stack
        label_str = (
            rf'\node[below] at ({x_shift}, {-max_height * self.cell_height }) '
            rf'{{\fontsize{{{font_size}pt}}{{{font_size}pt}}\selectfont {escape_latex(name)}}};'
        )
        # Appending the label string to the document
        self.doc.append(NoEscape(label_str))

    def generate_latex(self, filename="queue_with_stacks.tex"):
        self.doc.generate_tex(filename)


custom_color = input("Please enter the color code for the filled stack cells ( #a9fc8d ): ")

queue = QueueWithStacks(custom_color)

cell_width = float(input("Please enter the width of each stack cell (in cm): "))
cell_height = float(input("Please enter the height of each stack cell (in cm): "))
queue.set_cell_dimensions(cell_width, cell_height)

enqueue_values = input("Please enter the values to enqueue (separated by spaces): ")
values = list(map(int, enqueue_values.split()))
for value in values:
    queue.enqueue(value)

num_dequeue = int(input("Please enter the number of items to dequeue: "))
for _ in range(num_dequeue):
    queue.dequeue()

queue.generate_latex("queue_with_stacks")

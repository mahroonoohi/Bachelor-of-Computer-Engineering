from pylatex import Document, Section, TikZ, Figure, NoEscape
from pylatex.utils import escape_latex
from pylatex.package import Package

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return None

class Stack:
    def __init__(self, doc, width, height, queue_capacity=5, push_color='#00FF00'):
        self.queue1 = Queue()
        self.queue2 = Queue()
        self.doc = doc
        self.queue_capacity = queue_capacity
        self.width = width
        self.height = height
        self.push_color_name = 'pushcolor'
        self.element_colors = {}  # برای ذخیره رنگ هر عنصر push شده
        self.font_size = min(width, height) * 0.3

        # تعریف رنگ push در ابتدای سند لاتکس
        self.doc.preamble.append(NoEscape(r'\definecolor{%s}{HTML}{%s}' % (self.push_color_name, push_color.lstrip('#'))))

    def is_empty(self):
        return self.queue1.is_empty() and self.queue2.is_empty()

    def push(self, data):
        self.queue2.enqueue(data)
        self.element_colors[data] = self.push_color_name  # ذخیره رنگ عنصر push شده
        self.draw_queues(f'After pushing {data}')

        while not self.queue1.is_empty():
            self.queue2.enqueue(self.queue1.dequeue())
            self.draw_queues('During push (transferring elements)')

        self.queue1, self.queue2 = self.queue2, self.queue1
        self.draw_queues(f'Final state after pushing {data}')

    def pop(self):
        if self.queue1.is_empty():
            return None

        popped_value = self.queue1.dequeue()
        self.draw_queues(f'Final state after popping {popped_value}')
        return popped_value

    def draw_queues(self, title=''):
        with self.doc.create(Section(title)):
            self.draw_queue(self.queue1.items, 'Queue 1')
            self.draw_queue(self.queue2.items, 'Queue 2')

    def draw_queue(self, items, queue_name):
        with self.doc.create(Figure(position='H')) as fig:
            with self.doc.create(TikZ()) as tikz:
                queue_length = len(items)
                for i in range(self.queue_capacity):
                    item = items[i] if i < queue_length else ''
                    color = self.element_colors.get(item, 'white')

                    # استفاده از رنگ ذخیره‌شده برای هر عنصر
                    tikz.append(NoEscape(
                        f'\\node[draw, rectangle, minimum width={self.width}cm, minimum height={self.height}cm, fill={color}, font=\\fontsize{{{self.font_size}cm}}{{{self.font_size * 1.2}cm}}\\selectfont] '
                        f'at ({i * self.width}, 0) {{{escape_latex(str(item))}}};'))

                # افزودن برچسب برای نام صف
                tikz.append(NoEscape(
                    f'\\node[below] at ({(self.queue_capacity * self.width) / 2 - 0.5 * self.width}, -{0.5 * self.height}) '
                    f'{{{escape_latex(queue_name)}}};'))

def process_operations(operations, doc, width, height, push_color):
    s = Stack(doc, width, height, push_color=push_color)
    ops = operations.split(',')

    for op in ops:
        command = op.strip().split()
        if command[0].lower() == 'push':
            s.push(int(command[1]))
        elif command[0].lower() == 'pop':
            if s.is_empty():
                with doc.create(Section("Stack is empty.")):
                    pass
            else:
                s.pop()

def main():
    user_input = input("Please enter the stack operations (e.g., 'push 5,push 10,pop,push 15'): ")
    width = float(input("Enter the width of the queue cells (in cm): "))
    height = float(input("Enter the height of the queue cells (in cm): "))
    push_color = input("Enter the hex color code for push operations (e.g., '#00FF00'): ")

    doc = Document()
    doc.packages.append(Package('xcolor'))  
    doc.packages.append(Package('float'))
    
    doc.packages.append(Package('geometry', options="top=2.5cm, left=2.5cm, right=2.5cm"))

    with doc.create(Section("Stack Implementation Using Two Queues")):
        doc.append(NoEscape(
            "A stack is a LIFO (Last In, First Out) data structure, while a queue is a FIFO (First In, First Out) data structure. "
            "The challenge here is to simulate stack behavior using queues. We can use two queues, q1 and q2, to implement a stack. "
            "The key idea is to:\n\n"
            "Push operation:\n"
            "1. Enqueue the new element into q2.\n"
            "2. Dequeue all elements from q1 and enqueue them into q2.\n"
            "3. Swap the names of q1 and q2.\n\n"
            "Pop operation:\n"
            "1. Dequeue and return the front element of q1."
        ))

    process_operations(user_input, doc, width, height, push_color)
    doc.generate_pdf('stack_operations', clean_tex=False)

if __name__ == '__main__':
    main()

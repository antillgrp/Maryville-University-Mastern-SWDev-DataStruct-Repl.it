import random
import sys
from queue import Queue
import curses
import time

class HeapBSTree:

    # https://www.datacamp.com/community/tutorials/inner-classes-python
    class __bstNode:
      def __init__(self, value, leNode=None, gtNode=None):
        self.nodeTuple = (leNode, value, gtNode)      
      @property
      def value(self):
        return self.nodeTuple[1]
      # NO SET VALUE
      @property
      def leBranch(self):
        return self.nodeTuple[0]
      def setLeBranch(self, bstNode):
        self.nodeTuple = (
          bstNode,
          self.nodeTuple[1],
          self.nodeTuple[2]          
        )
      @property
      def gtBranch(self):
        return self.nodeTuple[2]
      def setGtBranch(self, bstNode):
        self.nodeTuple = (
          self.nodeTuple[0],
          self.nodeTuple[1],          
          bstNode          
        )

    def __init__(self):        
        # HEAP
        self.__heap = []
        self.__last_index = -1
        self.__heapLogQueue = Queue()

        # BST
        self.__BSTRoot = None
        self.__BSTLogQueue = Queue()

        self.__last_inserted_str = str(int(sys.maxsize))
    
    def cursesAnimatedDump(self, values):

        # https://docs.python.org/3/howto/curses.html
        # stdscr = curses.initscr()
        
        def drawQueue(stdscr, headerStr, logQueue, startLine=0): 
          try:
            curses.noecho()
            curses.cbreak()

            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

            finalLine = 0            
            while not logQueue.empty():
              stdscr.clear()
              stdscr.addstr(startLine, 0, headerStr)
              stdscr.addstr(startLine + 2, 0, "Inserted value:")

              inserted, treeLines = logQueue.get_nowait()
                            
              subStrs = str(values).partition(inserted)
              
              stdscr.addstr(startLine + 4, 0, "{}".format(subStrs[0]))
              stdscr.addstr(
                startLine + 4, 
                len(subStrs[0]), 
                "{}".format(subStrs[1]),
                curses.color_pair(1) | curses.A_BOLD
              )
              stdscr.addstr(
                startLine + 4, 
                len(subStrs[0] + subStrs[1]), 
                "{}".format(subStrs[2])
              )

              for i in range(len(treeLines)):
                finalLine = startLine + 6 + i
                subStrs = treeLines[i].partition(inserted)
                stdscr.addstr(finalLine , 0, "{}".format(subStrs[0]))
                stdscr.addstr(
                  finalLine, 
                  len(subStrs[0]), 
                  "{}".format(subStrs[1]),
                  curses.color_pair(1) | curses.A_BOLD
                )
                stdscr.addstr(
                  finalLine, 
                  len(subStrs[0] + subStrs[1]), 
                  "{}".format(subStrs[2])
                )

              stdscr.refresh()
              print("\r")
              time.sleep(2) 
            
            stdscr.getch()
            return finalLine
          finally:
              curses.echo()
              curses.nocbreak()
              #curses.endwin()

        def draw(stdscr):
          drawQueue(stdscr, "HEAP TREE BUILDING ...", self.__heapLogQueue, 0)
          drawQueue(stdscr, "BST TREE BUILDING ...", self.__BSTLogQueue, 0)

        curses.wrapper(draw)

    def __logOperations(self, push=True):
        self.__last_inserted_str = self.__last_inserted_str if push else str(int(sys.maxsize))
        self.__logHeapOperation(push)
        self.__logBSTOperation(push)

    def __buildHeapTString(self, rootIndex=0, showLevel=False):

      if rootIndex >= len(self.__heap) or len(self.__heap) == 0:
          return [], 0, 0, 0

      nodeStr = '{}({})'.format(
          '[{}]'.format(rootIndex) if showLevel else '',
          str(self.__heap[rootIndex])
      )

      new_root_width = gap_size = len(nodeStr)

      # Get the left and right sub-boxes, their widths, and root repr positions
      l_box, l_box_width, l_root_start, l_root_end = self.__buildHeapTString(
          2 * rootIndex + 1,  # <-- LEFT
          showLevel
      )
      r_box, r_box_width, r_root_start, r_root_end = self.__buildHeapTString(
          2 * rootIndex + 2,  # <-- RIGHT
          showLevel
      )

      rootLine = []
      arrowsLine = []

      # Draw the branch connecting the current root node to the left sub-box
      # Pad the line with whitespaces where necessary
      if l_box_width > 0:
          l_root = (l_root_start + l_root_end) // 2 + 1
          rootLine.append(' ' * (l_root + 1))
          rootLine.append('_' * (l_box_width - l_root))
          arrowsLine.append(' ' * l_root + '/')
          arrowsLine.append(' ' * (l_box_width - l_root))
          new_root_start = l_box_width + 1
          gap_size += 1
      else:
          new_root_start = 0

      # Draw the representation of the current root node
      rootLine.append(nodeStr)
      arrowsLine.append(' ' * new_root_width)

      # Draw the branch connecting the current root node to the right sub-box
      # Pad the line with whitespaces where necessary
      if r_box_width > 0:
          r_root = (r_root_start + r_root_end) // 2
          rootLine.append('_' * r_root)
          rootLine.append(' ' * (r_box_width - r_root + 1))
          arrowsLine.append(' ' * r_root + '\\')
          arrowsLine.append(' ' * (r_box_width - r_root))
          gap_size += 1
      new_root_end = new_root_start + new_root_width - 1

      # Combine the left and right sub-boxes with the branches drawn above
      gap = ' ' * gap_size
      new_box = [''.join(rootLine), ''.join(arrowsLine)]
      for i in range(max(len(l_box), len(r_box))):
          l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
          r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
          new_box.append(l_line + gap + r_line)

      # Return the new box, its width and its root repr positions
      return new_box, len(new_box[0]), new_root_start, new_root_end

    def __logHeapOperation(self, push=True):  # push = False for pop      
      
      lines = self.__buildHeapTString()[0]   
      self.__heapLogQueue.put_nowait((self.__last_inserted_str, lines))

    def __build_BSTString(self, showLevel=False):
      
      def build_BSTString(root, showLevel, level=0):
        if root == None:
          return [], 0, 0, 0

        nodeStr = '{}({})'.format(
          '[{}]'.format(level) if showLevel else '',
          str(root.value)
        )

        new_root_width = gap_size = len(nodeStr)

        # Get the left and right sub-boxes, their widths, and root repr positions
        l_box, l_box_width, l_root_start, l_root_end = build_BSTString(
            root.leBranch,
            showLevel,
            level + 1
        )
        r_box, r_box_width, r_root_start, r_root_end = build_BSTString(
            root.gtBranch,
            showLevel,
            level +1
        )
        
        rootLine = []
        arrowsLine = []

        # Draw the branch connecting the current root node to the left sub-box
        # Pad the line with whitespaces where necessary
        if l_box_width > 0:
            l_root = (l_root_start + l_root_end) // 2 + 1
            rootLine.append(' ' * (l_root + 1))
            rootLine.append('_' * (l_box_width - l_root))
            arrowsLine.append(' ' * l_root + '/')
            arrowsLine.append(' ' * (l_box_width - l_root))
            new_root_start = l_box_width + 1
            gap_size += 1
        else:
            new_root_start = 0
          
        # Draw the representation of the current root node
        rootLine.append(nodeStr)
        arrowsLine.append(' ' * new_root_width)

        # Draw the branch connecting the current root node to the right sub-box
        # Pad the line with whitespaces where necessary
        if r_box_width > 0:
            r_root = (r_root_start + r_root_end) // 2
            rootLine.append('_' * r_root)
            rootLine.append(' ' * (r_box_width - r_root + 1))
            arrowsLine.append(' ' * r_root + '\\')
            arrowsLine.append(' ' * (r_box_width - r_root))
            gap_size += 1
        new_root_end = new_root_start + new_root_width - 1

        # Combine the left and right sub-boxes with the branches drawn above
        gap = ' ' * gap_size
        new_box = [''.join(rootLine), ''.join(arrowsLine)]
        for i in range(max(len(l_box), len(r_box))):
            l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
            r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
            new_box.append(l_line + gap + r_line)

        # Return the new box, its width and its root repr positions
        return new_box, len(new_box[0]), new_root_start, new_root_end


      return build_BSTString(self.__BSTRoot, showLevel)

    def __logBSTOperation(self, push=True): # push = False for pop

        lines = self.__build_BSTString()[0]
        self.__BSTLogQueue.put_nowait((self.__last_inserted_str, lines))

    def push(self, value):        
        self.__last_index += 1
        if self.__last_index < len(self.__heap):
            self.__heap[self.__last_index] = value
        else:
            self.__heap.append(value)
        self.__siftup(self.__last_index)

        # push for BST
        self.__BSTpush(value)

        # visual logger
        self.__last_inserted_str = str(value)
        self.__logOperations(True)
    
    def __BSTpush(self, value):

        def recursiveBSTpush(root: self.__bstNode, value):
          if value <= root.value:
            if root.leBranch == None:
              root.setLeBranch(self.__bstNode(value, None, None))
            else:
              recursiveBSTpush(root.leBranch, value)
          else:
            if root.gtBranch == None:
              root.setGtBranch(self.__bstNode(value, None, None))
            else:
              recursiveBSTpush(root.gtBranch, value)

        if self.__BSTRoot == None:
          self.__BSTRoot = self.__bstNode(value, None, None)
        else:
          recursiveBSTpush(self.__BSTRoot, value)

      # def pop(self):
      #     if self.__last_index == -1:
      #         raise IndexError('pop from empty heap')

      #     min_value = self.__heap[0]

      #     self.__heap[0] = self.__heap[self.__last_index]
      #     self.__last_index -= 1
      #     self.__siftdown(0)

      #     return min_value

    def __siftup(self, index):
        while index > 0:
            parent_index, parent_value = self.__get_parent(index)

            if parent_value <= self.__heap[index]:
                break

            self.__heap[parent_index], self.__heap[index] = \
                self.__heap[index], self.__heap[parent_index]

            index = parent_index

    def __siftdown(self, index):
        while True:
            index_value = self.__heap[index]

            left_child_index, left_child_value = self.__get_left_child(index, index_value)
            right_child_index, right_child_value = self.__get_right_child(index, index_value)

            if index_value <= left_child_value and index_value <= right_child_value:
                break

            if left_child_value < right_child_value:
                new_index = left_child_index
            else:
                new_index = right_child_index

            self.__heap[new_index], self.__heap[index] = \
                self.__heap[index], self.__heap[new_index]

            index = new_index

    def __get_parent(self, index):
        if index == 0:
            return None, None

        parent_index = (index - 1) // 2

        return parent_index, self.__heap[parent_index]

    def __get_left_child(self, index, default_value):
        left_child_index = 2 * index + 1

        if left_child_index > self.__last_index:
            return None, default_value

        return left_child_index, self.__heap[left_child_index]

    def __get_right_child(self, index, default_value):
        right_child_index = 2 * index + 2

        if right_child_index > self.__last_index:
            return None, default_value

        return right_child_index, self.__heap[right_child_index]

    def __len__(self):
        return self.__last_index + 1
  
    def __str__(self):
        lines = self.__build_tree_string(0)[0]
        return '\n' + '\n'.join((line.rstrip() for line in lines))

    
def run():

  values = random.sample(range(10000), 15)
  # print(values)

  h = HeapBSTree()
  for v in values:
      h.push(v)
      #print(h)
  
  h.cursesAnimatedDump(values) 




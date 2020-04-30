# Assignment Requirements

# Consider the following list of integers: 
# [1,2,3,4,5,6,7,8,9,10].  
# Show how this list is sorted by the following algorithms:

#     bubble sort
#     selection sort
#     insertion sort

# Q. What is the difference between a list and a dictionary?
# A. A list is an ordered sequence of objects, whereas dictionaries are unordered sets. But the main difference is that items in dictionaries are accessed via keys and not via their position.   


# How are they coded differently and what different implementations they have?  

# Dictionaries are the Python implementation of an abstract data type, known in computer science as an associative array. Associative arrays consist - like dictionaries of (key, value) pairs, such that each possible key appears at most once in the collection. Any key of the dictionary is associated (or mapped) to a value. Dictionaries don't support the sequence operation of the sequence data types like strings, tuples and lists. Dictionaries belong to the built-in mapping type, but so far they are the sole representative of this kind! 

#Build a script that utilizes at least one list and one dictionary.

import curses
from collections import defaultdict
from queue import Queue
import random
import _thread
import time


def bubble_sort(nums,
                logSwap=lambda alg, seq: print("{}:{}".format(alg, seq))):
    # We set swapped to True so the loop looks runs at least once
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                # Swap the elements
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                # Set the flag to True so we'll loop again
                swapped = True
                # log swapped
                logSwap("bubble_sort", nums)


def selection_sort(nums,
                   logSwap=lambda alg, seq: print("{}:{}".format(alg, seq))):
    # This value of i corresponds to how many values were sorted
    for i in range(len(nums)):
        # We assume that the first item of the unsorted segment is the smallest
        lowest_value_index = i
        # This loop iterates over the unsorted items
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[lowest_value_index]:
                lowest_value_index = j
        # Swap values of the lowest unsorted element with the first unsorted
        # element
        nums[i], nums[lowest_value_index] = nums[lowest_value_index], nums[i]
        # log swapped
        logSwap("selection_sort", nums)


def insertion_sort(nums,
                   logSwap=lambda alg, seq: print("{}:{}".format(alg, seq))):
    # Start on the second element as we assume the first element is sorted
    for i in range(1, len(nums)):
        item_to_insert = nums[i]
        # And keep a reference of the index of the previous element
        j = i - 1
        # Move all items of the sorted segment forward if they are larger than
        # the item to insert
        while j >= 0 and nums[j] > item_to_insert:
            nums[j + 1] = nums[j]
            j -= 1
        # Insert the item
        nums[j + 1] = item_to_insert
        # log swapped
        logSwap("insertion_sort", nums)


class sortingStepLogger:
    def __init__(self, maxLen, stdscr):
        self.queuesDict = defaultdict(Queue)
        self.lastOneDict = defaultdict(lambda: [])
        self.stdscr = stdscr
        self.maxLen = maxLen

    def __printSeqsAsBars(self, *seqs):
        #print("__printSeqsAsBars", file=open('samplefile.txt', "a+"))
        #print(*seqs, file=open('samplefile.txt', "a+"))
        strBuffer = ''

        self.stdscr.addstr(
            0, 0, "".join(
                map(
                    lambda name: name.upper() + ' ' * (self.maxLen + 6 - len(name)),
                    self.queuesDict.keys())))

        for row in range(len(seqs[0])):
            # for col in range(len(seqs)):
            #   self.stdscr.addstr(row, 0, "NAME")
            strBuffer = ''
            for col in range(len(seqs)):
                strBuffer += '[{:02d}]|{}{}{}'.format(
                    seqs[col][row], '-' * seqs[col][row],
                    ' ' * (self.maxLen - seqs[col][row]), '|')
            self.stdscr.addstr(row + 1, 0, strBuffer)
        self.stdscr.refresh()
        print("\r")

    def log(self, algName, sortingSeq):
        # keep the last added on a temp cache
        # when queuesDict[algName] is empty keep printing out the last one
        self.lastOneDict[algName], sortingSeq = sortingSeq.copy(
        ), self.lastOneDict[algName]
        # add it to the queue
        self.queuesDict[algName].put(self.lastOneDict[algName])

    def dump(self):
        print("dumpInside", file=open('samplefile.txt', "a+"))
        if len(self.queuesDict) > 0:
            print(
                "len(self.queuesDict) > 0", file=open('samplefile.txt', "a+"))
            while any(
                    map(
                        lambda queue: not queue.empty(),
                        self.queuesDict.values()  # values are queues
                    )):
                arrs = [
                    self.queuesDict[algName].get()
                    if not self.queuesDict[algName].empty() else
                    self.lastOneDict[algName]
                    for algName in self.queuesDict.keys()
                ]
                print(*arrs, file=open('samplefile.txt', "a+"))
                self.__printSeqsAsBars(*arrs)
                time.sleep(1)


def run():

    print('Main', file=open('samplefile.txt', "w"))

    nums = []
    while len(nums) < 20:      
      next = random.randint(1, 20)
      if next not in nums:
        nums.append(next)
        
    stdscr = curses.initscr()

    stepLogger = sortingStepLogger(20, stdscr)

    try:
        _thread.start_new_thread(bubble_sort, (
            nums.copy(),
            stepLogger.log,
        ))
        _thread.start_new_thread(selection_sort, (
            nums.copy(),
            stepLogger.log,
        ))
        _thread.start_new_thread(insertion_sort, (
            nums.copy(),
            stepLogger.log,
        ))
    except:
        print(
            "Error: unable to start thread", file=open('samplefile.txt', "a+"))

    try:
        curses.noecho()
        curses.cbreak()

        stepLogger.dump()

        print('stepLogger.dump()', file=open('samplefile.txt', "a+"))

    finally:
        curses.echo()
        curses.nocbreak()
        #curses.endwin()



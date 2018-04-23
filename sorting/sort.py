"""
mod_sort.py contains methods for
drawing sorting visualization and
sorting algorithms
"""

import tkinter as tk
import random
import time
import math
import threading
import copy
import sys

class SortAnimation(object):
	"""
	SortAnimation defines methods for
	drawing list as graph and manipulating
	elements in said list
	"""
	def __init__(self, tk_root, width, height, size, sort_func, generator):
		self.tk_root = tk_root
		self.width = int(width)
		self.height = int(height)
		self.size = size
		self.array = generator(self)
		if len(self.array) != self.size:
			raise Exception("Invalid generator function, expected array of length size")
		self.array2 = [0] * (self.size)
		self.line_width = width / self.size
		if min(self.array) < 0.0:
			self.vertical_translation = abs(min(self.array))
			self.vertical_scale = height / (max(self.array) - min(self.array))
		else:
			self.vertical_translation = 0
			self.vertical_scale = height / max(self.array)
		self.sort_func = sort_func
		self.generator = generator
		self.is_stopped = False
		self.thread = None
		self.canvas = tk.Canvas(self.tk_root, width=width, height=height, background="#dfdfdf")
		self.make_lines()

	def pack(self):
		self.canvas.pack()

	def unpack(self):
		self.canvas.pack_forget()

	def make_lines(self):
		self.lines = [self.canvas.create_line((i + 0.5)*self.line_width, self.height+self.vertical_translation, (i + 0.5)*self.line_width, (self.height - (self.array[i]*self.vertical_scale)) + self.vertical_translation, width=self.line_width) for i in range(0, len(self.array))]

	def start(self):
		if self.thread is not None and self.thread.is_alive():
			self.reset()
		self.thread = threading.Thread(target=self.sort_func, args=(self,), name="sorting")
		self.is_stopped = False
		self.thread.start()
	
	def stop(self):
		self.is_stopped = True

	def reset(self):
		self.stop()
		self.canvas.pack_forget()
		self.array = self.generator(self)
		if len(self.array) != self.size:
			raise Exception("Invalid generator function, expected array of length size")
		self.array2 = [0] * (self.size)
		self.canvas.delete("all")
		self.make_lines()
		self.canvas.pack()

	def get(self, index):
		return self.array[index]

	def min(self):
		return min(self.array)

	def max(self):
		return max(self.array)

	def stopped(self):
		return self.is_stopped

	def swap(self, ind1, ind2):
		tmp = self.array[ind2]
		self.array[ind2] = self.array[ind1]
		self.array[ind1] = tmp
		self.canvas.coords(self.lines[ind2], (ind2 + 0.5)*self.line_width, self.height+self.vertical_translation, (ind2 + 0.5)*self.line_width, (self.height - (self.array[ind2]*self.vertical_scale)) + self.vertical_translation)
		self.canvas.coords(self.lines[ind1], (ind1 + 0.5)*self.line_width, self.height+self.vertical_translation, (ind1 + 0.5)*self.line_width, (self.height - (self.array[ind1]*self.vertical_scale)) + self.vertical_translation)

	def change(self, ind, n):
		self.array[ind] = n
		self.canvas.coords(self.lines[ind], ind*self.line_width, self.height+self.vertical_translation, ind*self.line_width, (self.height - (n*self.vertical_scale)) + self.vertical_translation)

	def colour(self, line, colour):
		self.canvas.itemconfig(self.lines[line], fill=colour)

	def getColour(self, line):
		return self.canvas.itemcget(self.lines[line], "fill")

def partition(sort_anim, left, right):
	l2 = left
	r2 = right - 1
	p = sort_anim.get(right)
	while not sort_anim.stopped():
		while sort_anim.get(l2) <= p and l2 < right:
			l2 += 1
		while r2 > left and sort_anim.get(r2) > p:
			r2 -= 1
		if l2 >= r2:
			break
		else:
			sort_anim.swap(l2, r2)

	sort_anim.swap(l2, right)
	return l2

def quick_sort(sort_anim, left=0, right=0, first=True):
	if first:
		left = 0
		right = sort_anim.size - 1
	if (right - left <= 0) or sort_anim.stopped():
		return
	else:
		pivotPoint = partition(sort_anim, left, right)
		quick_sort(sort_anim, left, pivotPoint - 1, False)
		quick_sort(sort_anim, pivotPoint, right, False)

def bubble_sort(sort_anim):
	is_sorted = False
	num_sorted = 0
	while not is_sorted and not sort_anim.stopped():
		is_sorted = True
		for i in range(1, sort_anim.size - num_sorted):
			if sort_anim.get(i) < sort_anim.get(i-1):
				sort_anim.swap(i, i-1)
				is_sorted = False
			elif sort_anim.stopped():
				break
			num_sorted + 1

def merge(sort_anim, low, mid, high):
	lower = low
	upper = mid + 1
	k = 0
	for i in range(low, high + 1):
		if lower > mid:
			sort_anim.array2[k] = sort_anim.get(upper)
			upper = upper + 1
		elif upper > high:
			sort_anim.array2[k] = sort_anim.get(lower)
			lower = lower + 1
		elif sort_anim.get(lower) < sort_anim.get(upper):
			sort_anim.array2[k] = sort_anim.get(lower)
			lower = lower + 1
		else:
			sort_anim.array2[k] = sort_anim.get(upper)
			upper = upper + 1
		k = k + 1
	lower = low
	for i in range(k):
		sort_anim.change(lower, sort_anim.array2[i])
		lower = lower + 1

def merge_sort(sort_anim, low = 0, high = 0, first = True):
	if first:
		low = 0
		high = sort_anim.size - 1
	if low < high:
		mid = math.floor((low + high)/2)
		merge_sort(sort_anim, low, mid, False)
		merge_sort(sort_anim, mid + 1, high, False)
		merge(sort_anim, low, mid, high)
	else:
		return

def selection_sort(sort_anim):
	current = 0
	while not sort_anim.stopped() and current < sort_anim.size:
		min = sort_anim.get(current)
		switch = current
		for i in range(current + 1, sort_anim.size - 1):
			if sort_anim.get(i) < min:
				min = sort_anim.get(i)
				switch = i
		sort_anim.swap(current, switch)
		current += 1
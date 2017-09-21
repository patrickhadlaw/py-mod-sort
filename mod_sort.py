#
#	python modular sorting animation
#	file: mod_sort.py
#	   description: mod_sort contains the sortAnimation class
#			   and the sorting functions used by sortAnimation
#	license: py-mod-sort/LICENSE (Apache 2.0)
#	by: Patrick Stanislaw Hadlaw
#

import tkinter as tk
import random
import time
import math
import threading
import copy

#
# Sorting Algorithms
#

class SortAnimation(object):
	def __init__(self, tkroot, width, height, arr, sortfunc):
		self.tkRoot = tkroot
		self.width = int(width)
		self.height = int(height)
		self.backup = copy.copy(arr)
		self.array = copy.copy(arr)
		self.lineWidth = width / len(self.array)
		if min(self.array) < 0.0:
			self.verticalTranslation = abs(min(self.array))
			self.verticalScale = height / (max(self.array) - min(self.array))
		else:
			self.verticalTranslation = 0
			self.verticalScale = height / max(self.array)
		self.sortFunc = sortfunc
		self.isStopped = False
		self.thread = None
		self.canvas = tk.Canvas(self.tkRoot, width=width, height=height, background="#dfdfdf")
		self.genLines()
	def pack(self):
		self.canvas.pack()
	def unpack(self):
		self.canvas.pack_forget()
	def genLines(self):
		self.lines = [self.canvas.create_line(i*self.lineWidth, self.height+self.verticalTranslation, i*self.lineWidth, (self.height - (self.array[i]*self.verticalScale)) + self.verticalTranslation, width=self.lineWidth) for i in range(0, len(self.array))]
	def start(self):
		if self.thread is None:
			self.thread = threading.Thread(target=self.sortFunc, args=(self,))
			self.thread.start()
		else:
			self.thread = threading.Thread(target=self.sortFunc, args=(self,))
			self.thread.start()
	def reset(self):
		if self.thread != None and self.thread.is_alive():
			self.isStopped = True
		else:
			if self.thread != None and self.isStopped:
				self.thread.join()
				self.isStopped = False
			self.array = copy.copy(self.backup)
			self.canvas.delete("all")
			self.genLines()
			self.thread = threading.Thread(target=self.sortFunc, args=(self,))
	def get(self, index):
		return self.array[index]
	def min(self):
		return min(self.array)
	def max(self):
		return max(self.array)
	def length(self):
		return len(self.array)
	def stopped(self):
		return self.isStopped
	def swap(self, ind1, ind2):
		tmp = self.array[ind2]
		self.array[ind2] = self.array[ind1]
		self.array[ind1] = tmp
		self.canvas.coords(self.lines[ind2], ind2*self.lineWidth, self.height+self.verticalTranslation, ind2*self.lineWidth, (self.height - (self.array[ind2]*self.verticalScale)) + self.verticalTranslation)
		self.canvas.itemconfig(self.lines[ind1], fill="black")
		self.canvas.coords(self.lines[ind1], ind1*self.lineWidth, self.height+self.verticalTranslation, ind1*self.lineWidth, (self.height - (self.array[ind1]*self.verticalScale)) + self.verticalTranslation)
		self.canvas.itemconfig(self.lines[ind2], fill="black")
	def colour(self, line, colour):
		self.canvas.itemconfig(self.lines[line], fill=colour)
	def getColour(self, line):
		return self.canvas.itemcget(self.lines[line], "fill")

def partition(sortAnim, left, right):
	l2 = left
	r2 = right - 1
	p = sortAnim.get(right)
	sortAnim.colour(right, "red")
	while not sortAnim.stopped():
		while sortAnim.get(l2) <= p and l2 < right:
			l2 += 1
		while r2 > left and sortAnim.get(r2) > p:
			r2 -= 1
		if l2 >= r2:
			break
		else:
			sortAnim.swap(l2, r2)

	sortAnim.swap(l2, right)
	return l2;

def quickSort(sortAnim, left=0, right=0, first=True):
	if first:
		left = 0
		right = sortAnim.length() - 1
	if (right - left <= 0) or sortAnim.stopped():
		return
	else:
		pivotPoint = partition(sortAnim, left, right)
		quickSort(sortAnim, left, pivotPoint - 1, False)
		quickSort(sortAnim, pivotPoint + 1, right, False)

def bubbleSort(sortAnim):
	isSorted = False
	while not isSorted and not sortAnim.stopped():
		isSorted = True
		for i in range(1, sortAnim.length()):
			sortAnim.colour(i, "red")
			if sortAnim.get(i) < sortAnim.get(i-1):
				sortAnim.swap(i, i-1)
				isSorted = False

def radixCountingSort(sortAnim, exp):
	n = sortAnim.length()
	output = [0] * (n)
	count = [0] * (10)

def radixSort(sortAnim):
	print("hello")

def merge(sortAnim, low, mid, high):
		print("hello")

def mergeSort(sortAnim, low = 0, high = 0, first = True):
		print("hello")
##	if first:
##		left = 0
##		right = sortAnim.length() - 1
##	if low < high:
##		mid = round((low + high)/2)
##		mergeSort(sortAnim, low, mid)
##		mergeSort(sortAnim, mid + 1, high)
##		merge(sortAnim, low, mid, high)
##	else:
##		return

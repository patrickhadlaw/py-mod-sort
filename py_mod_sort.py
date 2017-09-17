#
#	python modular sorting animation
#       file: py_mod_sort.py
#       description: 
#	github: https://github.com/patrickhadlaw/py-mod-sort
#	by: Patrick Stanislaw Hadlaw
#

import mod_sort
import mod_gen
import tkinter as tk
import math

root = tk.Tk()
root.geometry("800x600") # Window dimensions

# Dimensions of sorting animation
animationWidth = 400
animationHeight = 200

# Current SortAnimation: defined in mod_sort
currentAnimation = mod_sort.SortAnimation(root, animationWidth, animationHeight, mod_gen.randomize(mod_gen.block(animationWidth, 4, True)), mod_sort.quickSort)

#
# Dropdown menu for sorting functions, allows user to choose function to sort in the animation
#

# Sort function dropdown menu choices
sortOptions = [
        ("QuickSort", mod_sort.quickSort),
        ("RadixSort", mod_sort.radixSort),
        ("MergeSort", mod_sort.mergeSort)
    ]

# Current sort function
sortFunc = mod_sort.quickSort;

def pickSortFunc(value): # Sets sort function on command: dropdown selection
	for name, func in sortOptions:
		if value == name:
			sortFunc = func
			#currentAnimation.unpack()
			currentAnimation = mod_sort.SortAnimation(root, animationWidth, animationHeight, sortData, sortFunc)
			currentAnimation.pack()


defaultSort = tk.StringVar(root)
defaultSort.set("QuickSort") # Default dropdown value

# Dropdown menu definition
dropdownSortFunc = tk.OptionMenu(root, defaultSort, "QuickSort", "RadixSort", "MergeSort", command=pickSortFunc)
dropdownSortFunc.pack()

#
# Dropdown menu for array generator functions, allows user to choose dataset to sort in the animation
#

# Data generation dropdown menu choices
genOptions = [
		("4Block Randomized", mod_gen.randomize(mod_gen.block(animationWidth, 4, True))),
		("Sine Wave Randomized", mod_gen.randomize(mod_gen.functional(animationWidth, 1, lambda x: (4*(math.sin(720*x)))+5, True)))
	]

# Current dataset
a, sortData = genOptions[0]

def pickSortFunc(value): # Sets dataset on dropdown selection
	for name, data in genOptions:
		if value == name:
			sortData = data
			#currentAnimation.unpack()
			currentAnimation = mod_sort.SortAnimation(root, animationWidth, animationHeight, sortData, sortFunc)
			currentAnimation.pack()

			
defaultData = tk.StringVar(root)
defaultData.set("4Block Randomized") # Default dropdown value

# Dropdown menu definition
defaultData = tk.OptionMenu(root, defaultData, "4Block Randomized", "Sine Wave Randomized", "Random")
defaultData.pack();


# Activated on click of sort button, begins the sort animation
def onSort():
	currentAnimation.start()

sort = tk.Button(root, text = "Sort", bd = 1, command=onSort)
sort.pack()

# Activated on click of reset button, stop the sort animation and resets the data
def onReset():
        currentAnimation.reset()

reset = tk.Button(root, text = "Reset", bd = 1, command=onReset)
reset.pack()

currentAnimation.pack()

root.mainloop()


"""
py-mod-sort.py sorting function visualization
"""

import sorting
import math
import argparse

import tkinter as tk

SORT_FUNCTIONS = {
	"QuickSort": sorting.quick_sort,
	"BubbleSort": sorting.bubble_sort,
	"SelectionSort": sorting.selection_sort,
	"MergeSort": sorting.merge_sort
}

def pick_sort_function(sort_anim, option):
	for name, func in SORT_FUNCTIONS.items():
		if option == name:
			sort_anim.sort_func = func
			sort_anim.reset()
			return
	raise Exception("Invalid sorting function")

def four_block_randomized(sort_anim):
	return sorting.randomize(sorting.block(sort_anim.size, 4, True))

def sine_wave_random(sort_anim):
	return sorting.randomize(sorting.functional(sort_anim.size, 1, lambda x: (math.sin(math.radians(x*(360 / sort_anim.size)))) + 1, True))

def random(sort_anim):
	return sorting.randomize(sorting.random_element(sort_anim.size, True))

GENERATORS = {
	"4Block Randomized": four_block_randomized,
	"Sine Wave Randomized": sine_wave_random,
	"Random": random
}

def pick_sort_generator(sort_anim, option):
	for name, generator in GENERATORS.items():
		if option == name:
			sort_anim.generator = generator
			sort_anim.reset()
			return
	raise Exception("Invalid sorting generator")

def main():
	parser = argparse.ArgumentParser(description="Process some integers.")
	parser.add_argument("-w", "--window-size", dest="window_size", default="800x600", help="(default: '800x600') dimension of window string with the format '<width>x<height>'")
	parser.add_argument("-n", "--num-elements", dest="num_elements", default=None, help="(optional) number of elements to sort in animation")

	args = parser.parse_args()

	root = tk.Tk()
	root.geometry(args.window_size)

	split = args.window_size.split("x")

	if args.num_elements is None:
		args.num_elements = split[0]
	if int(args.num_elements) <= 1:
		raise Exception("Invalid number of elements")
	
	animation_width = int(split[0])
	animation_height = int(int(split[1]) / 2)

	sort_animation = sorting.SortAnimation(root, animation_width, animation_height, int(args.num_elements), SORT_FUNCTIONS["QuickSort"], GENERATORS["4Block Randomized"])

	"""
	Dropdown menu for the sorting algorithm,
	allows user to choose sorting algorithm in the animation
	"""

	default_sort = tk.StringVar(root)
	default_sort.set("QuickSort")

	sort_func_dropdown = tk.OptionMenu(root, default_sort, "QuickSort", "BubbleSort", "SelectionSort", "MergeSort", command=lambda option: pick_sort_function(sort_animation, option))
	sort_func_dropdown.pack()

	"""
	Dropdown menu for array generator functions,
	allows user to choose dataset to sort in the animation
	"""
				
	default_generator = tk.StringVar(root)
	default_generator.set("4Block Randomized")

	generator_dropdown = tk.OptionMenu(root, default_generator, "4Block Randomized", "Sine Wave Randomized", "Random", command=lambda option: pick_sort_generator(sort_animation, option))
	generator_dropdown.pack()

	def on_sort():
		sort_animation.start()

	sort = tk.Button(root, text = "Sort", bd = 1, command=on_sort)
	sort.pack()

	def on_reset():
		sort_animation.reset()

	reset = tk.Button(root, text = "Reset", bd = 1, command=on_reset)
	reset.pack()

	sort_animation.pack()

	root.mainloop()

if __name__ == "__main__":
	main()
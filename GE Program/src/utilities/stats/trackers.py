"""Utilities for tracking progress of runs, including time taken per
generation, fitness plots, fitness caches, etc."""

cache = {}
# This dict stores the cache for an evolutionary run. The key for each entry
# is the phenotype of the individual, the value is its fitness.

invalid_cache = []
# This list stores a list of invalid phenotypes over an evolutionary run.
# PonyGE uses this list to avoid re-generating previously seen invalid
# solutions.

best_fitness_list = []
# fitness_plot is simply a list of the best fitnesses at each generation.
# Useful for plotting evolutionary progress.

time_list = []
# time_list stores the system time after each generation has been completed.
# Useful for keeping track of how long each generation takes.

stats_list = []
# List for storing stats at each generation
# Used when verbose mode is off to speed up program

best_ever = None
# Store the best ever individual here.

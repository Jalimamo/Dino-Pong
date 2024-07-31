import pickle

import pygame
from matplotlib import pyplot as plt


def draw_rectangle(window, color, x, y, width, height):
    pygame.draw.rect(window, color, (x, y, width, height))


def draw_circle(window, color, x, y, radius):
    pygame.draw.circle(window, color, (x, y), radius)


def plot(mean_fitness_values, max_fitness_values):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Generation')
    plt.ylabel('Fitness values')
    plt.plot(mean_fitness_values, color="royalblue", label="Mean Fitness")
    plt.plot(max_fitness_values, color="darkorange", linestyle="dashed", label="Max Fitness")
    plt.legend()
    plt.text(len(mean_fitness_values) - 1, mean_fitness_values[-1], str(round(mean_fitness_values[-1], 2)))
    plt.text(len(max_fitness_values) - 1, max_fitness_values[-1], str(round(max_fitness_values[-1], 2)))
    plt.ylim(ymin=0)
    plt.xlim(xmin=0)
    plt.tight_layout()
    plt.pause(.1)


def load_network_from_file(file_path):
    try:
        with open(file_path, "rb") as f:
            network = pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not load the network saved in the supplied path: {file_path}")
    return network

import sys

import pygame

from life import GameOfLife
from patterns import Acorn, RandomPattern, GliderGun

WIDTH  = 800
HEIGHT = 600

TICKRATE = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.display.set_caption('Game of Life')

window = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))


def update_grid(surface, current_state, next_state):
    # Spawn cells that are in next_state and not in current_state
    for cell in next_state.difference(current_state):
        surface.set_at(cell, WHITE)
    # Kill cells that are in current_state and not in next_state
    for cell in current_state.difference(next_state):
        surface.set_at(cell, BLACK)


def run(life):
    current_state = set()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(TICKRATE)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        next_state = life.bounded_set(WIDTH, HEIGHT)

        update_grid(surface, current_state, next_state)

        window.blit(surface, (0, 0))
        pygame.display.flip()

        current_state = next_state
        life.evolve()


def main():
    pattern = RandomPattern(WIDTH, HEIGHT, sparsity=8, seed=420)
    # pattern = Acorn()
    # pattern = GliderGun()
    life = GameOfLife(pattern)

    run(life)


if __name__ == '__main__':
    main()



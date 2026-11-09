import asyncio

import pygame

from game import Game

pygame.init()
asyncio.run(Game().run())

import unittest
import pygame
from Main import load_level, reset_to_start, switch_level, SCREEN_HEIGHT, ground_height, player

def test_load_level():
    print("Testing load_level function...")
    # Test loading a level (e.g., "BG1")
    bg_image, bg_width, ground_image, ground_width = load_level("BG1")
    assert isinstance(bg_image, pygame.Surface)
    assert isinstance(bg_width, int)
    assert isinstance(ground_image, pygame.Surface)
    assert isinstance(ground_width, int)
    print("load_level function passed!")

def test_reset_to_start():
    print("Testing reset_to_start function...")
    # Initialize some variables for testing
    current_level = "BG2"  # Set to a different level
    scroll = 100  # Set to a non-zero scroll value
    player.rect.x = 50  # Set to a non-default player position
    player.rect.y = 300

    # Test resetting to the starting level (e.g., "BG1")
    reset_to_start()
    assert current_level == "BG1"
    assert scroll == 0
    assert player.rect.x == 20
    assert player.rect.y == SCREEN_HEIGHT - ground_height - 250
    print("reset_to_start function passed!")

def test_switch_level():
    print("Testing switch_level function...")
    # Initialize some variables for testing
    current_level = "BG1"  # Set to the starting level
    scroll = 0
    at_lighthouse_entrance_door = True

    # Test switching to a new level (e.g., "BG2")
    new_scroll = 50
    switch_level("BG2", new_scroll)
    assert current_level == "BG2"
    assert scroll == new_scroll
    assert not at_lighthouse_entrance_door
    print("switch_level function passed!")

if __name__ == "__main__":
    pygame.init()

    # Call the test functions
    test_load_level()
    test_reset_to_start()
    test_switch_level()

    pygame.quit()
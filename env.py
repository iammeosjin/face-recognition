"""
environment variables or the folder structures
"""

import os

join_path = os.path.join

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = join_path(BASE_DIR, "input")
TEST_FOLDER = join_path(BASE_DIR, "test")
OUTPUT_FOLDER = join_path(BASE_DIR, "output")

if not os.path.exists(INPUT_FOLDER):
    os.makedirs(INPUT_FOLDER)

if not os.path.exists(TEST_FOLDER):
    os.makedirs(TEST_FOLDER)


if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

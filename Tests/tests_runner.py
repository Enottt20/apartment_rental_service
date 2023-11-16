import os
import time
from subprocess import run
from threading import Timer
from logging import getLogger

logger = getLogger(__name__)

def run_script(script_path):
    logger.info(f"Running script: {script_path}")
    run(["python3", "-m", "unittest", script_path])

def run_all_scripts_in_directory(directory):
    script_paths = []

    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            script_path = os.path.join(directory, filename)
            script_paths.append(script_path)

    run_all_scripts(script_paths)

def run_all_scripts(script_paths):
    for script_path in script_paths:
        run_script(script_path)

if __name__ == "__main__":
    tests_directory = "e2e_tests"

    delay_before_start = 20
    logger.info(f"Waiting for {delay_before_start} seconds before starting tests.")
    time.sleep(delay_before_start)

    logger.info("Tests run")
    run_all_scripts_in_directory(tests_directory)

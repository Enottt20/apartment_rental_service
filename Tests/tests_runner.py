import os
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

    logger.info("Tests will run after 15 seconds")
    timer = Timer(1, run_all_scripts_in_directory, args=(tests_directory,))
    timer.start()

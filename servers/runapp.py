import os
import sys


# Get the path to the base directory of the app
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# append the path to the WSGI env path
sys.path.insert(0, BASE_DIR)

from emule import app as application

if __name__ == "__main__":
    application.run('localhost', 5000, True)

import sys
import os

# Add the current directory to the module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from atm_client import start_atm

def main():
    start_atm("atm2")

if __name__ == "__main__":
    main()

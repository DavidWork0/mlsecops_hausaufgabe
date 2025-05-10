#!/usr/bin/env python3

import os
import sys

def main():
    print("Starting run_all.py")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print("Listing installed packages:")
    os.system("pip list")
    
    # Your application code goes here
    print("Run_all.py completed successfully")

if __name__ == "__main__":
    main()

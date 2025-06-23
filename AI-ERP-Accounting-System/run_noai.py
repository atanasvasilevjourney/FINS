#!/usr/bin/env python3
"""
Simple runner for the ERP system without AI integration
"""

import subprocess
import sys
import os

def run_tests():
    """Run system tests"""
    print("Running system tests...")
    try:
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Tests failed: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Run the ERP system without AI integration"""
    print("FINS ERP System (No AI) - Launcher")
    print("=" * 40)
    
    # Change to the current directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # Check if requirements are installed
    try:
        import streamlit
        import pandas
        print("✓ Dependencies are installed")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return
    
    # Ask user what to do
    print("\nChoose an option:")
    print("1. Run tests")
    print("2. Start the application")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice in ["1", "3"]:
        if not run_tests():
            print("Tests failed. Please fix the issues before running the application.")
            if choice == "1":
                return
    
    if choice in ["2", "3"]:
        print("\nStarting FINS ERP System...")
        try:
            # Run the Streamlit app without AI
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", "app_noai.py",
                "--server.port", "8501",
                "--server.address", "localhost"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running the application: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nApplication stopped by user")
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main() 
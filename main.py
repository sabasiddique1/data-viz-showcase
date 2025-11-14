#!/usr/bin/env python3
"""
Main entry point for the Python Mega Project
Provides a menu-driven interface to access all modules
"""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def show_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("Python Mega Project - Main Menu")
    print("="*50)
    print("1. Hurricane Analysis")
    print("2. Medical System")
    print("3. Quiz Modules")
    print("4. Cipher Tools")
    print("5. Exit")
    print("="*50)

def run_hurricane_analysis():
    """Run the hurricane analysis module"""
    try:
        from hurricane_analysis import main as hurricane_main
        hurricane_main()
    except ImportError:
        print("Hurricane analysis module not yet implemented.")
    except Exception as e:
        print(f"Error running hurricane analysis: {e}")

def run_medical_system():
    """Run the medical system module"""
    try:
        from medical_system import main as medical_main
        medical_main()
    except ImportError:
        print("Medical system module not yet implemented.")
    except Exception as e:
        print(f"Error running medical system: {e}")

def run_quiz_modules():
    """Run the quiz modules"""
    try:
        from quiz_modules import main as quiz_main
        quiz_main()
    except ImportError:
        print("Quiz modules not yet implemented.")
    except Exception as e:
        print(f"Error running quiz modules: {e}")

def run_cipher_tools():
    """Run the cipher tools module"""
    try:
        from cipher_tools import main as cipher_main
        cipher_main()
    except ImportError:
        print("Cipher tools module not yet implemented.")
    except Exception as e:
        print(f"Error running cipher tools: {e}")

def main():
    """Main function"""
    print("Welcome to Python Mega Project!")
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            run_hurricane_analysis()
        elif choice == '2':
            run_medical_system()
        elif choice == '3':
            run_quiz_modules()
        elif choice == '4':
            run_cipher_tools()
        elif choice == '5':
            print("\nThank you for using Python Mega Project. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")
        
        if choice != '5':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

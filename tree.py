#!/usr/bin/env python3
"""
Directory Tree Visualizer - Quick Launch Script
Simple entry point for the Directory Tree Visualizer
"""

import sys
import os

def main():
    """Quick launcher for Directory Tree Visualizer"""
    print("🌳 Directory Tree Visualizer - Quick Launch")
    print("=" * 50)
    
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        # If arguments provided, run console mode directly
        print("📋 Running in console mode with provided arguments...")
        try:
            from tree_console import main as console_main
            console_main()
        except ImportError:
            print("❌ Console module not found. Make sure tree_console.py is in the same directory.")
        except Exception as e:
            print(f"❌ Error running console mode: {e}")
    else:
        # No arguments, show launcher menu
        print("Choose your interface:")
        print("1. 🖥️  GUI Mode")
        print("2. 💻 Console Mode") 
        print("3. 🧪 Run Tests")
        print("4. 🚪 Exit")
        
        while True:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == '1':
                try:
                    from directory_tree_gui import main as gui_main
                    gui_main()
                    break
                except ImportError:
                    print("❌ GUI module not found. Make sure directory_tree_gui.py is in the same directory.")
                except Exception as e:
                    print(f"❌ Error launching GUI: {e}")
                    
            elif choice == '2':
                try:
                    from tree_launcher import launch_console
                    launch_console()
                    break
                except ImportError:
                    print("❌ Console launcher not found.")
                except Exception as e:
                    print(f"❌ Error launching console: {e}")
                    
            elif choice == '3':
                try:
                    from test_tree_visualizer import main as test_main
                    test_main()
                    break
                except ImportError:
                    print("❌ Test module not found.")
                except Exception as e:
                    print(f"❌ Error running tests: {e}")
                    
            elif choice == '4':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
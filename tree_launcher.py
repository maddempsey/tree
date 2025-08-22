#!/usr/bin/env python3
"""
Directory Tree Visualizer Launcher
Choose between GUI and console interfaces
"""

import sys
import os
import tkinter as tk
from pathlib import Path

def launch_gui():
    """Launch the GUI version"""
    try:
        # Import and run GUI
        from directory_tree_gui import DirectoryTreeGUI
        
        root = tk.Tk()
        app = DirectoryTreeGUI(root)
        
        # Center window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Error importing GUI components: {e}")
        print("Make sure all required files are in the same directory.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        input("Press Enter to exit...")

def launch_console():
    """Launch the console version"""
    try:
        print("🌳 Directory Tree Visualizer - Console Mode")
        print("=" * 50)
        
        # Get directory from user
        while True:
            path = input("\nEnter directory path to scan (or 'quit' to exit): ").strip()
            
            if path.lower() in ['quit', 'exit', 'q']:
                return
            
            if not path:
                path = "."  # Current directory
            
            if not os.path.exists(path):
                print(f"❌ Directory not found: {path}")
                continue
            
            if not os.path.isdir(path):
                print(f"❌ Not a directory: {path}")
                continue
            
            break
        
        # Get options
        print("\nScan Options:")
        max_depth_str = input("Maximum depth (press Enter for unlimited): ").strip()
        max_depth = int(max_depth_str) if max_depth_str else None
        
        show_hidden = input("Include hidden files? (y/N): ").strip().lower().startswith('y')
        include_files = not input("Directories only? (y/N): ").strip().lower().startswith('y')
        
        print("\nDisplay Options:")
        style = input("Tree style (unicode/ascii/simple) [unicode]: ").strip() or "unicode"
        show_size = not input("Hide sizes? (y/N): ").strip().lower().startswith('y')
        show_count = not input("Hide counts? (y/N): ").strip().lower().startswith('y')
        
        # Import and use the visualizer
        from directory_tree_visualizer import DirectoryTreeVisualizer
        
        visualizer = DirectoryTreeVisualizer()
        
        print(f"\n🔍 Scanning: {path}")
        visualizer.scan_directory(
            path, 
            max_depth=max_depth,
            show_hidden=show_hidden,
            include_files=include_files
        )
        
        # Display tree
        tree_text = visualizer.render_text_tree(
            style=style,
            show_size=show_size,
            show_count=show_count
        )
        
        print("\n" + tree_text)
        
        # Offer to save
        save_path = input(f"\nSave to file? (Enter filename or press Enter to skip): ").strip()
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(tree_text)
            print(f"💾 Saved to: {save_path}")
        
        print(f"\n📊 Summary: {visualizer.file_count} files, "
              f"{visualizer.folder_count} folders, "
              f"{visualizer.format_size(visualizer.total_size)} total")
        
    except ImportError as e:
        print(f"❌ Error importing required modules: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        input("\nPress Enter to continue...")

def main():
    """Main launcher function"""
    while True:
        print("\n" + "=" * 60)
        print("🌳 Directory Tree Visualizer")
        print("=" * 60)
        print("Choose your interface:")
        print("1. 🖥️  GUI Mode (Graphical Interface)")
        print("2. 💻 Console Mode (Text Interface)")
        print("3. ❓ Help")
        print("4. 🚪 Exit")
        print("=" * 60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            launch_gui()
        elif choice == '2':
            launch_console()
        elif choice == '3':
            show_help()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

def show_help():
    """Show help information"""
    help_text = """
🌳 Directory Tree Visualizer Help
================================

This application helps you visualize folder structures in multiple formats.

🖥️ GUI Mode Features:
• Interactive graphical interface
• Real-time directory scanning
• Multiple export formats (Text, HTML, JSON)
• Filtering options (extensions, file sizes, depth)
• Visual progress indicators

💻 Console Mode Features:  
• Fast text-based interface
• Command-line style operation
• Perfect for scripting and automation
• Multiple tree drawing styles

📁 Supported Features:
• Unlimited directory depth scanning
• File size and count statistics  
• Hidden file inclusion options
• File extension filtering
• Interactive HTML output with collapsible folders
• JSON export for data processing

🎨 Tree Styles:
• Unicode: Beautiful box-drawing characters
• ASCII: Compatible with all terminals
• Simple: Minimalist indentation-based

📊 Export Formats:
• Text: Human-readable tree structure
• HTML: Interactive web page with JavaScript
• JSON: Machine-readable data format

💡 Tips:
• Use file extension filters to focus on specific file types
• Set depth limits for large directory structures
• HTML export creates interactive trees you can share
• JSON export is perfect for further data analysis
"""
    print(help_text)
    input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)

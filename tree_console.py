#!/usr/bin/env python3
"""
Console-based Directory Tree Visualizer
Simple command-line interface for the directory tree visualizer
"""

import sys
import argparse
from pathlib import Path
from directory_tree_visualizer import DirectoryTreeVisualizer

def main():
    parser = argparse.ArgumentParser(
        description="🌳 Directory Tree Visualizer - Console Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tree_console.py C:\\Users\\mdemp\\Documents
  python tree_console.py /home/user/documents --max-depth 3
  python tree_console.py . --style ascii --no-files
  python tree_console.py . --extensions .py .txt --save tree.txt
        """
    )
    
    # Required arguments
    parser.add_argument('directory', help='Directory path to scan')
    
    # Scan options
    parser.add_argument('--max-depth', '-d', type=int, 
                       help='Maximum depth to scan')
    parser.add_argument('--hidden', action='store_true',
                       help='Include hidden files and folders')
    parser.add_argument('--no-files', action='store_true',
                       help='Only show directories, not files')
    parser.add_argument('--extensions', nargs='+',
                       help='Only include files with these extensions (e.g., .py .txt)')
    parser.add_argument('--min-size', type=float,
                       help='Minimum file size in MB')
    parser.add_argument('--max-size', type=float,
                       help='Maximum file size in MB')
    
    # Display options
    parser.add_argument('--style', choices=['unicode', 'ascii', 'simple'],
                       default='unicode', help='Tree drawing style')
    parser.add_argument('--no-size', action='store_true',
                       help='Hide file and folder sizes')
    parser.add_argument('--no-count', action='store_true',
                       help='Hide file and folder counts')
    parser.add_argument('--width', type=int, default=100,
                       help='Maximum line width')
    
    # Output options
    parser.add_argument('--save', help='Save output to file')
    parser.add_argument('--html', help='Save as interactive HTML file')
    parser.add_argument('--json', help='Save as JSON file')
    
    args = parser.parse_args()
    
    try:
        # Initialize visualizer
        visualizer = DirectoryTreeVisualizer()
        
        # Prepare scan options
        scan_options = {
            'max_depth': args.max_depth,
            'show_hidden': args.hidden,
            'include_files': not args.no_files
        }
        
        # Handle extensions
        if args.extensions:
            extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions]
            scan_options['extensions'] = extensions
        
        # Handle size filter
        if args.min_size or args.max_size:
            min_size = (args.min_size * 1024 * 1024) if args.min_size else 0
            max_size = (args.max_size * 1024 * 1024) if args.max_size else float('inf')
            scan_options['size_filter'] = (min_size, max_size)
        
        # Scan directory
        print(f"🔍 Scanning directory: {args.directory}")
        visualizer.scan_directory(args.directory, **scan_options)
        
        # Prepare display options
        display_options = {
            'style': args.style,
            'show_size': not args.no_size,
            'show_count': not args.no_count,
            'max_width': args.width
        }
        
        # Generate and display tree
        tree_text = visualizer.render_text_tree(**display_options)
        print(tree_text)
        
        # Save outputs if requested
        if args.save:
            with open(args.save, 'w', encoding='utf-8') as f:
                f.write(tree_text)
            print(f"\n💾 Tree saved to: {args.save}")
        
        if args.html:
            directory_name = Path(args.directory).name
            visualizer.export_html(args.html, f"Directory Tree - {directory_name}")
            print(f"\n🌐 Interactive HTML saved to: {args.html}")
        
        if args.json:
            visualizer.export_json(args.json)
            print(f"\n📄 JSON data saved to: {args.json}")
        
        # Show summary
        print(f"\n📊 Summary: {visualizer.file_count} files, "
              f"{visualizer.folder_count} folders, "
              f"{visualizer.format_size(visualizer.total_size)} total")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

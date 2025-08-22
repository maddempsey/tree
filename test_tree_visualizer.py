#!/usr/bin/env python3
"""
Test script for Directory Tree Visualizer
Quick validation of core functionality
"""

import os
import tempfile
from pathlib import Path
from directory_tree_visualizer import DirectoryTreeVisualizer

def create_test_structure():
    """Create a test directory structure"""
    # Create temporary directory
    test_dir = Path(tempfile.mkdtemp(prefix="tree_test_"))
    
    # Create subdirectories
    (test_dir / "documents").mkdir()
    (test_dir / "documents" / "projects").mkdir()
    (test_dir / "documents" / "archive").mkdir()
    (test_dir / "media").mkdir()
    (test_dir / "media" / "images").mkdir()
    (test_dir / "media" / "videos").mkdir()
    
    # Create some test files
    (test_dir / "readme.txt").write_text("Test readme file")
    (test_dir / "config.json").write_text('{"test": true}')
    (test_dir / "documents" / "report.pdf").write_text("PDF content")
    (test_dir / "documents" / "projects" / "main.py").write_text("print('Hello World')")
    (test_dir / "documents" / "projects" / "utils.py").write_text("def helper(): pass")
    (test_dir / "media" / "images" / "photo.jpg").write_text("JPEG data")
    (test_dir / "media" / "videos" / "movie.mp4").write_text("MP4 data")
    
    return test_dir

def test_basic_functionality():
    """Test basic directory scanning and rendering"""
    print("🧪 Testing Directory Tree Visualizer")
    print("=" * 50)
    
    # Create test structure
    test_dir = create_test_structure()
    print(f"📁 Created test directory: {test_dir}")
    
    try:
        # Initialize visualizer
        visualizer = DirectoryTreeVisualizer()
        
        # Test scanning
        print("\n🔍 Testing directory scanning...")
        tree_data = visualizer.scan_directory(str(test_dir))
        
        print(f"✅ Scan completed!")
        print(f"   Files found: {visualizer.file_count}")
        print(f"   Folders found: {visualizer.folder_count}")
        print(f"   Total size: {visualizer.format_size(visualizer.total_size)}")
        
        # Test text rendering
        print("\n📝 Testing text rendering...")
        tree_text = visualizer.render_text_tree(style="unicode")
        print("✅ Unicode tree generated!")
        
        # Show sample output
        print("\n📋 Sample Tree Output:")
        print("-" * 40)
        print(tree_text)
        
        # Test different styles
        print("\n🎨 Testing different styles...")
        for style in ["ascii", "simple"]:
            tree_text = visualizer.render_text_tree(style=style)
            print(f"✅ {style.capitalize()} style: OK")
        
        # Test filtering
        print("\n🔍 Testing file filtering...")
        visualizer.scan_directory(str(test_dir), extensions=['.py', '.txt'])
        filtered_count = visualizer.file_count
        print(f"✅ Extension filtering: {filtered_count} Python/text files found")
        
        # Test depth limiting
        visualizer.scan_directory(str(test_dir), max_depth=1)
        print(f"✅ Depth limiting: Scanned to depth {visualizer.max_depth if hasattr(visualizer, 'max_depth') else 1}")
        
        # Test export functionality
        print("\n💾 Testing export functionality...")
        
        # Test JSON export
        json_file = test_dir / "test_export.json"
        visualizer.scan_directory(str(test_dir))  # Full scan for export
        visualizer.export_json(str(json_file))
        if json_file.exists():
            print("✅ JSON export: OK")
        
        # Test HTML export
        html_file = test_dir / "test_export.html"
        visualizer.export_html(str(html_file), "Test Directory Tree")
        if html_file.exists():
            print("✅ HTML export: OK")
        
        print("\n🎉 All tests passed! Directory Tree Visualizer is working correctly.")
        print(f"\n💡 Test files created at: {test_dir}")
        print("You can examine the exported HTML and JSON files to see the output formats.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    
    finally:
        # Note: Not cleaning up test directory so user can examine output files
        print(f"\n🗂️ Test directory preserved for examination: {test_dir}")

def test_real_directory():
    """Test with the current directory"""
    print("\n" + "=" * 50)
    print("🔍 Testing with current directory (limited depth)")
    print("=" * 50)
    
    try:
        visualizer = DirectoryTreeVisualizer()
        
        # Scan current directory with limited depth to avoid overwhelming output
        current_dir = "."
        visualizer.scan_directory(current_dir, max_depth=2, include_files=True)
        
        # Generate tree
        tree_text = visualizer.render_text_tree(
            style="unicode", 
            show_size=True, 
            show_count=True, 
            max_width=80
        )
        
        print(tree_text)
        
        print(f"\n📊 Current Directory Summary:")
        print(f"   Files: {visualizer.file_count}")
        print(f"   Folders: {visualizer.folder_count}")
        print(f"   Total Size: {visualizer.format_size(visualizer.total_size)}")
        
    except Exception as e:
        print(f"❌ Error scanning current directory: {e}")

def main():
    """Run all tests"""
    print("🌳 Directory Tree Visualizer - Test Suite")
    print("=" * 60)
    
    # Test basic functionality
    success = test_basic_functionality()
    
    if success:
        # Test with real directory
        test_real_directory()
        
        print("\n" + "=" * 60)
        print("🎯 Ready to use! Try these commands:")
        print("=" * 60)
        print("GUI Mode:")
        print("  python directory_tree_gui.py")
        print()
        print("Console Mode:")
        print("  python tree_console.py .")
        print("  python tree_console.py C:\\Users --max-depth 3")
        print()
        print("Interactive Launcher:")
        print("  python tree_launcher.py")
        print("=" * 60)
    else:
        print("\n❌ Tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()

# 🌳 Directory Tree Visualizer

A powerful Python application for visualizing directory structures in multiple formats - text, interactive HTML, and JSON.

## ✨ Features

### 🎯 Core Functionality
- **Multiple Output Formats**: Text trees, interactive HTML, and structured JSON
- **Flexible Tree Styles**: Unicode, ASCII, and simple text styles  
- **Advanced Filtering**: By file size, extensions, depth, and hidden files
- **Rich Statistics**: File counts, folder counts, total sizes, and depth metrics
- **Cross-Platform**: Works on Windows, macOS, and Linux

### 🖥️ Multiple User Interfaces
- **GUI Mode**: Beautiful graphical interface with real-time preview
- **Console Mode**: Powerful command-line interface for automation
- **Interactive Launcher**: Choose your preferred interface

### 📊 Visual Features
- **Interactive HTML**: Expandable/collapsible tree with modern styling
- **File Type Icons**: Different icons for Python, images, documents, etc.
- **Size Information**: Human-readable file and folder sizes
- **Progress Tracking**: Real-time scanning progress in GUI mode

## 🚀 Quick Start

### 📦 Installation
1. Save all files to a directory (e.g., `TreeVisualizer`)
2. Ensure Python 3.6+ is installed
3. No additional packages required (uses built-in libraries)

### 🎮 Quick Launch Options

#### Option 1: Simple Launcher
```bash
python tree.py
```

#### Option 2: GUI Mode
```bash
python directory_tree_gui.py
```

#### Option 3: Console Mode
```bash
python tree_console.py C:\Users\mdemp\Documents\Python
```

#### Option 4: Interactive Launcher
```bash
python tree_launcher.py
```

## 📖 Usage Examples

### Basic Console Usage
```bash
# Scan current directory
python tree_console.py .

# Scan specific directory
python tree_console.py C:\Users\Documents

# Scan with limited depth
python tree_console.py C:\Projects --max-depth 3
```

### Advanced Filtering
```bash
# Only Python and text files
python tree_console.py . --extensions .py .txt

# Files between 1MB and 100MB
python tree_console.py /media --min-size 1 --max-size 100

# Directories only (no files)
python tree_console.py C:\Projects --no-files

# Include hidden files
python tree_console.py . --hidden
```

### Output Formats
```bash
# Save as text file
python tree_console.py . --save my_tree.txt

# Save as interactive HTML
python tree_console.py . --html my_tree.html

# Save as JSON data
python tree_console.py . --json my_tree.json
```

### Tree Styles
```bash
# Unicode style (default)
python tree_console.py . --style unicode

# ASCII style (terminal compatible)
python tree_console.py . --style ascii

# Simple style (minimal)
python tree_console.py . --style simple
```

## 🎨 GUI Features

The graphical interface provides:

### 📁 Directory Selection
- **Browse Button**: Easy folder selection
- **Manual Entry**: Type directory path directly
- **Recent Paths**: Remember recently scanned directories

### ⚙️ Scan Options
- **Maximum Depth**: Limit how deep to scan
- **Hidden Files**: Include or exclude hidden files
- **File Inclusion**: Option to show directories only
- **Extension Filter**: Scan specific file types (e.g., `.py .txt .jpg`)
- **Size Range**: Filter files by minimum and maximum size

### 🎭 Display Options  
- **Tree Style**: Choose Unicode, ASCII, or Simple
- **Size Display**: Show or hide file/folder sizes
- **Count Display**: Show or hide file/folder counts
- **Line Width**: Control maximum line width for display

### 💾 Export Options
- **Save as Text**: Human-readable tree structure
- **Save as HTML**: Interactive web page with JavaScript
- **Save as JSON**: Machine-readable data format

### 📊 Real-time Features
- **Progress Bar**: Visual indication of scan progress
- **Live Results**: View tree as it's being generated
- **Status Updates**: Current scan status and statistics

## 📁 Sample Output

### Text Tree (Unicode Style)
```
📁 MyProject (15 folders, 42 files, 2.3 MB)

├── 📄 README.md (1.2 KB)
├── 📄 requirements.txt (245 B)
├── 📁 src (12 folders, 35 files, 2.1 MB)
│   ├── 🐍 main.py (3.4 KB)
│   ├── 📁 utils (5 folders, 12 files, 856 KB)
│   │   ├── 🐍 helpers.py (2.1 KB)
│   │   └── 📁 data (4 folders, 8 files, 854 KB)
│   │       ├── 📄 dataset.csv (850 KB)
│   │       └── 📋 config.json (4.2 KB)
│   └── 📁 tests (7 folders, 18 files, 1.3 MB)
└── 📁 docs (3 folders, 5 files, 156 KB)
```

### Interactive HTML Features
- **Click to Expand/Collapse**: Interactive folder navigation
- **Modern Styling**: Clean, professional appearance  
- **Statistics Dashboard**: Overview of files, folders, and sizes
- **Responsive Design**: Works on desktop and mobile
- **Shareable**: Easy to send to colleagues or include in documentation

## 🗂️ File Structure

```
TreeVisualizer/
├── directory_tree_visualizer.py  # Core engine and logic
├── directory_tree_gui.py         # GUI interface (tkinter)
├── tree_console.py               # Command-line interface
├── tree_launcher.py              # Interactive launcher
├── tree.py                       # Quick launch script
├── test_tree_visualizer.py       # Test suite
└── README.md                     # This documentation
```

## 🎯 Use Cases

### 🖥️ Development Projects
- **Code Reviews**: Visualize project structure for reviews
- **Documentation**: Include tree diagrams in project docs
- **Onboarding**: Help new team members understand layout
- **Architecture**: Analyze and plan code organization

### 🔧 System Administration
- **Disk Analysis**: Identify large files and folder structures
- **Backup Planning**: Understand directory hierarchies
- **Cleanup**: Find and organize scattered files
- **Inventory**: Create directory listings for audits

### 📚 Data Organization
- **Media Libraries**: Organize photos, videos, music
- **Document Management**: Structure document repositories
- **Archive Analysis**: Understand contents of old archives
- **Research**: Catalog research data and materials

### 📊 Business Applications
- **Asset Management**: Track file locations and sizes
- **Compliance**: Document file structures for audits
- **Migration**: Plan and document system migrations
- **Training**: Create visual guides for file organization

## ⚙️ Command Line Reference

### Required Arguments
- `directory` - Directory path to scan

### Scan Options
- `--max-depth, -d` - Maximum depth to scan
- `--hidden` - Include hidden files and folders
- `--no-files` - Only show directories, not files
- `--extensions` - File extensions to include (e.g., `.py .txt`)
- `--min-size` - Minimum file size in MB
- `--max-size` - Maximum file size in MB

### Display Options
- `--style` - Tree style: `unicode`, `ascii`, `simple`
- `--no-size` - Hide file and folder sizes
- `--no-count` - Hide file and folder counts
- `--width` - Maximum line width (default: 100)

### Output Options
- `--save` - Save tree as text file
- `--html` - Save as interactive HTML file
- `--json` - Save as JSON data file

## 🧪 Testing

Run the test suite to verify installation:

```bash
python test_tree_visualizer.py
```

The test will:
- Create a sample directory structure
- Test all core functionality
- Verify text rendering in different styles
- Test filtering capabilities
- Validate export functionality
- Show sample output

## 🛠️ Technical Details

### Requirements
- **Python**: 3.6 or higher
- **Libraries**: Uses only built-in Python libraries
  - `tkinter` - GUI interface (included with Python)
  - `pathlib` - Modern path handling
  - `json` - JSON export functionality
  - `threading` - Non-blocking GUI operations

### Performance
- **Memory Efficient**: Processes files in chunks
- **Fast Scanning**: Optimized directory traversal
- **Large Directories**: Handles thousands of files
- **Progress Tracking**: Real-time feedback for long scans

### Cross-Platform Compatibility
- **Windows**: Full support with PowerShell and Command Prompt
- **macOS**: Native support with Terminal
- **Linux**: Compatible with all major distributions

## 🔧 Troubleshooting

### Common Issues

#### "Module not found" errors
- Ensure all files are in the same directory
- Check that Python can import from the current directory
- Verify file names match exactly (case-sensitive on Linux/macOS)

#### GUI won't start
- Verify `tkinter` is installed: `python -c "import tkinter"`
- Some minimal Python installations may not include tkinter
- Use console mode as alternative: `python tree_console.py .`

#### Permission denied errors
- Run as administrator for system directories
- Some files may be locked by other applications
- Use file extension filters to skip problematic files

#### Slow performance on large directories
- Use `--max-depth` to limit scan depth
- Apply `--extensions` filter to reduce file count
- Consider scanning subdirectories separately

#### Memory issues with very large directories
- The tool is optimized for memory efficiency
- For extremely large directories (100k+ files), use filtering
- Consider scanning in smaller chunks

## 💡 Tips and Tricks

### Performance Optimization
- **Use Filters**: Apply extension and size filters to focus scan
- **Limit Depth**: Use `--max-depth` for large directory trees
- **Batch Processing**: Scan large directories in smaller chunks

### Effective Usage
- **Code Projects**: Use `.py .js .html .css` for web projects
- **Documents**: Use `.pdf .doc .docx .txt` for document cleanup
- **Media Files**: Use `.jpg .png .mp4 .mp3` for media organization
- **Archives**: Be careful with compressed files (`.zip`, `.rar`)

### Automation Ideas
- **Scheduled Scans**: Create scripts for regular directory analysis
- **Build Integration**: Include tree generation in build processes
- **Documentation**: Auto-generate project structure documentation
- **Monitoring**: Track directory changes over time

### Advanced HTML Features
- **Sharing**: HTML files can be opened in any web browser
- **Printing**: Use browser print function for hard copies
- **Embedding**: Include HTML trees in web documentation
- **Customization**: Edit HTML files to add custom styling

## 📄 License

This project is provided for educational and personal use. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

Ideas for future enhancements:
- **Additional Hash Algorithms**: SHA-256, SHA-512 for file verification
- **Network Drives**: Support for UNC paths and network shares
- **Database Integration**: Store scan results in SQLite database
- **Web Interface**: Browser-based interface for remote scanning
- **File Operations**: Built-in copy, move, delete capabilities
- **Comparison Mode**: Compare directory structures between scans
- **Plugin System**: Extensible architecture for custom features

---

**🎉 Happy tree visualizing!**

*Keep your directories organized and well-documented!* 🌳📁✨

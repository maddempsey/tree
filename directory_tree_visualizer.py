import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

class DirectoryTreeVisualizer:
    """
    A comprehensive directory tree visualizer that can render folder structures
    in multiple formats including text, HTML, and JSON.
    """
    
    def __init__(self):
        self.tree_data = None
        self.root_path = None
        self.file_count = 0
        self.folder_count = 0
        self.total_size = 0
        
        # Tree rendering styles
        self.styles = {
            'unicode': {
                'branch': '├── ',
                'last': '└── ',
                'vertical': '│   ',
                'space': '    '
            },
            'ascii': {
                'branch': '|-- ',
                'last': '`-- ',
                'vertical': '|   ',
                'space': '    '
            },
            'simple': {
                'branch': '  ',
                'last': '  ',
                'vertical': '  ',
                'space': '  '
            }
        }
    
    def scan_directory(self, path: str, max_depth: Optional[int] = None, 
                      show_hidden: bool = False, include_files: bool = True,
                      extensions: Optional[List[str]] = None,
                      size_filter: Optional[Tuple[float, float]] = None) -> Dict:
        """
        Scan a directory and build a tree structure.
        
        Args:
            path: Root directory path to scan
            max_depth: Maximum depth to scan (None for unlimited)
            show_hidden: Include hidden files and folders
            include_files: Include files in the tree
            extensions: List of file extensions to include (e.g., ['.py', '.txt'])
            size_filter: Tuple of (min_size, max_size) in bytes
        
        Returns:
            Dictionary representing the directory tree
        """
        self.root_path = Path(path).resolve()
        self.file_count = 0
        self.folder_count = 0
        self.total_size = 0
        
        if not self.root_path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        
        if not self.root_path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        
        self.tree_data = self._scan_recursive(
            self.root_path, 0, max_depth, show_hidden, 
            include_files, extensions, size_filter
        )
        
        return self.tree_data
    
    def _scan_recursive(self, path: Path, current_depth: int, max_depth: Optional[int],
                       show_hidden: bool, include_files: bool, 
                       extensions: Optional[List[str]], 
                       size_filter: Optional[Tuple[float, float]]) -> Dict:
        """Recursively scan directory structure"""
        
        node = {
            'name': path.name,
            'path': str(path),
            'type': 'directory',
            'size': 0,
            'children': [],
            'file_count': 0,
            'folder_count': 0
        }
        
        # Check depth limit
        if max_depth is not None and current_depth >= max_depth:
            return node
        
        try:
            items = list(path.iterdir())
            
            # Sort items (directories first, then files)
            items.sort(key=lambda x: (x.is_file(), x.name.lower()))
            
            for item in items:
                # Skip hidden files if not requested
                if not show_hidden and item.name.startswith('.'):
                    continue
                
                if item.is_dir():
                    # Recursively scan subdirectory
                    child_node = self._scan_recursive(
                        item, current_depth + 1, max_depth, show_hidden,
                        include_files, extensions, size_filter
                    )
                    
                    node['children'].append(child_node)
                    node['size'] += child_node['size']
                    node['file_count'] += child_node['file_count']
                    node['folder_count'] += child_node['folder_count'] + 1
                    self.folder_count += 1
                    
                elif include_files and item.is_file():
                    # Get file info
                    try:
                        file_size = item.stat().st_size
                        
                        # Apply extension filter
                        if extensions and item.suffix.lower() not in [ext.lower() for ext in extensions]:
                            continue
                        
                        # Apply size filter
                        if size_filter:
                            min_size, max_size = size_filter
                            if file_size < min_size or file_size > max_size:
                                continue
                        
                        file_node = {
                            'name': item.name,
                            'path': str(item),
                            'type': 'file',
                            'size': file_size,
                            'extension': item.suffix,
                            'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                        }
                        
                        node['children'].append(file_node)
                        node['size'] += file_size
                        node['file_count'] += 1
                        self.file_count += 1
                        self.total_size += file_size
                        
                    except (OSError, PermissionError):
                        # Skip files we can't access
                        continue
                        
        except (OSError, PermissionError):
            # Skip directories we can't access
            pass
        
        return node
    
    def render_text_tree(self, style: str = 'unicode', show_size: bool = True,
                        show_count: bool = True, max_width: int = 100) -> str:
        """
        Render the tree as formatted text.
        
        Args:
            style: Tree style ('unicode', 'ascii', 'simple')
            show_size: Show file/folder sizes
            show_count: Show file/folder counts
            max_width: Maximum line width
        
        Returns:
            Formatted tree as string
        """
        if not self.tree_data:
            return "No tree data available. Please scan a directory first."
        
        style_chars = self.styles.get(style, self.styles['unicode'])
        lines = []
        
        # Add header
        root_name = self.tree_data['name'] or str(self.root_path)
        header = f"📁 {root_name}"
        
        if show_count:
            header += f" ({self.folder_count} folders, {self.file_count} files"
            if show_size:
                header += f", {self.format_size(self.total_size)}"
            header += ")"
        elif show_size:
            header += f" ({self.format_size(self.total_size)})"
        
        lines.append(header)
        lines.append("")
        
        # Render tree
        self._render_node_text(
            self.tree_data, "", True, style_chars, show_size, 
            show_count, max_width, lines
        )
        
        return "\n".join(lines)
    
    def _render_node_text(self, node: Dict, prefix: str, is_last: bool,
                         style_chars: Dict, show_size: bool, show_count: bool,
                         max_width: int, lines: List[str]):
        """Recursively render tree nodes as text"""
        
        if node['type'] == 'directory':
            icon = "📁"
            name = node['name']
            
            # Add size/count info for directories
            info_parts = []
            if show_count and 'file_count' in node:
                total_items = node['file_count'] + node.get('folder_count', 0)
                if total_items > 0:
                    info_parts.append(f"{total_items} items")
            
            if show_size and node['size'] > 0:
                info_parts.append(self.format_size(node['size']))
            
            if info_parts:
                name += f" ({', '.join(info_parts)})"
        else:
            # Determine file icon based on extension
            icon = self._get_file_icon(node.get('extension', ''))
            name = node['name']
            
            if show_size:
                name += f" ({self.format_size(node['size'])})"
        
        # Create line with proper prefix
        connector = style_chars['last'] if is_last else style_chars['branch']
        line = f"{prefix}{connector}{icon} {name}"
        
        # Truncate if too long
        if len(line) > max_width:
            line = line[:max_width-3] + "..."
        
        lines.append(line)
        
        # Render children for directories
        if node['type'] == 'directory' and 'children' in node:
            children = node['children']
            if children:
                new_prefix = prefix + (style_chars['space'] if is_last else style_chars['vertical'])
                
                for i, child in enumerate(children):
                    child_is_last = (i == len(children) - 1)
                    self._render_node_text(
                        child, new_prefix, child_is_last, style_chars,
                        show_size, show_count, max_width, lines
                    )
    
    def _get_file_icon(self, extension: str) -> str:
        """Get appropriate icon for file extension"""
        extension = extension.lower()
        
        icon_map = {
            '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨',
            '.jpg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.svg': '🖼️',
            '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬', '.mov': '🎬',
            '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵', '.ogg': '🎵',
            '.pdf': '📄', '.doc': '📝', '.docx': '📝', '.txt': '📄',
            '.zip': '📦', '.rar': '📦', '.7z': '📦', '.tar': '📦',
            '.exe': '⚙️', '.msi': '⚙️', '.deb': '⚙️', '.rpm': '⚙️',
            '.json': '📋', '.xml': '📋', '.yml': '📋', '.yaml': '📋',
            '.md': '📖', '.readme': '📖'
        }
        
        return icon_map.get(extension, '📄')
    
    def export_html(self, filename: str, title: str = "Directory Tree"):
        """Export tree as interactive HTML"""
        if not self.tree_data:
            raise ValueError("No tree data available")
        
        html_content = self._generate_html(title)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_html(self, title: str) -> str:
        """Generate HTML content for the tree"""
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Consolas', 'Monaco', monospace;
            line-height: 1.4;
            margin: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .tree-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-height: 80vh;
            overflow: auto;
        }}
        .tree-node {{
            margin: 2px 0;
            cursor: pointer;
            transition: background-color 0.2s;
        }}
        .tree-node:hover {{
            background-color: #e9ecef;
            border-radius: 4px;
        }}
        .tree-node.directory {{
            font-weight: bold;
            color: #495057;
        }}
        .tree-node.file {{
            color: #6c757d;
        }}
        .tree-toggle {{
            display: inline-block;
            width: 20px;
            text-align: center;
            cursor: pointer;
            user-select: none;
        }}
        .tree-icon {{
            margin-right: 5px;
        }}
        .tree-name {{
            color: #212529;
        }}
        .tree-size {{
            color: #6c757d;
            font-size: 0.9em;
            margin-left: 10px;
        }}
        .tree-children {{
            margin-left: 20px;
            border-left: 1px dotted #dee2e6;
            padding-left: 10px;
        }}
        .collapsed {{
            display: none;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin-top: 10px;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌳 {title}</h1>
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{self.folder_count}</div>
                <div class="stat-label">Folders</div>
            </div>
            <div class="stat">
                <div class="stat-value">{self.file_count}</div>
                <div class="stat-label">Files</div>
            </div>
            <div class="stat">
                <div class="stat-value">{self.format_size(self.total_size)}</div>
                <div class="stat-label">Total Size</div>
            </div>
        </div>
    </div>
    
    <div class="tree-container">
        <div class="tree-node directory" onclick="toggleNode(this)">
            <span class="tree-toggle">📁</span>
            <span class="tree-name">{self.tree_data['name'] or 'Root'}</span>
            <span class="tree-size">({self.format_size(self.tree_data['size'])})</span>
        </div>
        <div class="tree-children">
            {self._render_html_children(self.tree_data.get('children', []))}
        </div>
    </div>

    <script>
        function toggleNode(element) {{
            const children = element.nextElementSibling;
            const toggle = element.querySelector('.tree-toggle');
            
            if (children && children.classList.contains('tree-children')) {{
                if (children.classList.contains('collapsed')) {{
                    children.classList.remove('collapsed');
                    toggle.textContent = element.classList.contains('directory') ? '📁' : '📄';
                }} else {{
                    children.classList.add('collapsed');
                    toggle.textContent = '📁';
                }}
            }}
        }}
        
        // Auto-expand first few levels
        document.addEventListener('DOMContentLoaded', function() {{
            const topLevelNodes = document.querySelectorAll('.tree-children > .tree-node.directory');
            topLevelNodes.forEach((node, index) => {{
                if (index < 3) {{ // Expand first 3 directories
                    toggleNode(node);
                }}
            }});
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def _render_html_children(self, children: List[Dict]) -> str:
        """Render children nodes as HTML"""
        if not children:
            return ""
        
        html_parts = []
        
        for child in children:
            if child['type'] == 'directory':
                icon = '📁'
                class_name = 'directory'
                onclick = 'onclick="toggleNode(this)"'
                size_info = f"({len(child.get('children', []))} items, {self.format_size(child['size'])})"
                
                child_html = f"""
                <div class="tree-node {class_name}" {onclick}>
                    <span class="tree-toggle">{icon}</span>
                    <span class="tree-name">{child['name']}</span>
                    <span class="tree-size">{size_info}</span>
                </div>"""
                
                if child.get('children'):
                    child_html += f"""
                    <div class="tree-children collapsed">
                        {self._render_html_children(child['children'])}
                    </div>"""
            else:
                icon = self._get_file_icon(child.get('extension', ''))
                class_name = 'file'
                size_info = f"({self.format_size(child['size'])})"
                
                child_html = f"""
                <div class="tree-node {class_name}">
                    <span class="tree-toggle"> </span>
                    <span class="tree-icon">{icon}</span>
                    <span class="tree-name">{child['name']}</span>
                    <span class="tree-size">{size_info}</span>
                </div>"""
            
            html_parts.append(child_html)
        
        return "".join(html_parts)
    
    def export_json(self, filename: str):
        """Export tree data as JSON"""
        if not self.tree_data:
            raise ValueError("No tree data available")
        
        export_data = {
            'scan_info': {
                'root_path': str(self.root_path),
                'scan_time': datetime.now().isoformat(),
                'total_files': self.file_count,
                'total_folders': self.folder_count,
                'total_size': self.total_size
            },
            'tree_data': self.tree_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

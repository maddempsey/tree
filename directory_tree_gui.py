import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
from datetime import datetime
from directory_tree_visualizer import DirectoryTreeVisualizer

class DirectoryTreeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌳 Directory Tree Visualizer")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Variables
        self.visualizer = DirectoryTreeVisualizer()
        self.selected_directory = tk.StringVar()
        self.scan_thread = None
        self.is_scanning = False
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = tk.Label(main_frame, text="🌳 Directory Tree Visualizer", 
                              font=('Arial', 18, 'bold'), fg='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Directory selection
        dir_frame = ttk.LabelFrame(main_frame, text="Select Directory", padding="10")
        dir_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(0, weight=1)
        
        dir_entry_frame = ttk.Frame(dir_frame)
        dir_entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        dir_entry_frame.columnconfigure(0, weight=1)
        
        self.dir_entry = ttk.Entry(dir_entry_frame, textvariable=self.selected_directory, width=60)
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(dir_entry_frame, text="Browse", 
                  command=self.browse_directory).grid(row=0, column=1)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Scan Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Options - Row 1
        options_row1 = ttk.Frame(options_frame)
        options_row1.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Max depth
        ttk.Label(options_row1, text="Max Depth:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.max_depth_var = tk.StringVar(value="")
        max_depth_spin = ttk.Spinbox(options_row1, from_=1, to=20, width=5, textvariable=self.max_depth_var)
        max_depth_spin.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Show hidden
        self.show_hidden_var = tk.BooleanVar()
        ttk.Checkbutton(options_row1, text="Include Hidden Files", 
                       variable=self.show_hidden_var).grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        
        # Include files
        self.include_files_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_row1, text="Include Files", 
                       variable=self.include_files_var).grid(row=0, column=3, sticky=tk.W)
        
        # Options - Row 2
        options_row2 = ttk.Frame(options_frame)
        options_row2.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # File extensions
        ttk.Label(options_row2, text="Extensions:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.extensions_var = tk.StringVar()
        ttk.Entry(options_row2, textvariable=self.extensions_var, width=30).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Size filter
        ttk.Label(options_row2, text="Min Size (MB):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.min_size_var = tk.StringVar()
        ttk.Entry(options_row2, textvariable=self.min_size_var, width=10).grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(options_row2, text="Max Size (MB):").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.max_size_var = tk.StringVar()
        ttk.Entry(options_row2, textvariable=self.max_size_var, width=10).grid(row=0, column=5, sticky=tk.W)
        
        # Display options
        display_frame = ttk.LabelFrame(main_frame, text="Display Options", padding="10")
        display_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        display_row = ttk.Frame(display_frame)
        display_row.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Tree style
        ttk.Label(display_row, text="Style:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.style_var = tk.StringVar(value="unicode")
        style_combo = ttk.Combobox(display_row, textvariable=self.style_var, 
                                  values=["unicode", "ascii", "simple"], state="readonly", width=10)
        style_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Show options
        self.show_size_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(display_row, text="Show Sizes", 
                       variable=self.show_size_var).grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        
        self.show_count_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(display_row, text="Show Counts", 
                       variable=self.show_count_var).grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # Max width
        ttk.Label(display_row, text="Max Width:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.max_width_var = tk.StringVar(value="100")
        ttk.Entry(display_row, textvariable=self.max_width_var, width=5).grid(row=0, column=5, sticky=tk.W)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(side=tk.TOP, pady=(0, 10))
        
        self.scan_button = ttk.Button(buttons_frame, text="🔍 Scan Directory", 
                                     command=self.start_scan)
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(buttons_frame, text="⏹ Stop Scan", 
                                     command=self.stop_scan, state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_text_button = ttk.Button(buttons_frame, text="💾 Save as Text", 
                                          command=self.save_text, state='disabled')
        self.save_text_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_html_button = ttk.Button(buttons_frame, text="🌐 Save as HTML", 
                                          command=self.save_html, state='disabled')
        self.save_html_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_json_button = ttk.Button(buttons_frame, text="📄 Save as JSON", 
                                          command=self.save_json, state='disabled')
        self.save_json_button.pack(side=tk.LEFT)
        
        # Progress and results
        results_frame = ttk.LabelFrame(control_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(results_frame, length=400, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Results text
        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, wrap=tk.WORD, 
                                                     font=('Consolas', 9))
        self.results_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready to scan", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def browse_directory(self):
        """Browse for directory to scan"""
        directory = filedialog.askdirectory(title="Select Directory to Scan")
        if directory:
            self.selected_directory.set(directory)
            
    def get_scan_options(self):
        """Get scan options from GUI"""
        options = {}
        
        # Max depth
        max_depth_str = self.max_depth_var.get().strip()
        options['max_depth'] = int(max_depth_str) if max_depth_str else None
        
        # Boolean options
        options['show_hidden'] = self.show_hidden_var.get()
        options['include_files'] = self.include_files_var.get()
        
        # Extensions
        extensions_str = self.extensions_var.get().strip()
        if extensions_str:
            extensions = [ext.strip() for ext in extensions_str.split() if ext.strip()]
            options['extensions'] = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        else:
            options['extensions'] = None
        
        # Size filter
        min_size_str = self.min_size_var.get().strip()
        max_size_str = self.max_size_var.get().strip()
        
        if min_size_str or max_size_str:
            min_size = float(min_size_str) * 1024 * 1024 if min_size_str else 0
            max_size = float(max_size_str) * 1024 * 1024 if max_size_str else float('inf')
            options['size_filter'] = (min_size, max_size)
        else:
            options['size_filter'] = None
        
        return options
    
    def get_display_options(self):
        """Get display options from GUI"""
        return {
            'style': self.style_var.get(),
            'show_size': self.show_size_var.get(),
            'show_count': self.show_count_var.get(),
            'max_width': int(self.max_width_var.get()) if self.max_width_var.get().strip() else 100
        }
    
    def start_scan(self):
        """Start directory scan"""
        directory = self.selected_directory.get().strip()
        if not directory:
            messagebox.showwarning("Warning", "Please select a directory to scan!")
            return
        
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Selected directory does not exist!")
            return
        
        if self.is_scanning:
            messagebox.showwarning("Warning", "A scan is already in progress!")
            return
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        
        # Update UI
        self.scan_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.save_text_button.config(state='disabled')
        self.save_html_button.config(state='disabled')
        self.save_json_button.config(state='disabled')
        
        self.progress_bar.start()
        self.status_bar.config(text="Scanning directory...")
        self.is_scanning = True
        
        # Get options
        scan_options = self.get_scan_options()
        display_options = self.get_display_options()
        
        # Start scan in separate thread
        self.scan_thread = threading.Thread(
            target=self._run_scan,
            args=(directory, scan_options, display_options),
            daemon=True
        )
        self.scan_thread.start()
    
    def _run_scan(self, directory, scan_options, display_options):
        """Run scan in separate thread"""
        try:
            # Scan directory
            self.visualizer.scan_directory(directory, **scan_options)
            
            # Generate text tree
            tree_text = self.visualizer.render_text_tree(**display_options)
            
            # Update UI
            self.root.after(0, self._scan_completed, tree_text)
            
        except Exception as e:
            self.root.after(0, self._scan_error, str(e))
    
    def _scan_completed(self, tree_text):
        """Handle scan completion"""
        self.is_scanning = False
        
        # Update UI
        self.scan_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.save_text_button.config(state='normal')
        self.save_html_button.config(state='normal')
        self.save_json_button.config(state='normal')
        
        self.progress_bar.stop()
        
        # Show results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, tree_text)
        
        # Update status
        self.status_bar.config(text=f"Scan completed: {self.visualizer.file_count} files, "
                                   f"{self.visualizer.folder_count} folders, "
                                   f"{self.visualizer.format_size(self.visualizer.total_size)}")
    
    def _scan_error(self, error_message):
        """Handle scan error"""
        self.is_scanning = False
        
        # Update UI
        self.scan_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress_bar.stop()
        
        self.status_bar.config(text=f"Scan failed: {error_message}")
        messagebox.showerror("Scan Error", f"An error occurred during scanning:\n{error_message}")
    
    def stop_scan(self):
        """Stop current scan"""
        self.is_scanning = False
        self.scan_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress_bar.stop()
        self.status_bar.config(text="Scan stopped by user")
    
    def save_text(self):
        """Save tree as text file"""
        if not self.visualizer.tree_data:
            messagebox.showinfo("Info", "No tree data to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Tree as Text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialname=f"directory_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                display_options = self.get_display_options()
                tree_text = self.visualizer.render_text_tree(**display_options)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(tree_text)
                
                messagebox.showinfo("Success", f"Tree saved to:\n{filename}")
                self.status_bar.config(text=f"Tree saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save tree:\n{e}")
    
    def save_html(self):
        """Save tree as HTML file"""
        if not self.visualizer.tree_data:
            messagebox.showinfo("Info", "No tree data to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Tree as HTML",
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            initialname=f"directory_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        )
        
        if filename:
            try:
                directory_name = Path(self.selected_directory.get()).name
                self.visualizer.export_html(filename, f"Directory Tree - {directory_name}")
                messagebox.showinfo("Success", f"Interactive HTML tree saved to:\n{filename}")
                self.status_bar.config(text=f"HTML tree saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save HTML tree:\n{e}")
    
    def save_json(self):
        """Save tree as JSON file"""
        if not self.visualizer.tree_data:
            messagebox.showinfo("Info", "No tree data to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Tree as JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialname=f"directory_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filename:
            try:
                self.visualizer.export_json(filename)
                messagebox.showinfo("Success", f"Tree data saved to:\n{filename}")
                self.status_bar.config(text=f"JSON data saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save JSON data:\n{e}")


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = DirectoryTreeGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()

"""
Simple GUI for Building Detection System
Requires tkinter (usually comes with Python)
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from pathlib import Path

class BuildingDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Building Detection System")
        self.root.geometry("650x450")
        
        self.input_path = tk.StringVar()
        self.output_folder = tk.StringVar(value="output")
        self.input_mode = tk.StringVar(value="folder")  # "folder" or "file"
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Building Detection System", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Input mode selection
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(mode_frame, text="Select Input Mode:", font=("Arial", 10, "bold")).pack(anchor='w')
        
        mode_radio_frame = tk.Frame(mode_frame)
        mode_radio_frame.pack(anchor='w', pady=5)
        
        tk.Radiobutton(mode_radio_frame, text="Process Folder", 
                      variable=self.input_mode, value="folder",
                      command=self.update_input_label).pack(side='left', padx=(0,20))
        tk.Radiobutton(mode_radio_frame, text="Process Single File", 
                      variable=self.input_mode, value="file",
                      command=self.update_input_label).pack(side='left')
        
        # Input selection
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill='x')
        
        self.input_label = tk.Label(input_frame, text="Input Folder (containing images):")
        self.input_label.pack(anchor='w')
        
        input_entry_frame = tk.Frame(input_frame)
        input_entry_frame.pack(fill='x', pady=5)
        
        tk.Entry(input_entry_frame, textvariable=self.input_path, width=50).pack(side='left', fill='x', expand=True)
        self.browse_button = tk.Button(input_entry_frame, text="Browse Folder", command=self.browse_input)
        self.browse_button.pack(side='right', padx=(5,0))
        
        # Output folder selection
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(output_frame, text="Output Folder:").pack(anchor='w')
        
        output_entry_frame = tk.Frame(output_frame)
        output_entry_frame.pack(fill='x', pady=5)
        
        tk.Entry(output_entry_frame, textvariable=self.output_folder, width=50).pack(side='left', fill='x', expand=True)
        tk.Button(output_entry_frame, text="Browse", command=self.browse_output_folder).pack(side='right', padx=(5,0))
        
        # Progress bar
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(pady=20, padx=20, fill='x')
        
        tk.Label(self.progress_frame, text="Progress:").pack(anchor='w')
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill='x', pady=5)
        
        # Status text
        self.status_text = tk.Text(self.root, height=10, width=70)
        self.status_text.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Scrollbar for status text
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side='right', fill='y')
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.process_button = tk.Button(button_frame, text="Start Detection", 
                                       command=self.start_detection, 
                                       bg='green', fg='white', font=("Arial", 12, "bold"))
        self.process_button.pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side='left', padx=5)
        tk.Button(button_frame, text="Open Output Folder", command=self.open_output_folder).pack(side='left', padx=5)
        
        # Initial status
        self.log_message("Ready to detect buildings!\n")
        self.log_message("Supported formats: TIF, TIFF, PNG, JPG, JPEG, BMP, GIF\n")
        self.log_message("1. Choose input mode (folder or single file)")
        self.log_message("2. Select input folder/file containing images")
        self.log_message("3. Choose output folder (optional)")
        self.log_message("4. Click 'Start Detection'")
    
    def update_input_label(self):
        if self.input_mode.get() == "folder":
            self.input_label.config(text="Input Folder (containing images):")
            self.browse_button.config(text="Browse Folder")
        else:
            self.input_label.config(text="Input File (single image):")
            self.browse_button.config(text="Browse File")
        
        # Clear previous selection when mode changes
        self.input_path.set("")
    
    def browse_input(self):
        if self.input_mode.get() == "folder":
            path = filedialog.askdirectory(title="Select folder containing images")
            if path:
                self.input_path.set(path)
                self.log_message(f"Selected input folder: {path}")
        else:
            # Support multiple image formats
            filetypes = [
                ("All Supported Images", "*.tif;*.tiff;*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                ("TIFF files", "*.tif;*.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("BMP files", "*.bmp"),
                ("GIF files", "*.gif"),
                ("All files", "*.*")
            ]
            path = filedialog.askopenfilename(
                title="Select image file",
                filetypes=filetypes
            )
            if path:
                self.input_path.set(path)
                self.log_message(f"Selected input file: {path}")
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder.set(folder)
            self.log_message(f"Selected output folder: {folder}")
    
    def log_message(self, message):
        self.status_text.insert('end', message + '\n')
        self.status_text.see('end')
        self.root.update()
    
    def clear_log(self):
        self.status_text.delete(1.0, 'end')
    
    def open_output_folder(self):
        output_path = self.output_folder.get()
        if os.path.exists(output_path):
            os.startfile(output_path)  # Windows
        else:
            messagebox.showwarning("Warning", f"Output folder does not exist: {output_path}")
    
    def start_detection(self):
        input_path = self.input_path.get()
        output_path = self.output_folder.get()
        input_mode = self.input_mode.get()
        
        if not input_path:
            if input_mode == "folder":
                messagebox.showerror("Error", "Please select an input folder")
            else:
                messagebox.showerror("Error", "Please select an input file")
            return
        
        if not os.path.exists(input_path):
            if input_mode == "folder":
                messagebox.showerror("Error", f"Input folder does not exist: {input_path}")
            else:
                messagebox.showerror("Error", f"Input file does not exist: {input_path}")
            return
        
        # Disable button and start progress
        self.process_button.config(state='disabled')
        self.progress_bar.start()
        
        # Run detection in separate thread
        thread = threading.Thread(target=self.run_detection, args=(input_path, output_path, input_mode))
        thread.daemon = True
        thread.start()
    
    def run_detection(self, input_path, output_path, input_mode):
        try:
            self.log_message(f"\n=== Starting Building Detection ===")
            if input_mode == "folder":
                self.log_message(f"Input folder: {input_path}")
            else:
                self.log_message(f"Input file: {input_path}")
            self.log_message(f"Output folder: {output_path}")
            
            # Import detection functions
            try:
                from building_detector import detect_buildings_in_folder, process_single_image
                import pandas as pd
            except ImportError:
                self.log_message("Error: building_detector.py not found or dependencies missing")
                self.log_message("Please ensure all required packages are installed:")
                self.log_message("pip install opencv-python numpy pandas matplotlib")
                return
            
            # Run detection based on mode
            if input_mode == "folder":
                # Process entire folder
                results_df = detect_buildings_in_folder(input_path, output_path)
                
                if not results_df.empty:
                    self.log_message(f"\n✓ Detection completed successfully!")
                    self.log_message(f"✓ Total images processed: {len(results_df)}")
                    self.log_message(f"✓ Total buildings detected: {results_df['building_count'].sum()}")
                    self.log_message(f"✓ Average buildings per image: {results_df['building_count'].mean():.2f}")
                    self.log_message(f"✓ Individual CSV files created for each image")
                    self.log_message(f"✓ Results saved to: {output_path}")
                    
                    # Show completion message
                    self.root.after(0, lambda: messagebox.showinfo("Success", 
                        f"Detection completed!\n\nProcessed {len(results_df)} images\n"
                        f"Detected {results_df['building_count'].sum()} buildings\n"
                        f"Individual CSV files created for each image\n\n"
                        f"Check the '{output_path}' folder for results"))
                else:
                    self.log_message("\n✗ No images were processed successfully")
                    self.root.after(0, lambda: messagebox.showwarning("Warning", 
                        "No images were processed. Please check:\n"
                        "1. Input folder contains valid images\n"
                        "2. Image formats are supported (.tif, .tiff, .png, .jpg, .jpeg, .bmp, .gif)\n"
                        "3. Images are not corrupted"))
            else:
                # Process single file
                self.log_message(f"Processing single image: {os.path.basename(input_path)}")
                
                # Create output directory if it doesn't exist
                os.makedirs(output_path, exist_ok=True)
                
                # Process the single image
                result = process_single_image(input_path, output_path)
                
                if result and result.get('building_count', 0) >= 0:
                    self.log_message(f"\n✓ Single image detection completed successfully!")
                    self.log_message(f"✓ Image processed: {os.path.basename(input_path)}")
                    self.log_message(f"✓ Buildings detected: {result.get('building_count', 0)}")
                    self.log_message(f"✓ Total building area: {result.get('total_building_area_pixels', 0)} pixels")
                    self.log_message(f"✓ Output image: {result.get('output_image', 'N/A')}")
                    self.log_message(f"✓ Individual CSV: {result.get('individual_csv', 'N/A')}")
                    self.log_message(f"✓ Results saved to: {output_path}")
                    
                    # Show completion message
                    self.root.after(0, lambda: messagebox.showinfo("Success", 
                        f"Detection completed!\n\nProcessed: {os.path.basename(input_path)}\n"
                        f"Detected {result.get('building_count', 0)} buildings\n"
                        f"Output saved to '{output_path}' folder"))
                else:
                    self.log_message("\n✗ Failed to process the image")
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                        "Failed to process the image. Please check:\n"
                        "1. Image file is not corrupted\n"
                        "2. Image format is supported\n"
                        "3. Image contains detectable buildings"))
                
        except Exception as e:
            self.log_message(f"\n✗ Error during detection: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Detection failed:\n{str(e)}"))
        
        finally:
            # Re-enable button and stop progress
            self.root.after(0, self.detection_finished)
    
    def detection_finished(self):
        self.process_button.config(state='normal')
        self.progress_bar.stop()

def main():
    # Check if tkinter is available
    try:
        root = tk.Tk()
        app = BuildingDetectorGUI(root)
        root.mainloop()
    except ImportError:
        print("Error: tkinter not available")
        print("Please install tkinter or run the command line version:")
        print("python building_detector.py")

if __name__ == "__main__":
    main()
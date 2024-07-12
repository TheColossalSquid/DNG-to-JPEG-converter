import rawpy
import imageio
import os
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, BooleanVar
import threading

def convert_dng_to_jpeg(dng_path, jpeg_path):
    try:
        with rawpy.imread(dng_path) as raw:
            rgb = raw.postprocess()
        imageio.imwrite(jpeg_path, rgb)
        print(f"Successfully converted {dng_path} to {jpeg_path}")
    except Exception as e:
        print(f"Failed to convert {dng_path} to {jpeg_path}: {e}")

def batch_convert_dng_to_jpeg(dng_folder, jpeg_folder, progress_var, cancel_var):
    if not os.path.exists(dng_folder):
        print(f"The directory {dng_folder} does not exist.")
        return
    
    if not os.path.exists(jpeg_folder):
        os.makedirs(jpeg_folder)
    
    dng_files = [f for f in os.listdir(dng_folder) if f.lower().endswith('.dng')]
    total_files = len(dng_files)

    for i, file_name in enumerate(dng_files):
        if cancel_var.get():
            messagebox.showinfo("Conversion Cancelled", "The conversion process was cancelled.")
            return
        dng_path = os.path.join(dng_folder, file_name)
        jpeg_path = os.path.join(jpeg_folder, os.path.splitext(file_name)[0] + '.jpeg')
        convert_dng_to_jpeg(dng_path, jpeg_path)
        progress_var.set(f"Converting {i+1}/{total_files} photos")
    
    messagebox.showinfo("Conversion Completed", "All DNG files have been converted to JPEG.")

def select_dng_folder():
    folder_selected = filedialog.askdirectory()
    dng_folder_entry.delete(0, tk.END)
    dng_folder_entry.insert(0, folder_selected)

def select_jpeg_folder():
    folder_selected = filedialog.askdirectory()
    jpeg_folder_entry.delete(0, tk.END)
    jpeg_folder_entry.insert(0, folder_selected)

def start_conversion():
    dng_folder = dng_folder_entry.get()
    jpeg_folder = jpeg_folder_entry.get()
    if not dng_folder or not jpeg_folder:
        messagebox.showwarning("Input Error", "Please select both source and destination folders.")
        return
    cancel_var.set(False)
    progress_var.set("Starting conversion...")
    conversion_thread = threading.Thread(target=batch_convert_dng_to_jpeg, args=(dng_folder, jpeg_folder, progress_var, cancel_var))
    conversion_thread.start()

def cancel_conversion():
    cancel_var.set(True)

# Create the main window
root = tk.Tk()
root.title("DNG to JPEG Converter")

# Create and place the widgets
tk.Label(root, text="Select Source Folder (DNG files)").grid(row=0, column=0, padx=10, pady=10)
dng_folder_entry = tk.Entry(root, width=50)
dng_folder_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_dng_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Select Destination Folder (JPEG files)").grid(row=1, column=0, padx=10, pady=10)
jpeg_folder_entry = tk.Entry(root, width=50)
jpeg_folder_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_jpeg_folder).grid(row=1, column=2, padx=10, pady=10)

progress_var = StringVar()
tk.Label(root, textvariable=progress_var).grid(row=2, column=0, columnspan=3, pady=10)

cancel_var = BooleanVar()
tk.Button(root, text="Start Conversion", command=start_conversion).grid(row=3, column=0, columnspan=2, pady=20)
tk.Button(root, text="Cancel Conversion", command=cancel_conversion).grid(row=3, column=2, pady=20)

# Run the application
root.mainloop()

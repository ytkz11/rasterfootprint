import os
import tkinter as tk
from tkinter import filedialog, messagebox
from osgeo import gdal, ogr, osr
from raster_footprint import footprint_from_href
import base64
from logo import img
from main import create_polygon

def footprint_from_href_info(file, holes=False, nodata=0):
    footprint = footprint_from_href(file, densify_distance=1, holes=holes, nodata=nodata)
    return footprint

def browse_files():
    file_paths = filedialog.askopenfilenames(
        filetypes=[
            ("TIFF files", "*.tif;*.TIF;*.tiff;*.TIFF"),
            ("All files", "*.*")
        ]
    )
    if file_paths:
        for file_path in file_paths:
            try:
                # Retrieve the parameters from the GUI
                holes = holes_var.get()
                nodata_value = int(nodata_entry.get()) if nodata_entry.get().isdigit() else 0
                create_polygon(file_path, holes=holes, nodata=nodata_value)  # Call create_polygon for each file
            except Exception as e:
                messagebox.showerror("Error", f"处理 {file_path} 时出错: {e}")
        messagebox.showinfo("单文件处理完成", "单文件已成功处理!")

def browse_folder():
    folder_path = filedialog.askdirectory()  # Select a folder
    if folder_path:
        tiff_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                      if f.lower().endswith(('.tif', '.tiff', '.TIF', '.TIFF'))]
        if tiff_files:
            for file_path in tiff_files:
                try:
                    # Retrieve the parameters from the GUI
                    holes =  holes_var.get()
                    nodata_value = int(nodata_entry.get()) if nodata_entry.get().isdigit() else 0
                    create_polygon(file_path, holes=holes, nodata=nodata_value)
                except Exception as e:
                    messagebox.showerror("Error", f"处理 {file_path} 时出错: {e}")
            messagebox.showinfo("批量处理完成", "所有文件已成功处理!")
        else:
            messagebox.showwarning("没有 TIFF 文件", "该文件夹中没有 TIFF 文件。")

# GUI Setup
root = tk.Tk()
root.title("影像有效范围创建器")
root.geometry("400x300")
icon = open("gui_icon.ico", 'wb+')
icon.write(base64.b64decode(img))  # 写入到临时文件中
icon.close()
root.iconbitmap("gui_icon.ico")  # 设置图标
os.remove("gui_icon.ico")  # 删除临时图标

# 选择多个文件按钮
btn_batch_file = tk.Button(root, text="选择单个文件", command=browse_files)
btn_batch_file.pack(pady=10)

# 选择文件夹按钮
btn_batch_folder = tk.Button(root, text="选择文件夹（批量处理）", command=browse_folder)
btn_batch_folder.pack(pady=10)

# Holes Option: Add a checkbox for holes
holes_var = tk.BooleanVar()
checkbox_holes = tk.Checkbutton(root, text="保留孔洞 (Holes)", variable=holes_var)
checkbox_holes.pack(pady=5)

# NoData Value Option: Add an entry field for NoData value
label_nodata = tk.Label(root, text="无效值 (NoData) 参数:")
label_nodata.pack(pady=5)
nodata_entry = tk.Entry(root)
nodata_entry.insert(0, "0")  # Default NoData value is 0
nodata_entry.pack(pady=5)

root.mainloop()

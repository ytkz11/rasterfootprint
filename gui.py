import os
import tkinter as tk
from tkinter import filedialog, messagebox
from osgeo import gdal, ogr, osr
from raster_footprint import footprint_from_href
import base64
from logo import img


def footprint_from_href_info(file, holes=False, nodata=0):
    footprint = footprint_from_href(file, densify_distance=1, holes=holes, nodata=nodata)
    return footprint

def create_polygon(file, holes=False, nodata=0):
    polygon = footprint_from_href_info(file, holes=holes, nodata=nodata)

    output_file = os.path.splitext(file)[0] + '_boundary.shp'
    dataset = gdal.Open(file)
    projection = dataset.GetProjection()  # Get projection information
    driver = ogr.GetDriverByName('ESRI Shapefile')

    if os.path.exists(output_file):
        driver.DeleteDataSource(output_file)  # Delete existing shapefile if it exists

    data_source = driver.CreateDataSource(output_file)

    srs = osr.SpatialReference(wkt=projection)  # Define spatial reference
    layer = data_source.CreateLayer('boundary', srs, ogr.wkbPolygon)  # Create a polygon layer

    field_name = ogr.FieldDefn("Name", ogr.OFTString)
    field_name.SetWidth(24)
    layer.CreateField(field_name)  # Add field to the layer

    poly = ogr.Geometry(ogr.wkbPolygon)
    if len(polygon['coordinates']) > 0:
        for hole_coords in polygon['coordinates']:
            hole_ring = ogr.Geometry(ogr.wkbLinearRing)
            for coord in hole_coords:
                hole_ring.AddPoint(coord[0], coord[1])
            poly.AddGeometry(hole_ring)

    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("Name", "MyPolygon")
    feature.SetGeometry(poly)
    layer.CreateFeature(feature)  # Add feature to the layer

    # Cleanup resources
    feature = None
    data_source = None
    print(f"文件已成功创建: {output_file}")
    return output_file

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
                holes = False
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
                    holes = False
                    nodata_value = int(nodata_entry.get()) if nodata_entry.get().isdigit() else 0
                    create_polygon(file_path, holes=holes, nodata=nodata_value)
                except Exception as e:
                    messagebox.showerror("Error", f"处理 {file_path} 时出错: {e}")
            messagebox.showinfo("批量处理完成", "所有文件已成功处理!")
        else:
            messagebox.showwarning("没有 TIFF 文件", "该文件夹中没有 TIFF 文件。")

# GUI Setup
root = tk.Tk()
root.title("影像有效范围创建器（生成无孔洞）")
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
# checkbox_holes = tk.Checkbutton(root, text="保留孔洞 (Holes)", variable=holes_var)
# checkbox_holes.pack(pady=5)

# NoData Value Option: Add an entry field for NoData value
label_nodata = tk.Label(root, text="无效值 (NoData) 参数:")
label_nodata.pack(pady=5)
nodata_entry = tk.Entry(root)
nodata_entry.insert(0, "0")  # Default NoData value is 0
nodata_entry.pack(pady=5)

root.mainloop()

# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from osgeo import gdal, ogr, osr
from utils import footprint_from_href
import base64
from logo import img

def footprint_from_href_info(file, holes=False, nodata=0):
    # Generate footprint from the raster file
    footprint = footprint_from_href(file, densify_distance=1, holes=holes, nodata=nodata)
    return footprint

def create_polygon(file, holes=False, nodata=0):
    # Get the polygon footprint from the raster file
    polygon = footprint_from_href_info(file, holes=holes, nodata=nodata)

    # Define output shapefile path by appending '_boundary.shp' to the input file name
    output_file = os.path.splitext(file)[0] + '_boundary.shp'
    dataset = gdal.Open(file)
    projection = dataset.GetProjection()  # Get projection information
    
    # Get the ESRI Shapefile driver for creating and managing shapefiles
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # Delete the output file if it already exists to avoid duplication or conflicts
    if os.path.exists(output_file):
        driver.DeleteDataSource(output_file)  # Delete existing shapefile if it exists

    # Create a new data source (i.e., a new shapefile)
    data_source = driver.CreateDataSource(output_file)

    # Define the spatial reference from the raster's projection
    srs = osr.SpatialReference(wkt=projection)  
    # Create a polygon layer named 'boundary' with the specified spatial reference
    layer = data_source.CreateLayer('boundary', srs, ogr.wkbPolygon)  

    # Define a string field named "Name" with a width of 24 characters
    field_name = ogr.FieldDefn("Name", ogr.OFTString)
    field_name.SetWidth(24)
    layer.CreateField(field_name)  # Add field to the layer

    # Create a new polygon geometry
    poly = ogr.Geometry(ogr.wkbPolygon)
    if len(polygon['coordinates']) > 4:
        # Iterate through each set of coordinates (including holes) and build linear rings
        for hole_coords in polygon['coordinates']:
            hole_ring = ogr.Geometry(ogr.wkbLinearRing)
            for coord in hole_coords:
                hole_ring.AddPoint(coord[0], coord[1])
            poly.AddGeometry(hole_ring)
    else:
        try:
            # Find the ring with the most coordinates (assumed to be the outer ring)
            max_i = len(polygon['coordinates'][0])
            target_i = 0
            for i in range(len(polygon['coordinates'])):
                temp_i = len(polygon['coordinates'][i])
                if max_i < temp_i:
                    max_i = temp_i
                    target_i = i

            # Build the polygon from the identified outer ring
            for hole_coords in polygon['coordinates'][target_i]:
                hole_ring = ogr.Geometry(ogr.wkbLinearRing)
                for coord in hole_coords:
                    hole_ring.AddPoint(coord[0], coord[1])
                poly.AddGeometry(hole_ring)

        except:
            print('Something went wrong')

    # Create a new feature for the layer
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("Name", "MyPolygon")
    feature.SetGeometry(poly)
    layer.CreateFeature(feature)  # Add feature to the layer

    # Cleanup resources
    feature = None
    data_source = None
    print(f"File successfully created: {output_file}")
    return output_file

def browse_files():
    # Open file dialog to select multiple files
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
                create_polygon(file_path, holes=holes, nodata=nodata_value)  # Process each file
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {file_path}: {e}")
        messagebox.showinfo("Single File Processing Complete", "Single file processing completed successfully!")

def browse_folder():
    # Open folder dialog to select a directory
    folder_path = filedialog.askdirectory()  
    if folder_path:
        # List all TIFF files in the folder
        tiff_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                      if f.lower().endswith(('.tif', '.tiff', '.TIF', '.TIFF'))]
        if tiff_files:
            for file_path in tiff_files:
                try:
                    # Retrieve the parameters from the GUI
                    holes = holes_var.get()
                    nodata_value = int(nodata_entry.get()) if nodata_entry.get().isdigit() else 0
                    create_polygon(file_path, holes=holes, nodata=nodata_value)
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing {file_path}: {e}")
            messagebox.showinfo("Batch Processing Complete", "All files processed successfully!")
        else:
            messagebox.showwarning("No TIFF Files", "No TIFF files found in the selected folder.")

# GUI Setup
root = tk.Tk()
root.title("Raster Coverage Creator")
root.geometry("400x300")

# Create and set the window icon from base64-encoded data
icon = open("gui_icon.ico", 'wb+')
icon.write(base64.b64decode(img))  # Write to a temporary file
icon.close()
root.iconbitmap("gui_icon.ico")  # Set the icon
os.remove("gui_icon.ico")  # Delete the temporary icon file

# Button to select multiple files
btn_batch_file = tk.Button(root, text="Select Single File", command=browse_files)
btn_batch_file.pack(pady=10)

# Button to select a folder for batch processing
btn_batch_folder = tk.Button(root, text="Select Folder (Batch Processing)", command=browse_folder)
btn_batch_folder.pack(pady=10)

# Holes Option: Add a checkbox for holes
holes_var = tk.BooleanVar()
checkbox_holes = tk.Checkbutton(root, text="Keep Holes", variable=holes_var)
checkbox_holes.pack(pady=5)

# NoData Value Option: Add an entry field for NoData value
label_nodata = tk.Label(root, text="NoData Value Parameter:")
label_nodata.pack(pady=5)
nodata_entry = tk.Entry(root)
nodata_entry.insert(0, "0")  # Default NoData value is 0
nodata_entry.pack(pady=5)

root.mainloop()
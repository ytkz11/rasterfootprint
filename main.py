import os

from osgeo import gdal, ogr, osr

from raster_footprint import footprint_from_href
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2

def footprint_from_href_info(file, holes=False, nodata=0):
    ds = gdal.Open(file)
    if ds is None:
        raise Exception("无法打开文件")
    array = ds.ReadAsArray()
    img  = Image.open(file)
    img_array = np.array(img)
    img_cv2 = cv2.imread(file)
    img_gdal_array = np.transpose(array, (1,2,0))
    # plt.imshow(img_gdal_array),plt.show()
    footprint = footprint_from_href(        file,
                                            # densify_distance=1,
                                            # simplify_tolerance=0.001,
                                            holes=holes,
                                            nodata=nodata)

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
    if len(polygon['coordinates']) > 4:
        for hole_coords in polygon['coordinates']:
            hole_ring = ogr.Geometry(ogr.wkbLinearRing)
            for coord in hole_coords:
                hole_ring.AddPoint(coord[0], coord[1])
            poly.AddGeometry(hole_ring)
    else:
        try:
            max_i = len(polygon['coordinates'][0])
            target_i = 0
            for i in range(len(polygon['coordinates'])):
                temp_i = len(polygon['coordinates'][i])
                if max_i < temp_i:
                    max_i = temp_i
                    target_i = i

            for hole_coords in polygon['coordinates'][target_i]:
                hole_ring = ogr.Geometry(ogr.wkbLinearRing)
                for coord in hole_coords:
                    hole_ring.AddPoint(coord[0], coord[1])
                poly.AddGeometry(hole_ring)

        except:
            print('出了问题')

    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("Name", "MyPolygon")
    feature.SetGeometry(poly)
    layer.CreateFeature(feature)  # Add feature to the layer

    # Cleanup resources
    feature = None
    data_source = None
    print(f"文件已成功创建: {output_file}")
if __name__ == '__main__':
    tif_path = r'D:\无人机\test\DJI_20230410091605_0121_hole.tif'
    tif_path = r'D:\无人机\test\DJI_20230410091605_0121_hole_2000.tif'
    create_polygon(tif_path,holes=1,nodata=0)
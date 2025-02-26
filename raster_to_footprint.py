import os
from osgeo import gdal, ogr, osr
from utils import footprint_from_href

def footprint_from_href_info(file, holes=False, nodata=0):
    # Generate footprint from the raster file using footprint_from_href
    footprint = footprint_from_href(
        file,
        # densify_distance=1,  # Uncomment to set densification distance
        # simplify_tolerance=0.001,  # Uncomment to set simplification tolerance
        holes=holes,
        nodata=nodata
    )
    return footprint

def create_polygon(file, holes=False, nodata=0):
    # Get the polygon footprint from the raster file
    polygon = footprint_from_href_info(file, holes=holes, nodata=nodata)

    # Define output shapefile path by appending '_boundary.shp' to the input file name
    output_file = os.path.splitext(file)[0] + '_boundary.shp'
    
    # Open the raster dataset
    dataset = gdal.Open(file)
    projection = dataset.GetProjection()  # Get projection information from the raster

    # Get the ESRI Shapefile driver object for creating and managing shapefiles
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # If the output file already exists, delete it to avoid duplication or conflicts
    if os.path.exists(output_file):
        driver.DeleteDataSource(output_file)  # Delete existing shapefile if it exists
    
    # Create a new data source (i.e., a new shapefile)
    data_source = driver.CreateDataSource(output_file)

    # Define the spatial reference system from the raster's projection
    srs = osr.SpatialReference(wkt=projection)

    # Create a polygon layer named 'boundary' with the specified spatial reference
    layer = data_source.CreateLayer('boundary', srs, ogr.wkbPolygon)

    # Define a string field named "Name" with a width of 24 characters
    field_name = ogr.FieldDefn("Name", ogr.OFTString)
    field_name.SetWidth(24)
    layer.CreateField(field_name)  # Add the field to the layer

    # Create a new polygon geometry
    poly = ogr.Geometry(ogr.wkbPolygon)

    # Iterate through each set of coordinates in the polygon (for outer ring and holes)
    for _coords in polygon['coordinates']:
        _ring = ogr.Geometry(ogr.wkbLinearRing)  # Create a linear ring object
        for coord in _coords:
            _ring.AddPoint(coord[0], coord[1])  # Add point coordinates to the linear ring
        poly.AddGeometry(_ring)  # Add the linear ring to the polygon (as outer ring or hole)

    # Create a new feature for the layer
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("Name", "MyPolygon")  # Set the "Name" field value
    feature.SetGeometry(poly)  # Assign the polygon geometry to the feature
    layer.CreateFeature(feature)  # Add the feature to the layer

    # Cleanup resources
    feature = None
    data_source = None
    print(f"File successfully created: {output_file}")

if __name__ == "__main__":
    tif_path = r'.\raster\LC09_L2SP_138039_20230101_20230315_02_T1_SR_B2_rgb_clip_nohole.tif'
    create_polygon(tif_path, holes=1, nodata=0)
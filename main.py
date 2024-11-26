import os

from osgeo import gdal, ogr, osr

from raster_footprint import footprint_from_href


def footprint_from_href_info(file, holes=False, nodata=0):
    footprint = footprint_from_href(        file,
                                            densify_distance=1,
                                            # simplify_tolerance=0.001,
                                            holes=holes,
                                            nodata=nodata)

    return footprint

def create_polygon(file,holes=False,nodata=0):

        polygon = footprint_from_href_info(file,holes=holes,nodata=nodata)

        output_file = os.path.splitext(file)[0]+'1122.shp'
        dataset = gdal.Open(tif_path)
        projection = dataset.GetProjection()    # 创建Shapefile
        driver = ogr.GetDriverByName('ESRI Shapefile')

        if os.path.exists(output_file):

            driver.DeleteDataSource(output_file)
        data_source = driver.CreateDataSource(output_file)

           #创建图层
        srs = osr.SpatialReference(wkt=projection)
        layer = data_source.CreateLayer('boundary', srs, ogr.wkbPolygon)    # 添加字段
        field_name = ogr.FieldDefn("Name", ogr.OFTString)
        field_name.SetWidth(24)
        layer.CreateField(field_name)
    # 创建多边形
        poly = ogr.Geometry(ogr.wkbPolygon)
    # 添加所有点位数据
        if len(polygon['coordinates']) > 0:
            for hole_coords in polygon['coordinates']:
                # Ensure the hole ring has at least 4 points and is closed
                if len(hole_coords) >= 4:
                    hole_ring = ogr.Geometry(ogr.wkbLinearRing)
                    for coord in hole_coords:
                        hole_ring.AddPoint(coord[0], coord[1])

                    # Ensure the hole is closed by checking if the first and last point are the same
                    if hole_ring.GetPoint(0) != hole_ring.GetPoint(hole_ring.GetPointCount() - 1):
                        hole_ring.AddPoint(hole_coords[0][0], hole_coords[0][1])

                    poly.AddGeometry(hole_ring)
                else:
                    print(f"警告: 孔洞的坐标数量不足 4 个，已跳过孔洞处理: {hole_coords}")

                    # 创建要素
                    #
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField("Name", "MyPolygon")
    # 设置几何体
    #
        feature.SetGeometry(poly)
    # 将要素添加到图层
        layer.CreateFeature(feature)
    # 清理资源
    #
        feature = None
        data_source = None
        print(f"文件已成功创建: {output_file}")

if __name__ == '__main__':
    tif_path = r'D:\无人机\test\DJI_20230410091605_0121.tif'
    create_polygon(tif_path,holes=True,nodata=0)
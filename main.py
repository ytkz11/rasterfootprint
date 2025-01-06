import os

from osgeo import gdal, ogr, osr

from raster_footprint import footprint_from_href


def footprint_from_href_info(file, holes=False, nodata=0):

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

    # 获取 ESRI Shapefile 驱动器对象，用于创建和管理 Shapefile 文件
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # 如果输出文件已经存在，则删除它以避免重复或冲突
    if os.path.exists(output_file):
        driver.DeleteDataSource(output_file)  # Delete existing shapefile if it exists
    # 创建一个新的数据源（即新的 Shapefile 文件）
    data_source = driver.CreateDataSource(output_file)

    srs = osr.SpatialReference(wkt=projection)  # Define spatial reference

    # 创建一个名为 'boundary' 的多边形图层，并指定其空间参考系统
    layer = data_source.CreateLayer('boundary', srs, ogr.wkbPolygon)

    field_name = ogr.FieldDefn("Name", ogr.OFTString)
    field_name.SetWidth(24)
    layer.CreateField(field_name)  # Add field to the layer

    poly = ogr.Geometry(ogr.wkbPolygon)

    #  遍历输入多边形中的每个孔洞（内环），并构建相应的线性环
    for _coords in polygon['coordinates']:
        _ring = ogr.Geometry(ogr.wkbLinearRing)  # 创建一个线性环对象
        for coord in _coords:
            _ring.AddPoint(coord[0], coord[1])  # 向线性环中添加点坐标
        poly.AddGeometry(_ring) # 将线性环添加到多边形中作为孔洞


    # if len(polygon['coordinates']) > 4:
    #     for hole_coords in polygon['coordinates']:
    #         hole_ring = ogr.Geometry(ogr.wkbLinearRing)
    #         for coord in hole_coords:
    #             hole_ring.AddPoint(coord[0], coord[1])
    #         poly.AddGeometry(hole_ring)
    # else:
    #     try:
    #         max_i = len(polygon['coordinates'][0])
    #         target_i = 0
    #         for i in range(len(polygon['coordinates'])):
    #             temp_i = len(polygon['coordinates'][i])
    #             if max_i < temp_i:
    #                 max_i = temp_i
    #                 target_i = i
    #
    #         for hole_coords in polygon['coordinates'][target_i]:
    #             hole_ring = ogr.Geometry(ogr.wkbLinearRing)
    #             for coord in hole_coords:
    #                 hole_ring.AddPoint(coord[0], coord[1])
    #             poly.AddGeometry(hole_ring)
    #
    #     except Exception as e:
    #         print('出了问题')
    #         print(e)

    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("Name", "MyPolygon")
    feature.SetGeometry(poly)
    layer.CreateFeature(feature)  # Add feature to the layer

    # Cleanup resources
    feature = None
    data_source = None
    print(f"文件已成功创建: {output_file}")
if __name__ == '__main__':
    tif_path = r'.\raster\LC09_L2SP_138039_20230101_20230315_02_T1_SR_B2_rgb_clip_nohole.tif'
    # tif_path = r'.\raster\LC09_L2SP_138039_20230101_20230315_02_T1_SR_B2_rgb.tif'
    # tif_path = r'D:\无人机\test\DJI_20230410091605_0121.tif'
    # tif_path = r'D:\无人机\test\DJI_20230410091605_0121_hole_2000.tif'
    create_polygon(tif_path,holes=1,nodata=0)
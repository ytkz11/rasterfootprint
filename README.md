# rasterfootprint

输入遥感影像的路径，生成对应的有效覆盖范围。

![image-20241126223932773](https://raw.githubusercontent.com/ytkz11/picture/master/image-20241126223932773.png)

界面写得很简单，一共两个按钮。对应两种处理方式。

一个是单文件处理；第二个是批处理。

单文件处理测试：

点击第一个按钮。界面如下：

![image-20241126224451474](https://raw.githubusercontent.com/ytkz11/picture/master/image-20241126224451474.png)



在处理完成后，会弹出窗口提示。

批量文件处理测试：

点击第2个按钮。要选择的文件夹必须包含tif文件，我选择的路径是D:\test

![image-20241126224652378](https://raw.githubusercontent.com/ytkz11/picture/master/image-20241126224652378.png)

界面如下,选择好文件夹后，点击选择文件夹按钮：

![image-20241126224302372](https://raw.githubusercontent.com/ytkz11/picture/master/image-20241126224302372.png)



在处理完成后，会弹出窗口提示。如下：

![image-20241126224817045](https://raw.githubusercontent.com/ytkz11/picture/master/image-20241126224817045.png)



将结果放在QGIS展示，目测是否正确。



![image-20241126225013944](https://raw.githubusercontent.com/ytkz11/picture/master/image-20241126225013944.png)

![image-20241126224949176](https://raw.githubusercontent.com/ytkz11/picture/master/image-20241126224949176.png)

# 针对含孔洞的有效范围

安装footprint后，打开footprint.py，只针对footprint_from_mask函数

定位到第85行，修改代码，如下：

修改前：

```
reprojected = reproject_geometry(
        densified, source_crs, destination_crs, precision=precision
    )
```



修改后：

```
reprojected = densified

```



二者区别在于 ，是否进行重投影。

所以 ，footprint_from_mask函数被修改为

```python
def footprint_from_mask(
    mask: npt.NDArray[np.uint8],
    transform: Affine,
    source_crs: CRS,
    *,
    destination_crs: CRS = CRS.from_epsg(4326),
    precision: int = DEFAULT_PRECISION,
    densify_factor: Optional[int] = None,
    densify_distance: Optional[float] = None,
    simplify_tolerance: Optional[float] = None,
    convex_hull: bool = False,
    holes: bool = False,
) -> Optional[Dict[str, Any]]:
    geometry = get_mask_geometry(
        mask, transform=transform, convex_hull=convex_hull, holes=holes
    )

    if geometry is None:
        return None

    densified = densify_geometry(
        geometry, factor=densify_factor, distance=densify_distance
    )
    if source_crs == destination_crs:
    reprojected = densified
    simplified = simplify_geometry(reprojected, tolerance=simplify_tolerance)

    return mapping(simplified)
```

修改界面，如下：
![img.png](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202411281150448.png)



带孔洞的影像有效覆盖范围可视化结果如下：

![image-20241128115448672](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202411281154860.png)

支持批量处理，结果如下：

![image-20241128115520778](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202411281155111.png)



支持不同坐标系的影像生成有效范围。（投影坐标系、地理坐标系都支持）

测试如下：

![image-20241128141453506](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202411281414399.png)

![image-20241128141637592](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202411281416098.png)

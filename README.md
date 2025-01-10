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





# 2025年1月10日 更新

之前写的代码，是有bug的。

原因是：自己对于带孔洞的矢量读写不熟悉。所写的代码冗余且带有错误。

当时写的时候，过于仓促，没写注释。搞得现在时隔两个月，我重新再去读自己写的代码，我已不知道当时为什么要这么写。

所以现在我重新对带孔洞的矢量读写的部分代码进行梳理。在慢慢的编写、测试过程中，逐渐完善了生成遥感影像覆盖范围的小工具。

这个小工具，只是一个demo，功能很单一，限于本人时间有限，不能继续完善。



当时是处于什么的情况下才写出这样的代码，我不禁地问自己。

```
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

        except Exception as e:
            print('出了问题')
            print(e)
```





### 改动

改了孔洞矢量的读写问题。代码如下：

```
    #  遍历输入多边形中的每个孔洞（内环），并构建相应的线性环
    for _coords in polygon['coordinates']:
        _ring = ogr.Geometry(ogr.wkbLinearRing)  # 创建一个线性环对象
        for coord in _coords:
            _ring.AddPoint(coord[0], coord[1])  # 向线性环中添加点坐标
        poly.AddGeometry(_ring) # 将线性环添加到多边形中作为孔洞
```

具体分析，请看下面的图，均为带孔洞的矢量的在python中的具体表达。

1.

![image-20250106102917645](https://mmbiz.qlogo.cn/mmbiz_png/mQe6iaSqrIKbyzBU8DswHeOF4A9RDliaY92ChchK9xWyVfmf4Z0UJXjThabqOGpUIOaYBblTdJbXpiaIM2r6N5Vrg/0?wx_fmt=png&from=appmsg)**这是带一个孔洞的矢量，外轮廓由5个点组成。内轮廓（指孔洞）由265个点组成。**

可以想象，这个是一个标准的正正方方的标准影像。



2.

![image-20250106102950315](https://mmbiz.qlogo.cn/mmbiz_png/mQe6iaSqrIKbyzBU8DswHeOF4A9RDliaY9Kv64ofhhvSf23SbiaWiaAOo7F5S2b3LjohRw6KLHGcyv6UJDljicCzD1A/0?wx_fmt=png&from=appmsg)

**这是带一个孔洞的矢量，外轮廓由3307个点组成。内轮廓（指孔洞）由465个点组成。**

可以想象，这个是一个不标准的多边形的影像。



3.

![image-20250106104637777](https://mmbiz.qlogo.cn/mmbiz_png/mQe6iaSqrIKbyzBU8DswHeOF4A9RDliaY9Ph0LzHowr60TjBTphNzsm6DBNedJsZib4icn6PTaNM7VVvBnN5N4Rn4w/0?wx_fmt=png&from=appmsg)

**这是带354个孔洞的矢量，外轮廓由1055个点组成。**

![image-20250106105439069](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202501061741915.png)





# 测试结果

![image-20250106105854434](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202501061741581.png)

![image-20250106105902341](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202501061740474.png)



![image-20250106110115672](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202501061740552.png)

### 使用说明

这小工具，提供单文件处理模式、批量处理模式。

这小工具，没有确定按钮。在你点击 “选择单个文件” 或 “选择文件夹”后会自动运行程序。**所以要提前勾选是否保留孔洞。**

**无效值参数默认为0，一般不需要改动。**

若你选择批量处理，在你选择的文件夹中必须要存在你需要生成的栅格文件，文件类型为tif格式。

![img](https://mmbiz.qpic.cn/mmbiz_png/mQe6iaSqrIKbyzBU8DswHeOF4A9RDliaY9SULW3X45clFqs2snun7BFfdJibpXKwpl0xYIzMxCTEN38ehMj9W1Lkw/0?wx_fmt=png&from=appmsg)


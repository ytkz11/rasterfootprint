```
[中文介绍](https://github.com/ytkz11/rasterfootprint/READMEcn.md)
```

## Introduction

Raster Footprint is a tool designed to generate the effective coverage area of remote sensing images. Users only need to provide the path to a remote sensing image to generate its corresponding effective coverage area. The tool supports both single-file processing and batch processing modes.

## Features

- **Single File Processing**: Processes a single remote sensing image file to generate its effective coverage area.
- **Batch Processing**: Processes all remote sensing image files in a folder to generate their effective coverage areas.
- **Hole Support**: Supports generating effective coverage areas with holes.
- **Multi-Coordinate System Support**: Supports images in both projected and geographic coordinate systems.

## Usage

### Single File Processing

1. Open the tool interface.
2. Click the "Select Single File" button and choose a remote sensing image file.
3. The program runs automatically and displays a prompt window upon completion.
4. Results can be visualized in QGIS.

### Batch Processing

1. Open the tool interface.
2. Click the "Select Folder" button and choose a folder containing `.tif` files.
3. The program runs automatically and displays a prompt window upon completion.
4. Results can be visualized in QGIS.

### Hole Support

The modified code supports processing images with holes, ensuring that the generated polygons include inner rings (holes).

## Visualization in QGIS

To verify the results, load them into QGIS and visually inspect their correctness.

![image-20241126225013944](https://raw.githubusercontent.com/ytkz11/picture/master/image-20241126225013944.png)

![image-20241126224949176](https://raw.githubusercontent.com/ytkz11/picture/master/image-20241126224949176.png)

The visualization result of the effective coverage area with holes is shown below:

![image-20241128115448672](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202411281154860.png)

The result of batch processing is shown below:

![image-20241128115520778](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202411281155111.png)

Support for generating effective coverage areas from images in different coordinate systems (both projected and geographic coordinate systems) has been tested as follows:

![image-20241128141453506](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202411281414399.png)

![image-20241128141637592](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202411281416098.png)

<<<<<<< HEAD
## Conclusion

Although the Raster Footprint tool has simple functionality, it is sufficient for generating the effective coverage areas of remote sensing images. Due to time constraints, the tool's features are not yet fully refined. We welcome valuable feedback and suggestions from users.
=======




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

>>>>>>> e3b32cc82800059c680772aab8421ca581b5cffa

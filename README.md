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

## Conclusion

Although the Raster Footprint tool has simple functionality, it is sufficient for generating the effective coverage areas of remote sensing images. Due to time constraints, the tool's features are not yet fully refined. We welcome valuable feedback and suggestions from users.

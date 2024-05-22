# Pixel Sorting
Pixel Sorting is a form of glitch art, wich aims to create glitchy images by rearanging their pixels according to several parameters.
<figure>
    <img src="https://github.com/Squidez/PixelSorting/blob/main/example.jpg" alt="Example of pixel sorted image" />
    <figcaption>Original image by Daniel Leone (https://unsplash.com/fr/photos/p1qtao69f2M)</figcaption>
</figure>

## Usage
To use the script call the _pixel_sorter_ function.

## Parameters
name | type | description
---|---|---
|**img_path**|str|path of the image to pixel sort|
|**min**|int : 0 to 255|value of the minimum threshold (default: 64)|
|**max**|int : 0 to 255|value of the maximum threshold (default: 192)|
|**mode**|str: lumi, red, green, blue, hue, sat|determines the mode of sorting (default: lumi)|
|**vertical**|bool|to sort the pixels vertically (default: False)|
|**descending**|bool|to sort the pixels by descending order (default: False)|

#### Modes
name|description
---|---
lumi|sort by luminescence
red, green, blue|sort by intensity of selected color
hue|sort by intensity of hue
sat|sort by intensity of saturation

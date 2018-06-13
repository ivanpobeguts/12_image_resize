# Image Resizer

The script resizes images. Resizing rules:

- Use **scale** or size (**width** and/or **height**), not both
- If either **width** or **height** is given, script saves image ratio
- If the **output directory** is not specified, image will be saved in the same directory 

# How to

Script requires Python 3.5 and some external dependencies. To install them run the following:

``` bash
$ pip install -r requirements.txt
```
Example with image flavicon.jpg with size 630x630:

``` bash

$ python image_resize.py flavicon.jpg --scale 0.5
Image successfully resized: flavicon_315x315.jpg

$ python image_resize.py flavicon.jpg --width 700
Image successfully resized: flavicon_700x700.jpg

$ python image_resize.py flavicon.jpg --height 80
Image successfully resized: flavicon_80x80.jpg

$ python image_resize.py flavicon.jpg --width 100 --height 80 --out c:\Work\python\git\
Warning: the image ratio was changed!
Image successfully resized: c:\Work\python\git\flavicon_100x80.jpg


```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

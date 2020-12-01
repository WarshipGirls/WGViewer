# Resource zip

## Adding new zip files

1. Ensure the file is zipped correctly, such that the file is not corrupted.


## Adding new images/icons

Please go through following checklist before adding images:

1. Ensure the background is transparent
	- You may use [online service](https://www.remove.bg/)
2. For images
	- under `assets/S`, ensure the resolution is `156 x 88`
	- under `assets/E`, ensure the resolution is `44 x 44`
3. Ensure the image does not cause `libpng warning: iCCP: known incorrect sRGB profile`
	- [solution](https://stackoverflow.com/questions/22745076/libpng-warning-iccp-known-incorrect-srgb-profile)
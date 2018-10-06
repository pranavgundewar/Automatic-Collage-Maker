# Automatic Collages
----------------

*Graphical application to make photo collage posters*

This is application for automatic collage creation given a input of set of images.
PhotoCollage allows you to create photo collage posters. It assembles the input
photographs it is given to generate a big poster. Photos are automatically
arranged to fill the whole poster, then you can change the final layout,
dimensions, border or swap photos in the generated grid. 
There are multiple layouts created based on different number of input images. 

## Features:
-----------
* Generates multiple layouts to avail various options for the user
* Possible to swap photos in the generated grid by random shuffling
* Get high-resolution image
* Works well even with a large number of photos (> 20)
* Output collage has the company logo on bottom right corner with color contrasting the background intensity

## Project Setup
---------------
Follow these instructions to get this project set up correctly.

### Supported Python versions

Python Project Template supports the following versions out of the box:

* Python 3.3+

### Instructions

1. Clone the github project:

		git clone https://pranavpg@bitbucket.org/hautebook/hautecollages.git HauteCollages

2. Install the project's development and runtime requirements:

		pip install -r requirements.txt

3. Run test script to ensure all the packages are correctly installed:

		python test.py

	Make sure libraries are installed properly. If you are able to import required libraries, proceed to the next step.

2. Open the final_collage_background.py script and edit the file if you want to change anything.

3. Run the python script as

		usage: final_collage_background.py [-h] [-f FOLDER] [-o OUTPUT] [-t TEXT]

		Automatic Photo Collage Maker.

		optional arguments:
			-h, --help            show this help message and exit
			-f FOLDER, --folder FOLDER
			                    folder with images (*.jpg, *.jpeg, *.png)
			-o OUTPUT, --output OUTPUT
			                    path to the destination folder where images are to be
			                    saved
			-t TEXT, --text TEXT  text that you want to display on final collages

## Author
----------
* Pranav Gundewar

## Contribution
---------------
* If you wish to contribute, please lint your code and pass tests

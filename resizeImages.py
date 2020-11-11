import os
from PIL import Image

def resizeImages(imageFolder):

    outputFolder = 'site'
    assetsFolder = 'assets'
    assetsImageFolder = f"./{assetsFolder}/{imageFolder}" 
    imageList = os.listdir(f"{assetsImageFolder}")
    numImages = len(imageList)
    # print(imageList)
    
    for index, imageFileName in enumerate(imageList):
        i = Image.open(f"{assetsImageFolder}/{imageFileName}")

        # Make the new image half the width and half the 
        # height of the original image
        width = i.size[0]
        height = i.size[1]
        
        newWidth = round(width*0.25)
        newHeight = round(height*0.25)
        
        resized_i = i.resize((newWidth, newHeight))


        #Save the cropped image
        # Build the path of the Output Assets Image folder
        outputAssetsImageFolder = f"./{outputFolder}/{assetsFolder}/{imageFolder}"
        os.makedirs(outputAssetsImageFolder, exist_ok=True)  # Force the creation of the target folder
        
        outputImageFile = f"{outputAssetsImageFolder}/{imageFileName}"
        resized_i.save(outputImageFile)
        
        print(f"Resizing {index} of {numImages}: {imageFileName}", end="\r", flush=True)
    
    print(f"Resized {numImages} images to {outputAssetsImageFolder}")


imageFolder = 'img'
resizeImages(imageFolder)
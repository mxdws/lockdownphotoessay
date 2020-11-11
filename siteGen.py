import json, os, shutil
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
from PIL import Image
import time

# Start the timer...
startTime = time.time()

def removeSite():
    outputFolder = 'site'
    if os.path.exists(outputFolder):
        shutil.rmtree(outputFolder)

def copyAssets(folder):
    outputFolder = 'site'
    assetSource = f"assets/{folder}"
    assetTarget = f"assets/{folder}"

    assetSourcePath = f"./{assetSource}"
    assetTargetPath = f"./{outputFolder}/{assetTarget}"

    if os.path.isdir(assetSource):
        # os.makedirs(assetTargetPath, exist_ok=True)  # Force the creation of the target folder
        shutil.copytree(assetSourcePath, assetTargetPath)
        print(f"Assets copied to the {assetTargetPath} folder")
    else:
        print(f"Assets source folder does not exist: {assetSource}")

def renderPage(pageHTML, permalink, template, title, description):
    # 5.1 Initialise some of the global template variables
    templateFolder = './templates'
    templateFile = template
    outputFolder = 'site'

    # Initialise Jinja2
    file_loader = FileSystemLoader(templateFolder)
    env = Environment(loader=file_loader)

    # Render with Jinja2
    targetTemplate = env.get_template(templateFile)
    targetHTML = targetTemplate.render(title=title, description=description, pageHTML=pageHTML)
    targetPath = f"./{outputFolder}/{permalink}"

    # Write the file to the output folder
    targetFile = f"{targetPath}/index.html"
    os.makedirs(targetPath, exist_ok=True)  # Force the creation of the target folder
    with open(targetFile, 'w') as file:
        file.write(targetHTML)

    print("Page rendered")

def renderSnippet(snippetContent, snippetFile):
    # 5.1 Initialise some of the global template variables
    snippetFolder = './snippets'
    snippetFile = snippetFile
    # outputFolder = 'site'

    # Initialise Jinja2
    file_loader = FileSystemLoader(snippetFolder)
    env = Environment(loader=file_loader)

    # Render with Jinja2
    targetSnippet = env.get_template(snippetFile)
    renderedSnippet = targetSnippet.render(snippetContent=snippetContent)

    return renderedSnippet

def getPageContentBlocks(contentFile):
    with open(contentFile, 'r') as f:
        pageContent = json.load(f)
    
    return pageContent

def getPageMarkUp(pageContentBlocks):
    pageHTML = ""

    for p in pageContentBlocks:    
        snippetFile= f"{p['blockType']}.html"
        snippetContent = p['blockContent']

        pageHTML += "\n" + renderSnippet(snippetContent, snippetFile)

    return pageHTML

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


# Start Generation Algorithm

# 1. Initialise some Global variables
contentFile = 'pageContent.json'
templateFile='page.html'

# 2. Remove any existing website folder
removeSite()

# 3. Get a list of all the blocks that make up the webpage
pageContentBlocks = getPageContentBlocks(contentFile)

# 4. Turn the block from Step 3 in to an HTML object
pageHTML = getPageMarkUp(pageContentBlocks)

# 5. Render the HTML and write it to a file
title=f"Lockdown in Chinatown - A Photo Essay by Martin Dawson"
description=f"The UK is in a second national lockdown, but what does that mean for one of the busiest areas in London?"

renderPage(pageHTML,'',templateFile, title, description)

# 6. Copy the assests folder to the Output folder
copyAssets('css')
copyAssets('svg')

# 7. Resize any images in an image folder
imageFolder = 'img'
resizeImages(imageFolder)

# ... and stop the timer!
endTime = time.time()
duration = endTime - startTime
print(f"Finished in {str(round(duration, 3))} seconds.")
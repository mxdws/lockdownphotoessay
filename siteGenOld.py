import json, os, shutil
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
from PIL import Image
import time

# Start the timer...
startTime = time.time()

class Site:

    with open("siteConfig.json", 'r') as f:
        site = json.load(f)
    
    pageData = site['pageManifest']['pageData']
    title = site['pageManifest']['pageData']['title']
    description = site['pageManifest']['pageData']['description']
    pageContentBlocks = site['pageManifest']['pageContent']
    outputFolder = site['outputFolder']
    templatesFolder = site['templatesFolder']
    templateFile = site['templateFile']
    snippetsFolder = site['snippetsFolder']
    assestsFolder = site['assets']['assetsFolder']
    assestsFoldersToCopy = site['assets']['foldersToCopy']
    assetsImagesFolder = site['assets']['imagesFolder']
    siteAuthor = site['author']
    siteSocials = site['social']


def removeSite():
    outputFolder = siteConfig.outputFolder
    if os.path.exists(outputFolder):
        shutil.rmtree(outputFolder)

def copyAssets():

    outputFolder = siteConfig.outputFolder
    assetsFolder = siteConfig.assestsFolder
    assestsFoldersToCopy = siteConfig.assestsFoldersToCopy

    for a in assestsFoldersToCopy:
        folderToCopy = a
        assetSource = f"{assetsFolder}/{folderToCopy}"
        assetTarget = f"{assetsFolder}/{folderToCopy}"

        assetSourcePath = f"./{assetSource}"
        assetTargetPath = f"./{outputFolder}/{assetTarget}"

        if os.path.isdir(assetSource):
            # os.makedirs(assetTargetPath, exist_ok=True)  # Force the creation of the target folder
            shutil.copytree(assetSourcePath, assetTargetPath)
            print(f"Assets copied to the {assetTargetPath} folder")
        else:
            print(f"Assets source folder does not exist: {assetSource}")

def renderPage(pageHTML, permalink):
    # 5.1 Initialise some of the global template variables
    templateFolder = siteConfig.templatesFolder
    templateFile = siteConfig.templateFile
    outputFolder = siteConfig.outputFolder

    # Extract some metadata from pageData
    title = siteConfig.title
    description = siteConfig.description

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
    snippetFolder = siteConfig.snippetsFolder
    snippetFile = snippetFile
    # outputFolder = 'site'

    # Initialise Jinja2
    file_loader = FileSystemLoader(snippetFolder)
    env = Environment(loader=file_loader)

    # Render with Jinja2
    targetSnippet = env.get_template(snippetFile)
    renderedSnippet = targetSnippet.render(snippetContent=snippetContent)

    return renderedSnippet

def getPageMarkUp(pageContentBlocks):
    pageHTML = ""

    for p in pageContentBlocks:    
        snippetFile= f"{p['blockType']}.html"
        snippetContent = p['blockContent']

        pageHTML += "\n" + renderSnippet(snippetContent, snippetFile)

    return pageHTML

def resizeImages():

    outputFolder = siteConfig.outputFolder
    assetsFolder = siteConfig.assestsFolder
    imageFolder = siteConfig.assetsImagesFolder
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
siteConfig = Site
pageContentBlocks = siteConfig.pageContentBlocks

# 2. Remove any existing website folder
removeSite()

# 4. Turn the block from Step 3 in to an HTML object
pageHTML = getPageMarkUp(pageContentBlocks)

# 5. Render the HTML and write it to a file
renderPage(pageHTML,'')

# 6. Copy the assests folder to the Output folder
copyAssets()

# 7. Resize any images in an image folder
resizeImages()

# ... and stop the timer!
endTime = time.time()
duration = endTime - startTime
print(f"Finished in {str(round(duration, 3))} seconds.")
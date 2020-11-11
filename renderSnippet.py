import json, os, shutil
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader


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

blockDetails = {
    "blockType": "heading-1",
    "blockContent": "Lockdown in ChinaTown"
}

snippetFile= f"{blockDetails['blockType']}.html"
snippetContent = blockDetails['blockContent']
renderedSnippet = renderSnippet(snippetContent,snippetFile)
print(renderedSnippet)


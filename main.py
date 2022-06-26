from PIL import Image, ImageOps, ImageDraw, ImageFont
import hashlib
import os
import random as rand
import math
import copy
import string
from WaveDeformer import WaveDeformer


INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'
IGNORED_FILES = ['.gitkeep']
FILE_EXT = '.jpg'
RANDOM_SEED = 2137


def loadFiles(dir):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    for f in IGNORED_FILES:
        if f in files:
            files.remove(f)
    return files

def saveImageWithMD5Name(image, outputDir = OUTPUT_DIR):
    outFilePath = outputDir + 'out' + FILE_EXT
    image.save(outFilePath)
    md5 = hashlib.md5()
    with open(outFilePath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    md5FilePath = outputDir + md5.hexdigest() + FILE_EXT
    image.save(md5FilePath)
    os.remove(outFilePath)
    print(f'File created: ${md5FilePath}')

def initialScaling(image, dimension = (64, 64)):
    # image = ImageOps.flip(image)
    return image.resize(dimension)


def createOutputDir(file):
    dir = OUTPUT_DIR + file.split('.')[0] + '/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def processFile(file):
    outputDir = createOutputDir(file)
    image = Image.open(INPUT_DIR + file)
    # 1 Transformation
    scaledImage = initialScaling(image)
    allImages = [scaledImage]
    saveImageWithMD5Name(scaledImage, outputDir)
    # 2 Transformation
    # rotatedImages = []
    for i in range(0, 12):
        randomFillColor = tuple([int(rand.uniform(0, 255)) for r in range(0,3)])
        rotatedImg = scaledImage.rotate(30 * i, fillcolor=randomFillColor, expand=False)
        saveImageWithMD5Name(rotatedImg, outputDir)
        # rotatedImages.append(rotatedImg)
        allImages.append(rotatedImg)
    # 3 Flip & Mirror
    # flippedImages = []
    for i in range(len(allImages)):
        flippedImg = ImageOps.flip(allImages[i])
        saveImageWithMD5Name(flippedImg, outputDir)
        allImages.append(flippedImg)
        mirroredImg = ImageOps.mirror(allImages[i])
        saveImageWithMD5Name(mirroredImg, outputDir)
        allImages.append(rotatedImg)
    # 4 Wave deformation
    for i in range(len(allImages)):
        deformedImgSin = ImageOps.deform(allImages[i], WaveDeformer(math.sin, 5))
        saveImageWithMD5Name(deformedImgSin, outputDir)
        # allImages.append(deformedImgSin)
        deformedImgCos = ImageOps.deform(allImages[i], WaveDeformer(math.cos, 5))
        saveImageWithMD5Name(deformedImgCos, outputDir)
        # allImages.append(deformedImgCos)
    # 5 Text field
    fnt = ImageFont.truetype("impact.ttf", size=10)
    textLineLegthMin = 3
    textLineLegthMax = 8
    textLinesMax = 4
    files = loadFiles(outputDir) # There were some duplicates in allImages list so reload unique images based on md5 saved gallery
    textImages = [Image.open(outputDir + f) for f in files]
    for i in range(len(textImages)):
        for x in range(0, 5):
            for y in range(0, 5):
                img = copy.deepcopy(textImages[i])
                d = ImageDraw.Draw(img)
                randText = ''
                lines = int(rand.uniform(1, textLinesMax))
                textSize = int(rand.uniform(textLineLegthMin, textLineLegthMax))
                for l in range(0, lines):
                    randText += ''.join(rand.choices(string.ascii_letters, k = textSize))
                    if l < lines - 1:
                        randText += '\n'
                d.multiline_text((x*10, y*10), randText, font=fnt, fill=(0, 0, 0))
                saveImageWithMD5Name(img, outputDir)



if __name__ == '__main__':
    if RANDOM_SEED is not None:
        rand.seed(RANDOM_SEED)

    files = loadFiles(INPUT_DIR)
    print(f'Program will process files: ${files}')
    for f in files:
        processFile(f)
    print('Done')
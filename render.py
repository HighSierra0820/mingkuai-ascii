from PIL import Image,ImageFont,ImageDraw
from genFont import fontPicPath,fontFamilyName,glyphHeight,glyphWidth
import os
import sys
import hashlib
import math

defaultRandSeed=162304
characterLengthLimit=60

marginPixel=glyphHeight*4
characterSpacing=glyphWidth//8

def getPic(ch: str):
    # ordOfCharacter=ord(ch)
    characterImagePath=f'{fontPicPath}{fontFamilyName}_{hex(ord(ch))[2:]:2s}.png'
    assert os.path.exists(characterImagePath),f'File not found: {characterImagePath}'

    hashResult=hashlib.md5(string=ch.encode('utf-8')+defaultRandSeed.to_bytes(4,'big')).hexdigest()
    # hashLength=len(hashResult)
    image=Image.open(characterImagePath)

    if ch!=' ' and int(hashResult[9:14],16)%3>1:
        for i in range(2):
            x=int(int(hashResult[i*4:i*4+2],16)/256.0*glyphWidth)
            y=int(int(hashResult[i*4+2:i*4+4],16)/256.0*glyphHeight)
            imagePixel=image.getpixel((x,y))
            flippedPixel=tuple(0xff-i for i in imagePixel)
            image.putpixel((x,y),flippedPixel)
        
    dim=0.5
    ful=0.9
    
    dimCornerCoeff=[
        # format: (horiLeft,horiRight,vertLeft,vertRight)
        (ful,ful,ful,ful), (ful,ful,ful,ful), (ful,ful,ful,ful), (ful,ful,ful,ful),
        (dim,ful,dim,ful), (ful,dim,dim,ful), (ful,dim,dim,ful), (ful,dim,ful,dim),
    ]
    (horiLeft,horiRight,vertLeft,vertRight)=dimCornerCoeff[int(hashResult,16)%8]
    
    for i in range(glyphWidth):
        for j in range(glyphHeight):
            gradW=i/glyphWidth
            coeffW=gradW*horiLeft+(1-gradW)*horiRight
            gradH=j/glyphHeight
            coeffH=gradH*vertLeft+(1-gradH)*vertRight
            imagePixel=image.getpixel((i,j))
            # newPixel=tuple(int(i*coeffW*coeffH) for i in imagePixel)
            newPixel=tuple(int(i*math.sqrt(coeffW*coeffH)) for i in imagePixel)
            image.putpixel((i,j),newPixel)
    return image

def drawCharacter(image: Image, ch: str, x: int, y: int):
    characterImage=getPic(ch)
    image.paste(characterImage,(x,y))

def render(inputText: str, outputImageName: str):
    # split text
    inputTextArr=inputText.split('\n')
    lines=[]
    for line in inputTextArr:
        while len(line)>characterLengthLimit:
            for i in range(characterLengthLimit-1,-1,-1):
                if line[i]==' ':
                    lines.append(line[:i])
                    line=line[i+1:]
                    break
        lines.append(line)
        lines.append('')
    while(lines[-1]==''):
        lines.pop()
    # render each line
    imageHeight=len(lines)*glyphHeight+2*marginPixel
    imageWidth=characterLengthLimit*glyphWidth+characterLengthLimit*characterSpacing+2*marginPixel
    image=Image.new(mode='RGB',size=(imageWidth,imageHeight))
    imageDraw=ImageDraw.Draw(image)
    for i,line in enumerate(lines):
        for j,ch in enumerate(line):
            drawCharacter(image,ch,marginPixel+j*glyphWidth+characterSpacing*j,marginPixel+i*glyphHeight)
    # invert
    image=image.point(lambda i: 0xff-i)
    # save
    image.save(outputImageName)

if __name__=="__main__":
    args=sys.argv[1:]
    if len(args)!=2:
        print('Usage: render.py <inputTextName> <outputImageName>')
        print('       image rendered will be saved to \'outputImageName.png\'')
        print('       e.g. render.py sample.txt sample_fanta')
        exit(0)
    inputTextName=args[0]
    outputImageName=f"{args[1]}.png"
    assert os.path.exists(inputTextName),f'File not found: {inputTextName}'
    with open(inputTextName,'r') as inputFile:
        inputText=inputFile.read()
    render(inputText, outputImageName)
    print(f'Image saved to {outputImageName}.')
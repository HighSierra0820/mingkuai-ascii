from PIL import Image,ImageFont,ImageDraw

fontPicPath="assets/pic/"
fontFilePath="assets/font/"

fontFamilyName="FantasqueSansMono"
fontType="ttf"
fontSize=36
fontWeight=["Regular","Bold","Italic","BoldItalic"]
fontFileName=f"{fontFilePath}{fontFamilyName}-{fontWeight[0]}.{fontType}"
font=ImageFont.truetype(fontFileName,fontSize)

charset=list(chr(i) for i in range(32,127)) # printable ASCII

glyphHeight=sum(font.getmetrics())
glyphWidth=font.getbbox(' ')[2]

if __name__=="__main__":
    for ch in charset:
        ordOfCh=ord(ch)
        saveName=f'{fontPicPath}{fontFamilyName}_{hex(ordOfCh)[2:]:2s}.png'
        newImage=Image.new(mode='RGB',size=(glyphWidth,glyphHeight))
        newImageDraw=ImageDraw.Draw(newImage)
        newImageDraw.text((0,0),ch,font=font)
        newImage.save(saveName)

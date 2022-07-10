from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from textWrapper import TextWrapper

fontsDirectory = 'fonts/'

class ImageCitate:
    def __init__(self,text,creator,file=False,avatar=False):
        self.text, self.file, self.avatar, self.creator = text, file, avatar, creator

        self.textFont = ImageFont.truetype(f"{fontsDirectory}textFont.ttf", encoding="utf-8", size=36)
        self.signFont = ImageFont.truetype(f"{fontsDirectory}signFont.ttf", encoding="utf-8", size=36)

        self.whiteColor = "#ffffff"

    def work(self):
        wrapper = TextWrapper(self.text, self.textFont, 800)
        resultText = wrapper.wrapped_text()

        imageSize = (1024, 1024)
        textCoords = (imageSize[0]/2, imageSize[1]/2)
        signCoords = (34, 861)
        avatarCoords = (signCoords[0], signCoords[1]-200)
        signCitateOfBestCoords = (imageSize[0]/2, 50)

        image = Image.new('RGB', imageSize)

        if self.avatar != False: avatarImage = Image.open(f'avatars/{self.avatar}', 'r')

        draw = ImageDraw.Draw(image)
        draw.text(signCitateOfBestCoords, "Цитаты великих людей", font=self.signFont, fill=self.whiteColor, anchor="ms")
        draw.text(textCoords, f"«{resultText}».", font=self.textFont, fill=self.whiteColor, anchor="ms")
        draw.multiline_text(signCoords, f"©{self.creator}\n{datetime.now().strftime('%Y-%m-%d')}", font=self.signFont, fill=self.whiteColor)

        if self.avatar != False: image.paste(avatarImage, avatarCoords)

        if not self.file: return image
        else: image.save(f'output/{self.file}')
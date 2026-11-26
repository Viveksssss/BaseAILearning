# # # from PIL import Image, ImageFilter
# # # im = Image.open(r"C:\Users\v1252\Pictures\【哲风壁纸】个性插画-动漫美少女.png")
# # # w,h = im.size
# # # print('Original image size : width:%d height: %d' %(w,h))
# # # im.thumbnail((w // 2, h // 2))
# # # print("Resize image to: %dx%d" % (w // 2, h // 2))
# # # im.save("test2.jpg", "jpeg")
# # # im = Image.open(r"C:\Users\v1252\Pictures\【哲风壁纸】个性插画-动漫美少女.png")

# # # im2 = im.filter(ImageFilter.BLUR)
# # # im2.save("blur.jpg", "jpeg")

# # # im2 = im.filter(ImageFilter.CONTOUR)
# # # im2.save("contour.jpg", "jpeg")


# # from PIL import Image, ImageDraw, ImageFont, ImageFilter
# # import random


# # def rndChar():
# #     return chr(random.randint(65, 90))


# # # 随机颜色1:
# # def rndColor():
# #     return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# # # 随机颜色2：
# # def rndColor2():
# #     return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
# # width = 60 * 4
# # height = 60
# # # Image.new(mode, size, color=None)
# # image = Image.new("RGB", (width, height), (255, 255, 255))
# # # 创建Font对象
# # font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\msyh.ttc", 36)
# # # 创建draw对象并和image绑定
# # # 用于以后绘制像素点和文本
# # draw = ImageDraw.Draw(image)
# # # 通过像素点绘制填充图片
# # for x in range(width):
# #     for y in range(height):
# #         draw.point((x, y), fill=rndColor())

# # # 绘制字母
# # for t in range(4):
# #     draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())
# # # 模糊处理
# # image = image.filter(ImageFilter.BLUR)
# # image.save("code.jpg", "jpeg")


# import chardet

# rs = chardet.detect(b"Hello, world!")
# print(rs)

# data = "江船火独明".encode("gb2312")
# rs = chardet.detect(data)
# print(rs)

# data2 = "此情可待成追忆".encode("utf-8")
# rs2 = chardet.detect(data2)
# print(rs2)


from tkinter import *


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text="Hello, world!")
        self.helloLabel.pack()
        self.quitButton = Button(self, text="Quit", command=self.quit)
        self.quitButton.pack()


app = Application()
# 设置窗口标题:
app.master.title("Hello World")
# 主消息循环:
app.mainloop()

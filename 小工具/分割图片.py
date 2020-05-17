from PIL import Image
import os


class ImageSplit(object):

    def split_image(self, img_path, split_width, index):
        img = Image.open(img_path)
        img_size = img.size
        if img_size[0] > split_width and index > 1:
            width = img_size[0] / 2
            height = img_size[1]
            img_1 = img.crop((0, 0, width, height))
            img_2 = img.crop((width, 0, img_size[0], height))
            img_1.save(img_path.replace('.jpg', '_2.jpg'))
            img_2.save(img_path.replace('.jpg', '_1.jpg'))
            os.remove(img_path)

    def get_image(self, dir_path, split_width):
        for home, dirs, files in os.walk(dir_path):
            if len(files) > 0:
                index = 0
                for img in files:
                    if '.jpg' in img and 'split' not in img:
                        index += 1
                        img_path = os.path.join(home, img)
                        # print(img_path)
                        self.split_image(img_path, split_width, index)

    def init(self):
        flag = True
        while flag:
            dir_path = input('请输入目录：')
            split_width = int(input('请输入多宽的图片需要分割（px）：  '))
            self.get_image(dir_path, split_width)

            is_continue = input('是否继续分割其他图片文件？ 1.继续  2.退出 \n')
            if is_continue != '1':
                flag = False


imageSplit = ImageSplit()
imageSplit.init()
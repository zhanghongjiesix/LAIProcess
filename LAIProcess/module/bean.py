import cv2
import os


class AshenImg:
    def __init__(self, path):
        # print('AshenImg', path)
        if type(path) is str:
            assert os.path.exists(path), '文件不存在!' + '[' + path + ']'
            self.path = path
            # 彩色图片
            self.img = cv2.imread(path, 1)
            if '/' in path:
                tmp = str(path).split('/')
                self.img_name = tmp[len(tmp) - 1]
                self.img_dir = str(path)[0:str(path).rindex('/')]
            else:
                self.img_name = path
                self.img_dir = ''
            if '.' in self.img_name:
                self.img_file_prefix = self.img_name[:self.img_name.rindex('.')]
                self.img_file_suffix = self.img_name[self.img_name.rindex('.')+1:]
            else:
                self.img_file_prefix = self.img_name
                self.img_file_suffix = ''
            self.img_width = int(self.img.shape[1])
            self.img_height = int(self.img.shape[0])
            # (x, y)
            self.img_center = (int(self.img_width / 2), int(self.img_height / 2))
            self.img_incircle_radius = int(min(self.img_width, self.img_height) / 2)
            # print('AshenImg', self.img_name)
            print('img_file_prefix', self.img_file_prefix)
            print('img_file_suffix', self.img_file_suffix)
            print('img_width', self.img_width)
            print('img_height', self.img_height)
            print('img_center', self.img_center)
            print('img_incircle_radius', self.img_incircle_radius)
            print('img_dir', self.img_dir)

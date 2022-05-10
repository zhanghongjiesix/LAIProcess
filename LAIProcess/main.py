import cv2
# 引入模块
from module import pixel_cal as pcal
from module import lai

# ---------输入配置

# 原图像
img_src_ori = 'E:/LAIProcess/static/zhang_4/4.JPG'
# 相机视角 度数 正整数
camera_view_angle_ori = 25
# 视角间隔 度数
angle_blank = 10
# 对切线数量 最终分割会*2
line_count = 5
# 可以手动输入来改变选取的色彩范围
threshold = 150

if __name__ == '__main__':
    # 首先生成裁剪后的图片
    img = pcal.obtain_crop_img(img_src_ori)
    # 然后使用计算主函数
    result = pcal.check_block_pixel_count(img, camera_view_angle_ori, angle_blank, line_count, threshold)
    print('计算结果:')
    print(result)

    cv2.namedWindow('tmp', cv2.WINDOW_NORMAL)
    img2 = cv2.resize(img.img, (640, 640))
    cv2.imshow('tmp', img2)
    cv2.waitKey()

    rs_LAI = lai.cal_LAI(camera_view_angle_ori, angle_blank, line_count, result)
    print('-'*56)
    print('LAI = ' + str(rs_LAI))


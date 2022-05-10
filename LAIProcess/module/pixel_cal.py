import os
import time
import cv2
from module import AshenImg
from module import incircle as ic
from module import bisector as br

# 辅助线配置
line_color = (0, 0, 255)
line_width = 2


def touch_point_position(img, point, incircle_result, point_result):
    """
    输入指定坐标找到相应位置
    :param point: 两元素元组 (x,y)
    :return:
    """
    # cv2.circle(second_step_img.img, point, 10, line_color, -1)
    incircle_position = ic.check_circle_with_point(point[0], point[1], incircle_result, img)
    if incircle_position is None:
        return None
    # print('incircle_position:', incircle_position)
    infan_position = br.check_fan_by_point(point[0], point[1], point_result, img)
    # print('infan_position:', infan_position)
    if infan_position is None:
        return None
    # print('make point position:{}{}'.format(incircle_position, infan_position))
    return incircle_position, infan_position


def output_pixels_rpb(bimg, incircle_result, point_result, need_write_local=True):
    """
    输出
    {
        "x": 0,
        "y": 0,
        "rpg": "255,255,255",
        "no": "C0B0"
    }
    :param bimg:
    :return:
    """
    print('pixels:', bimg.img_width * bimg.img_height)
    _s = time.time()
    result = []
    for h in range(0, bimg.img_height):
        for w in range(0, bimg.img_width):
            img_pixel = (w, h)
            r = touch_point_position(bimg, img_pixel, incircle_result, point_result)
            if r is not None:
                bgr = bimg.img[h, w]
                result.append({
                    "x": img_pixel[0],
                    "y": img_pixel[1],
                    "rgb": str(bgr[2]) + ',' + str(bgr[1]) + ',' + str(bgr[0]),
                    "no": str(r[0]) + str(r[1])
                })
    print('result.size: ', len(result))
    _e = time.time()
    print('output_pixels_rpb 本阶段耗时: %.2fs' % (float(_e - _s)))
    if need_write_local:
        output_data_file = bimg.img_dir + '/' + bimg.img_file_prefix + '_data.txt'
        print()
        print('结果写入文件中: {}'.format(output_data_file))
        _s = time.time()
        with open(output_data_file, 'w') as f:
            for rl in result:
                f.write(str(rl))
                f.write('\n')
        _e = time.time()
        print('本阶段耗时: %.2fs' % (float(_e - _s)))
    print()
    return result


def obtain_crop_img(src):
    print('预处理源图片 输出内切圆的方形 图片 并保存至./static下')
    cropped_img_path = ic.incircle_execute(AshenImg(src))
    print()

    print('内切圆预输入图像')
    second_step_img = AshenImg(cropped_img_path)
    print()
    return second_step_img


def check_block_pixel_count(img, angle_ori, angle_blank, line_count, threshold=160):
    assert type(img) is AshenImg, "输入需要为AshenImg!"
    _start = time.time()
    print('内切圆及嵌套环计算')
    circle_result = ic.circle_in_circle(img, angle_ori=angle_ori, angle_blank=angle_blank, need_guide_line=True)
    print()

    #print(circle_result)

    print('处理对切线')
    point_result = br.bisector(circle_result, img, line_count=line_count, need_guide_line=True)
    print()

    pixels_result = output_pixels_rpb(img, circle_result, point_result, need_write_local=False)

    print('统计数据中..')
    # 结构 { "C0B0": (216435, 6544) }
    #         区块    总像素   天空像素
    map_block_pixels_result = {}
    for point_block in point_result:
        map_block_pixels_result[str(point_block['parentCircle'] + point_block['no'])] = (0, 0)
    for r in pixels_result:
        rgbarr = str(r['rgb']).split(',')
        ir = int(rgbarr[0])
        ig = int(rgbarr[1])
        ib = int(rgbarr[2])
        x = int(r['x'])
        y = int(r['y'])
        t = map_block_pixels_result[r['no']]
        plus_flag = 0
        if ir >= threshold and ig >= threshold and ib >= threshold:
            plus_flag = 1
            cv2.circle(img.img, (x, y), 1, line_color, -1)
        map_block_pixels_result[r['no']] = (t[0] + 1, t[1] + plus_flag)
    _end = time.time()
    print('本阶段耗时: %.2fs' % (float(_end - _start)))
    print()
    return map_block_pixels_result


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # ---------输入配置
    # 原图像
    img_src_ori = './static/test0.jpeg'
    # 相机原视角 度数 正整数
    camera_view_angle_ori = 46
    # 视角间隔 度数
    angle_blank = 15
    # 对切线数量 最终分割会*2
    line_count = 4
    # 可以手动输入来改变选取的色彩范围
    threshold = 200

    second_step_img = obtain_crop_img(img_src_ori)

    check_block_pixel_count(second_step_img, camera_view_angle_ori, angle_blank, line_count, threshold)


    cv2.namedWindow('tmp', cv2.WINDOW_NORMAL)
    img2 = cv2.resize(second_step_img.img, (640, 640))
    cv2.imshow('tmp', img2)
    # cv2.imshow('tmp', second_step_img.img)
    cv2.waitKey()

import math
import cv2
import os
from module import AshenImg

# B G R
stroke_color = (0, 0, 255)
# pixel
stroke_width = 2
# output dir
output_dir = './static'


def incircle_execute(bimg):
    tmp_dir = output_dir + '/' + bimg.img_file_prefix
    if os.path.exists(tmp_dir) is False:
        os.makedirs(tmp_dir)
    # print('tmp_dir:', tmp_dir)
    img = bimg.img
    # (x, y)
    img_center = bimg.img_center
    img_incircle_radius = bimg.img_incircle_radius
    # 裁剪 [y0:y1, x0:x1]
    cropped = img[img_center[1] - img_incircle_radius:img_center[1] + img_incircle_radius, img_center[0] - img_incircle_radius:img_center[0] + img_incircle_radius]
    pre_write_file_path = tmp_dir + '/' + bimg.img_file_prefix + '_cropped.' + bimg.img_file_suffix
    print('pre_write_file_path', pre_write_file_path)
    cv2.imwrite(pre_write_file_path, cropped)
    with open(pre_write_file_path) as f:
        f.flush()
    return pre_write_file_path


def circle_in_circle(bimg, angle_ori=46, angle_blank=20, need_guide_line=True):
    """
    圆环套圆环
    :param bimg:
    :param angle_ori: 原角度
    :param angle_blank: 间隔角度
    :param need_guide_line:
    :return: 返回环数组
    {
        "radius": 0,
        "nextRadius": 0,
        "no": "C0"
    }
    """
    if angle_blank > angle_ori:
        angle_blank = angle_ori
    radius_ori = bimg.img_incircle_radius
    ccount = int(math.ceil(angle_ori / angle_blank))
    if angle_ori % angle_blank > 0:
        # 由于间隔角度是对于整个图像来说 所以对于半径来说应该是对半的
        inner_circle_radius = radius_ori * ((angle_ori % angle_blank) / angle_ori)
    else:
        inner_circle_radius = 0
    blank_circle_radius = radius_ori * (angle_blank / angle_ori)
    print('circle count', ccount)
    print('inner_circle_radius', inner_circle_radius)
    print('blank_circle_radius', blank_circle_radius)
    result = []
    for c in range(ccount):
        tmp_radius = int(radius_ori - c * blank_circle_radius)
        if need_guide_line:
            cv2.circle(bimg.img, bimg.img_center, tmp_radius, stroke_color, stroke_width)
        if (c + 1) >= ccount:
            next_radius = 0
        else:
            next_radius = int(radius_ori - (c + 1) * blank_circle_radius)
        result.append({
            "radius": tmp_radius,
            "nextRadius": next_radius,
            "no": "C{}".format(c)
        })
    return result


def check_round_by_no(datas, no):
    for i in datas:
        if no == i['no']:
            return i
    return None


def check_circle_with_point(x, y, datas, bimg):
    """
    检查一个坐标在某个圆中
    :param x:
    :param y:
    :param circle0:
    :return:
    """
    root_circle = check_round_by_no(datas, 'C0')
    if root_circle is None:
        return None
    root_radius = int(root_circle['radius'])
    r = abs(math.sqrt(math.pow(x - bimg.img_center[0], 2) + math.pow(y - bimg.img_center[1], 2))) < root_radius
    # print('check_circle_with_point 是否在最外层包含的圆内:', r)
    if r is False:
        return None
    for i in reversed(datas):
        cr = abs(math.sqrt(math.pow(x - bimg.img_center[0], 2) + math.pow(y - bimg.img_center[1], 2))) < int(i['radius'])
        if cr:
            return i['no']
    return None


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    bimg = AshenImg('./static/test0.jpeg')
    cropped_img_path = incircle_execute(bimg)
    circle_result = circle_in_circle(AshenImg(cropped_img_path))
    check_circle_with_point(1024, 1024, circle_result)
    print(circle_result)

import math
import cv2
import os
from module import incircle as ic
from module import AshenImg

# B G R
line_color = (0, 0, 255)
line_width = 2


def bisector(circle_result, bimg, line_count=3, need_guide_line=True):
    """

    :param bimg:
    :param line_count:
    :param need_guide_line:
    :return:
    """
    assert type(line_count) is int, '平分线数量需要为int'
    if line_count < 1:
        line_count = 1
    if line_count > 180:
        line_count = 180
    angle_bisector = 360 / (line_count * 2)
    print('angle_bisector', angle_bisector)
    # print('circle_result', circle_result)
    print('circle_result.length', len(circle_result))
    result = []
    for i in range(line_count * 2):
        x1 = bimg.img_center[0] + bimg.img_incircle_radius * math.cos(angle_bisector * i * math.pi / 180)
        y1 = bimg.img_center[1] + bimg.img_incircle_radius * math.sin(angle_bisector * i * math.pi / 180)
        # print('i: {}  x1: {}  y1: {}'.format(i, x1, y1))
        if need_guide_line:
            cv2.line(bimg.img, bimg.img_center, (int(x1), int(y1)), line_color, line_width)
        for index, incircle in enumerate(circle_result):
            radius = int(incircle['radius'])
            angle_start = angle_bisector * i
            angle_end = angle_bisector * (i + 1)
            cx1 = bimg.img_center[0] + radius * math.cos(angle_start * math.pi / 180)
            cy1 = bimg.img_center[1] + radius * math.sin(angle_start * math.pi / 180)
            # print('bisector radius:{}, angle_start:{} index:{}  i:{}'.format(radius, angle_start, index, i))
            cx1next = bimg.img_center[0] + radius * math.cos(angle_end * math.pi / 180)
            cy1next = bimg.img_center[1] + radius * math.sin(angle_end * math.pi / 180)
            cx1center = bimg.img_center[0] + radius * math.cos((angle_start + ((angle_end - angle_start) / 2)) * math.pi / 180)
            cy1center = bimg.img_center[1] + radius * math.sin((angle_start + ((angle_end - angle_start) / 2)) * math.pi / 180)
            # if need_guide_line:
            #     cv2.circle(bimg.img, (int(cx1), int(cy1)), 10, line_color, -1)
            if index == len(circle_result) - 1:
                result.append({
                    'parentCircle': incircle['no'],
                    'angle': angle_bisector,
                    'angleStart': angle_start,
                    'angleEnd': angle_end,
                    'no': 'B{}'.format(i),
                    'point': (cx1, cy1),  # 相对扇形 左上
                    'pointRight': (cx1next, cy1next),  # 相对扇形 右上
                    'pointDown': bimg.img_center,  # 相对扇形 左下
                    'pointDownRight': bimg.img_center,  # 相对扇形 右下
                    'pointCenter': (cx1center, cy1center),
                })
            else:
                cx1DownLeft = bimg.img_center[0] + (circle_result[index + 1]['radius']) * math.cos(angle_start * math.pi / 180)
                cy1DownLeft = bimg.img_center[1] + (circle_result[index + 1]['radius']) * math.sin(angle_start * math.pi / 180)
                cx1DownRight = bimg.img_center[0] + (circle_result[index + 1]['radius']) * math.cos(angle_end * math.pi / 180)
                cy1DownRight = bimg.img_center[1] + (circle_result[index + 1]['radius']) * math.sin(angle_end * math.pi / 180)
                result.append({
                    'parentCircle': incircle['no'],
                    'angle': angle_bisector,
                    'angleStart': angle_start,
                    'angleEnd': angle_end,
                    'no': 'B{}'.format(i),
                    'point': (cx1, cy1),  # 相对扇形 左上
                    'pointRight': (cx1next, cy1next),  # 相对扇形 右上
                    'pointDown': (cx1DownLeft, cy1DownLeft),  # 相对扇形 左下
                    'pointDownRight': (cx1DownRight, cy1DownRight),  # 相对扇形 右下
                    'pointCenter': (cx1center, cy1center),
                })
    return result


def check_fan_by_point(x, y, data, bimg):
    """

    :param x:
    :param y:
    :param data: #bisector() returned
    :param bimg:
    :return:
    """
    tmp = math.atan2(y - bimg.img_center[1], x - bimg.img_center[0])
    # print('tmp before[math.atan2(y1-y0, x1-x0)]: ', tmp)
    tmp2 = math.degrees(tmp)
    if tmp2 < 0:
        tmp2 = 360 + tmp2
    # print('tmp2 after.atan2.todegrees:', tmp2)

    r = None
    for d in data:
        angle_start = d['angleStart']
        angle_end = d['angleEnd']
        # print('fan no: {}, angle start:{}-end:{}'.format(fan_no, angle_start, angle_end))
        if angle_start <= tmp2 < angle_end:
            r = d['no']
            break
    return r


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    bimg = AshenImg('./static/test0/test0_cropped.jpeg')
    circle_result = ic.circle_in_circle(bimg, angle_blank=10)
    for i in circle_result:
        cv2.circle(bimg.img, bimg.img_center, int(i['radius']), line_color, line_width)
    point_result = bisector(circle_result, bimg, 3)
    for p in point_result:
        circle = p['parentCircle']
        pno = p['no']
        (lx1, ly1) = p['point']
        (rx1, ry1) = p['pointRight']
        (ldx1, ldy1) = p['pointDown']
        (rdx1, rdy1) = p['pointDownRight']
        if circle == 'C0' and pno == 'B0':
            print('left.top x:{}, y:{}'.format(lx1, ly1))
            print('right.top x:{}, y:{}'.format(rx1, ry1))
            print('left.bottom x:{}, y:{}'.format(ldx1, ldy1))
            print('right.bottom x:{}, y:{}'.format(rdx1, rdy1))
            cv2.circle(bimg.img, (int(lx1), int(ly1)), 10, line_color, -1)
            cv2.circle(bimg.img, (int(rx1), int(ry1)), 10, line_color, -1)
            cv2.circle(bimg.img, (int(ldx1), int(ldy1)), 10, line_color, -1)
            cv2.circle(bimg.img, (int(rdx1), int(rdy1)), 10, line_color, -1)

    cv2.imshow('tmp', bimg.img)
    cv2.waitKey()
    cv2.destroyAllWindows()


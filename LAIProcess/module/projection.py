import os
import math
import numpy as np
import pandas as pd
from sympy import *
import matplotlib.pyplot as plt

def check_src_data(src):
    """
    检查数据是否合法
    :param src:
    :return:
    """
    if type(src) == list:
        for d in src:
            assert 0 <= float(d) <= 90, '元素[{}]范围要求在0~90间'.format(d)

def cal_nomalization(src):
    """
    归一化
    :param src:
    :return:
    """
    return (2 * src) / math.pi


def cal_ave(src):
    count = 0
    for i in src:
        count = count + i
    if len(src) > 0:
        return count / len(src)
    else:
        return 0


def cal_beta_func(src):
    """
    计算既定数组的beta函数结果
    :param src:
    :return:
    """
    radians = [math.radians(i) for i in src]
    print('转弧度:', radians)
    nomalizations = [cal_nomalization(i) for i in radians]
    print('归一化:', nomalizations)
    # 标准差
    std = cal_ave(nomalizations) * (1 - cal_ave(nomalizations))
    # 方差
    vari = np.var(nomalizations)
    print('标准差:', std)
    print('方差:', vari)
    # beta函数 μ  ν
    beta_mu = (1 - cal_ave(nomalizations)) * (std / vari - 1)
    beta_nu = cal_ave(nomalizations) * (std / vari - 1)
    print('beta函数的两个值 μ:[{}]  ν:[{}]'.format(beta_mu, beta_nu))
    # gamma计算
    beta = math.gamma(beta_mu) * math.gamma(beta_nu) / math.gamma(beta_mu + beta_nu)
    print('beta:', beta)
    return beta, beta_mu, beta_nu


def plot_beta(src):
    beta, beta_mu, beta_nu = cal_beta_func(src)
    x = np.arange(1, 90, 1)
    y = []
    for t in x:
        t = math.radians(t)
        y1 = 2 / (np.pi * beta) * (1 - 2 * t / np.pi) ** (beta_mu - 1) * (2 * t / np.pi) ** (beta_nu - 1)
        y.append(y1)
    with open('E:/博士文件/树冠图片/虎溪樟树-4/beta.txt', 'w') as f:
        f.write(str(x))
        f.write(str(y))
    plt.scatter(x, y, marker='_')
    # plt.ylim((0, 1))
    plt.show()
    plt.pause(10)
    plt.close()


def cal_leaf_projection(src, theta):
    assert type(src) == list, "请传入list"
    assert 0 <= theta < 90, '元素[{}]范围要求在0~90间'.format(theta)
    print('输入的样本角度:{},计算的角度:{}'.format(src, theta))
    check_src_data(src)
    beta, beta_mu, beta_nu = cal_beta_func(src)
    theta = math.radians(theta)  # 输入要求的theta值,并转换为弧度值
    theta_l = np.arctan(1 / np.tan(theta))
    '''当0~theta_l时进行求解G(theta)'''
    x1 = np.arange(0.001, theta_l, 0.01)
    sum1 = 0
    for t in x1:
        a1 = np.cos(theta) * np.cos(t)
        f = 2 / (np.pi * beta) * (1 - 2 * t / np.pi) ** (beta_mu - 1) * (2 * t / np.pi) ** (beta_nu - 1)
        g1 = a1 * f
        sum1 += g1 * 0.01
    '''当theta_l~0.5pi时进行求解G(theta)'''
    x2 = np.arange(theta_l + 0.001, 0.5 * np.pi, 0.01)
    sum2 = 0
    for t in x2:
        f = 2 / (np.pi * beta) * (1 - 2 * t / np.pi) ** (beta_mu - 1) * (2 * t / np.pi) ** (beta_nu - 1)
        psi = np.arccos(1 / (np.tan(theta) * np.tan(t)))
        a2 = np.cos(theta) * np.cos(t) * (1 + (2 / np.pi) * (np.tan(psi) - psi))
        g2 = a2 * f
        sum2 += g2 * 0.01
    print('G(theta):', sum1 + sum2)
    return sum1 + sum2

if __name__ == '__main__':
    x = np.arange(1, 90, 1)
    df = pd.read_excel('E:/博士文件/树冠图片/虎溪樟树-4/天顶角.xlsx')
    src = list(df.loc[:, '天顶角'])
    plot_beta(src)
    y = []
    for t in x:
        y1 = cal_leaf_projection(src, t)
        y.append(y1)
    with open('E:/博士文件/树冠图片/虎溪樟树-4/叶投影函数.txt', 'w') as f:
        f.write(str(x))
        f.write(str(y))
    plt.scatter(x, y, marker='*')
    plt.ylim((0, 1))
    plt.show()
    plt.pause(10)
    plt.close()


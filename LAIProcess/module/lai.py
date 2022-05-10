import math
from module import projection as prj

dct = {}
def cal_omega(camera_view_angle_ori,angle_blank,line_count,data) :
    """
    计算Ω
    :param : data,line_count
    :return: allBlockPixel全部的像素点个数
    """
    print()
    dt_k_order = sorted(data.items(), key=lambda x:x[0])
    #ln P(θ)  ln Pi(θ)
    count = 0
    sumBlk = 0
    sumKey = 0
    sumLni = 0
    allBlockPixel = 0
    
    temp2 = -1
    thTemp = 0
    dtTemp = 0
    while count < len(dt_k_order):
        print(dt_k_order[count])
        sumBlk += dt_k_order[count][1][0]
        dtTemp = dt_k_order[count][1][1]
        if(dtTemp==0):
            dtTemp=1
        sumKey += dtTemp
        allBlockPixel += dt_k_order[count][1][0]
        p = dtTemp/dt_k_order[count][1][0]
        if p!=0:
            # ln_P1+ln_P2+ln_P3+ln_P4
            sumLni += math.log(p, math.e)
        if (count+1)%line_count==0:
            # p(θ)
            kDvb = sumKey/sumBlk
            if kDvb!=0:
                #lnP(θ)
                rsLnP = math.log(kDvb, math.e)
            else:
                rsLnP = 0
            # lnP_i(θ)
            rsLnPi = sumLni/line_count
            if rsLnP==0 or rsLnPi==0:
                rs = 0
            else:
                rs = rsLnP/rsLnPi

            thTemp=camera_view_angle_ori-angle_blank
            if(thTemp<0):
                thTemp=0
            theta = temp2*(camera_view_angle_ori+thTemp)/2
            if(temp2>0):
                camera_view_angle_ori-=angle_blank

            #θ; ln P(θ),Ω,sumBlk
            if theta == 0 and temp2>0:
                lnPt = dct[theta][0]
                rsT = dct[theta][1]
                sbT = dct[theta][2]
                dct[theta]=(rsLnP+lnPt,rs+rsT,sumBlk+sbT)
            else:
                dct[theta]=(rsLnP,rs,sumBlk)

            print('p('+str(theta)+') = '+str(sumKey)+'/'+str(sumBlk)+' = '+str(kDvb))
            print('lnP('+str(theta)+') = '+'lnP('+str(kDvb)+') = '+str(rsLnP))
            print('lnPi('+str(theta)+') = '+str(sumLni)+'/'+str(line_count)+' = '+str(rsLnPi))
            print('Ω('+str(theta)+') = '+str(rs))
            print('-'*56)

            temp2 = -temp2
            sumBlk = 0
            sumKey = 0
            sumLni = 0
        count += 1
    return allBlockPixel

def cal_LAI(camera_view_angle_ori,angle_blank,line_count,data):
    """
    计算LAI
    :param : camera_view_angle_ori,angle_blank,line_count,data
    :return: LAI
    """
    LAI = 0
    allBlockPixel = cal_omega(camera_view_angle_ori,angle_blank,line_count,data)
    print('全部的像素点个数:'+str(allBlockPixel))

    src = []
    for (key,value) in dct.items():
        if key == 0 :
            return LAI
        F = eval(input('输入F('+str(key)+'):'))
        # l = eval(input('输入l('+str(key)+'):'))
        lnP = dct[key][0]
        omega = dct[key][1]
        orgKey = key
        if key<0:
            src = input('输入src,以计算G('+str(key)+'),使用空格分隔:').split(' ')
            src = [float(src[i]) for i in range(len(src))]
            key = -key
        g = prj.cal_leaf_projection(src,key)
        laiTh = (-F*lnP)/(omega*g)
        wTh = dct[orgKey][2]/allBlockPixel
        
        print('LAI('+str(orgKey)+') = -'+str(F)+'*'+str(lnP)+'/'+str(omega)+'/'+str(g)+' = '+str(laiTh))
        print('W('+str(orgKey)+') = '+str(dct[orgKey][2])+'/'+str(allBlockPixel)+' = '+str(wTh))
        
        LAI += wTh*laiTh
    return LAI

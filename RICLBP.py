
from skimage.feature import local_binary_pattern as lbp
import os,sys,math,cv2
import numpy as np
import time
from collections import Counter
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt


def binary_to_decimal(lis):
    dec=(2**3)*lis[3]+(2**2)*lis[2]+(2**1)*lis[1]+(2**0)*lis[0]
    return int(dec)

def compare(pix,center):
    if pix>=center:
        return 1
    else:
        return 0
def dec2bin(val):
    l=[int(x) for x in bin(val)[2:]]
    b=[0]*(8-len(l))
    b.extend(l)
    dia=b[0::2]
    st=b[1::2]
    return dia,st

def getlbp(img): 
    neighbours=8
    counter=0
    h,w=img.shape
    im=np.pad(img,((1,1),(1,1)),mode='constant')
    dia_img=np.zeros((h,w),dtype=np.uint8)
    str_img=np.zeros((h,w),dtype=np.uint8)
    for x in range(1,h+1):
        for y in range(1,w+1):
    #         center=img[i,j]
            dia=[]
            hor=[]
            for counter in range(0,neighbours):
                if counter == 0:
                    dia.append(compare(im[x-1,y-1], im[x,y]))
                elif counter == 1:
                    hor.append(compare(im[x,y-1], im[x,y]))
                elif counter == 2:
                    dia.append(compare(im[x+1,y-1], im[x,y]))
                elif counter == 3:
                    hor.append(compare(im[x+1,y], im[x,y]))
                elif counter == 4:
                    dia.append(compare(im[x+1,y+1], im[x,y]))
                elif counter == 5:
                    hor.append(compare(im[x,y+1], im[x,y]))
                elif counter == 6:
                    dia.append(compare(im[x-1,y+1], im[x,y]))
                elif counter == 7:
                    hor.append(compare(im[x-1,y], im[x,y]))
            dia_img[x-1,y-1]=binary_to_decimal(dia)
            str_img[x-1,y-1]=binary_to_decimal(hor)
    return dia_img,str_img                
# def getlbp(img): 
#     neighbours=8
#     h,w=img.shape
#     img=lbp(image=img,P=neighbours,R=1)
#     dia_img=np.zeros((h,w),dtype=np.uint8)
#     str_img=np.zeros((h,w),dtype=np.uint8)
#     for x in range(0,h):
#         for y in range(0,w):
#     #         center=img[i,j]
#             dia,hor=dec2bin(int(img[x][y]))
#             dia_img[x,y]=binary_to_decimal(dia)
#             str_img[x,y]=binary_to_decimal(hor)
#     return dia_img,str_img 

def get090(arr):
    list0=[]
    list90=[]
    y,x=arr.shape
    for i in range(y):
        for j in range(x):
    #         print(i,j)
            try:
                list0.append((arr[i][j],arr[i][j+1]))
            except:
                pass
            try:
    #             print(arr[j,i],arr[j,i+1])
                list90.append((arr[j][i],arr[j+1][i]))

#                 print(arr[j,i],arr[j+1,i])
            
            except:
                continue
    return list0,list90
        

def get45135(arr):
#     print(np.where(arr==0))
    list45=[]
    list135=[]
    y,x=arr.shape
    for i in range(y):
        for j in range(x):
            try:
                list135.append((arr[i][j],arr[i+1][j+1]))
            except Exception as e:
                pass
            try:
                if (j-1)>=0:
                    list45.append((arr[i][j],arr[i+1][j-1]))
                
            except Exception as e:
                pass
            
    return list45,list135

def groupandcount(lis):
    lis=[(item[1],item[0]) if item[0]>item[1] else (item[0],item[1]) for item in lis]
#     print(len(set(lis)))
    counts = dict()
    for i in lis:
      counts[i] = counts.get(i, 0) + 1
    return counts

def getfeatures(image):
    # t1=time.time()
    im1,im2=getlbp(image)
    # print(time.time()-t1)
    list0,list90=get090(im2)
    a,b=im1.shape
    list45,list135=get45135(im1)
    tot=[]
    tot.extend(list0)
    tot.extend(list45)
    tot.extend(list90)
    tot.extend(list135)
    val=groupandcount(tot)
    bins=[(i,j) for i in range(16) for j in range(16) if i<=j]
    features=['_']*len(bins)
    # print(len(features))
    for idx,i in enumerate(bins):
        # print(idx)
        try:
            features[idx]=val[i]
        except Exception as e:
            features[idx]=0
    return features       
# print(len(bins))
# print(sorted(list0,key=lambda x:(x[0],x[1])))


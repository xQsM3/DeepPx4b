## THIS SCRIPT VISUALIZES PADDLESEG CITYSCAPES COLOR MAP

import math

import cv2 as cv
import numpy as np

class Label():
    def __init__(self,name,id,trainId,category,catId,hasInstances,ignoreInEval,color):
        self.name = name
        self.id = id
        self.trainId = trainId
        self.category = category
        self.catId = catId
        self.hasInstances = hasInstances
        self.ignoreInEval = ignoreInEval
        self.color = color

labels = [
    #       name                     id    trainId   category            catId     hasInstances   ignoreInEval   color
    Label(  'unlabeled'            ,  0 ,      255 , 'void'            , 0       , False        , True         , (  0,  0,  0) ),
    Label(  'ego vehicle'          ,  1 ,      255 , 'void'            , 0       , False        , True         , (  0,  0,  0) ),
    Label(  'rectification border' ,  2 ,      255 , 'void'            , 0       , False        , True         , (  0,  0,  0) ),
    Label(  'out of roi'           ,  3 ,      255 , 'void'            , 0       , False        , True         , (  0,  0,  0) ),
    Label(  'static'               ,  4 ,      255 , 'void'            , 0       , False        , True         , (  0,  0,  0) ),
    Label(  'dynamic'              ,  5 ,      255 , 'void'            , 0       , False        , True         , (111, 74,  0) ),
    Label(  'ground'               ,  6 ,      255 , 'void'            , 0       , False        , True         , ( 81,  0, 81) ),
    Label(  'road'                 ,  7 ,        0 , 'flat'            , 1       , False        , False        , (128, 64,128) ),
    Label(  'sidewalk'             ,  8 ,        1 , 'flat'            , 1       , False        , False        , (244, 35,232) ),
    Label(  'parking'              ,  9 ,      255 , 'flat'            , 1       , False        , True         , (250,170,160) ),
    Label(  'rail track'           , 10 ,      255 , 'flat'            , 1       , False        , True         , (230,150,140) ),
    Label(  'building'             , 11 ,        2 , 'construction'    , 2       , False        , False        , ( 70, 70, 70) ),
    Label(  'wall'                 , 12 ,        3 , 'construction'    , 2       , False        , False        , (102,102,156) ),
    Label(  'fence'                , 13 ,        4 , 'construction'    , 2       , False        , False        , (190,153,153) ),
    Label(  'guard rail'           , 14 ,      255 , 'construction'    , 2       , False        , True         , (180,165,180) ),
    Label(  'bridge'               , 15 ,      255 , 'construction'    , 2       , False        , True         , (150,100,100) ),
    Label(  'tunnel'               , 16 ,      255 , 'construction'    , 2       , False        , True         , (150,120, 90) ),
    Label(  'pole'                 , 17 ,        5 , 'object'          , 3       , False        , False        , (153,153,153) ),
    Label(  'polegroup'            , 18 ,      255 , 'object'          , 3       , False        , True         , (153,153,153) ),
    Label(  'traffic light'        , 19 ,        6 , 'object'          , 3       , False        , False        , (250,170, 30) ),
    Label(  'traffic sign'         , 20 ,        7 , 'object'          , 3       , False        , False        , (220,220,  0) ),
    Label(  'vegetation'           , 21 ,        8 , 'nature'          , 4       , False        , False        , (107,142, 35) ),
    Label(  'terrain'              , 22 ,        9 , 'nature'          , 4       , False        , False        , (152,251,152) ),
    Label(  'sky'                  , 23 ,       10 , 'sky'             , 5       , False        , False        , ( 70,130,180) ),
    Label(  'person'               , 24 ,       11 , 'human'           , 6       , True         , False        , (220, 20, 60) ),
    Label(  'rider'                , 25 ,       12 , 'human'           , 6       , True         , False        , (255,  0,  0) ),
    Label(  'car'                  , 26 ,       13 , 'vehicle'         , 7       , True         , False        , (  0,  0,142) ),
    Label(  'truck'                , 27 ,       14 , 'vehicle'         , 7       , True         , False        , (  0,  0, 70) ),
    Label(  'bus'                  , 28 ,       15 , 'vehicle'         , 7       , True         , False        , (  0, 60,100) ),
    Label(  'caravan'              , 29 ,      255 , 'vehicle'         , 7       , True         , True         , (  0,  0, 90) ),
    Label(  'trailer'              , 30 ,      255 , 'vehicle'         , 7       , True         , True         , (  0,  0,110) ),
    Label(  'train'                , 31 ,       16 , 'vehicle'         , 7       , True         , False        , (  0, 80,100) ),
    Label(  'motorcycle'           , 32 ,       17 , 'vehicle'         , 7       , True         , False        , (  0,  0,230) ),
    Label(  'bicycle'              , 33 ,       18 , 'vehicle'         , 7       , True         , False        , (119, 11, 32) ),
    Label(  'license plate'        , -1 ,       -1 , 'vehicle'         , 7       , False        , True         , (  0,  0,142) ),
]


zoom = 200
offset = 10
dim = math.ceil(math.sqrt(len(labels)) ) * zoom
image = np.zeros((dim+zoom//2,dim+zoom//2,3))+255

row = 0
col = 0

custom_color = ""
for i,label in enumerate(labels):
    if label.trainId == 255 or label.trainId == -1:
        label.color = (0,0,0)
    else:
        custom_color += str(label.color[0]) +" " +str(label.color[1]) +" " +str(label.color[2])+" "

    cv.rectangle(image,(row * zoom + offset, col * zoom + offset),
                 ((row + 1) * zoom + offset,(col + 1) * zoom + offset),
                 label.color,thickness=-1)
    cv.rectangle(image,(row * zoom + offset, col * zoom + offset),
                 ((row + 1) * zoom + offset,(col + 1) * zoom + offset),
                 (255,255,255),thickness=3)


    cv.putText(image,label.name,(row*zoom+zoom//4,col*zoom+offset+zoom//4),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv.LINE_AA)
    cv.putText(image,f"({label.category})",(row*zoom+zoom//4,col*zoom+offset+zoom//4+offset*3),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv.LINE_AA)
    cv.putText(image,f"ID: {label.id}",(row*zoom+zoom//4,col*zoom+offset+zoom//4+6*offset),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv.LINE_AA)
    cv.putText(image,f"TrainID: {label.trainId}",(row*zoom+zoom//10,col*zoom+offset+zoom//4+9*offset),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv.LINE_AA)
    row += 1
    if row*zoom+zoom+offset> image.shape[0]:
        row = 0
        col += 1


print(custom_color)
#cv.rectangle(image,(0,0),(500,500),(255,0,0),-1)
image_bgr = image[...,::-1]
cv.namedWindow("Labels",1500)
#cv.imshow("Labels",image_bgr)
#cv.waitKey(0)
cv.destroyAllWindows()
cv.resize(image_bgr,(1700,1700))

cv.imwrite("custom_color_paddleseg_cityscapes.png",image_bgr)


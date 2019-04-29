# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 10:08
# @Author  : DrMa

import tensorflow as tf
import numpy as np
def My_func(xs, ys):
    sum=0
    for i in range(len(xs)):
        temp_sum=0
        y=ys[i]#拿到每个样本的标签
        x=xs[i]#拿到每个样本的输出
        label_num=len(x)
        x_rights=[]
        right_indexs=[]
        for every_y in y:
            if every_y==-1:
                break
            x_rights.append(x[every_y])
            right_indexs.append(every_y)
        x=np.delete(x,right_indexs,axis=-1)

        for x_right in x_rights:
            for x_wrong in x:
                result=1-(x_right-x_wrong)
                temp_sum+=result
        temp_sum=temp_sum/label_num
        sum+=temp_sum
    final_result=np.array([sum/len(xs)],dtype=np.float32)
    return final_result
def multiLabelMarginLoss(tensor_a, tensor_b):
    tile_tensor_a = tf.py_func(My_func, [tensor_a, tensor_b], tf.float32)
    return tile_tensor_a

a=tf.constant([[0.1, 0.2, 0.4, 0.8],[0.1, 0.2, 0.4, 0.8]])
b=tf.constant([[0,3,-1,-1],[0,3,-1,-1]])
c=multiLabelMarginLoss(a,b)
sess = tf.Session()
loss=sess.run(c)
print(loss)



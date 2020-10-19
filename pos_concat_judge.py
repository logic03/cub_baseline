import os
import random

f1 = open("F:/ACCV/cub_baseline-master/models/label_clean_r50_448.txt")#第一个正样本
f2 = open("F:/ACCV/cub_baseline-master/models/label_clean_efnetb5.txt")#第二个正样本
f3 = open("F:/ACCV/cub_baseline-master/models/images_train3.txt")#训练的所有样本

list1 = []
list2 = []
list3 = []

#得到第一个正样本列表
for line1 in f1.readlines():
    list1.append(line1)
print("list1:", len(list1))

#得到第二个正样本列表
for line2 in f2.readlines():
    list2.append(line2)
print("list2:", len(list2))

#得到img_train所有样本的列表
for line3 in f3.readlines():
    list3.append(line3)
print("list3:", len(list3))

#取到两个正样本的并集
union = list(set(list1).union(set(list2)))
#print("union:", len(union))

#接下来按照类别挑选出所有第一个类别0001的列表元素
#放到另一个列表temp_list里面，计算这个的长度占总的imgtrain.txt里面的长度
#先看一下是不是大于90%

num_class = 5000

write_list_total = []#要写入的总的正样本路径
write_id_bigger_than_90 = []#大于90%的正样本

for k in range(num_class):
    #生成一个类别
    temp_list = []  # 用于放置第0000个类别的所有样本的聚类后的正样本的并集
    temp_train_list = [] # 用于放置第0000个类别的所有训练样本的图片
    #最后的时候看len(temp_list)在len(temp_train_list)的比例
    for i in range(len(union)):
        path_i = union[i]  # 得到第i个路径
        path_i_split = path_i.split("/")
        cls_i_str = path_i_split[1]  # 得到第i个路径的类别
        # 如果字符刚好匹配0000，那么就加入0000的
        cls_i_num = int(cls_i_str)  # 转成了数字进行匹配
        #判断这个类别是不是等于第k个类别
        if cls_i_num == k:
            temp_list.append(path_i)

    #统计完了聚类生成的第k个类别，就要统计原来的所有的第k个类别有多少
    #从imgtrain.txt里面读取
    for j in range(len(list3)):
        path_train_j = list3[j]
        temp = path_train_j.strip().split(" ")[1]#得到这个文件的总的路径
        path_train_j_split = temp.split("/")[1]#从路径中分离出类别
        cls_train_j_num = int(path_train_j_split)
        if cls_train_j_num == k:
            temp_train_list.append(path_train_j)

    len1 = len(temp_list)
    len2 = len(temp_train_list)
    print("num_k:", k)
    print("len1:", len1)
    print("len2:", len2)

    #这里就可以判断这个类别的数目是不是大于90%了
    #这里计算负样本，就是取temp_train_list和temp_list的差
    #做差之前就要先把序号去掉
    train_list = []
    for kk in range(len(temp_train_list)):
        temp = temp_train_list[kk].strip().split(" ")[1]  # 得到这个文件的总的路径
        train_list.append(temp + '\n')

    #当train_list的长度大于temp_list的时候,取剩下的负样本
    if len2 >= len1:
        temp_diff_list = list(set(train_list).difference(temp_list))
    else:
        pass

    cal = int(len2 * 0.65) #0.65可以改成0.9就是卡90，0.01就是全取
    if len1 < cal:
        print("lower_pros")
        diff = int(cal) - int(len1) + 1#还需要从负样本中随机抽几张,多取一张取整
        print("diff:", diff)
        diff_list = random.sample(temp_diff_list, diff)
        print("diff_list:", diff_list) #打印出选取的，然后再和并集一起写入
        write_list = list(set(temp_list).union(diff_list))
    else:
        write_id_bigger_than_90.append(k)
        write_list = temp_list #直接把temp_list写入

    write_list_total.extend(write_list)#把这个类别计算出的总的路径加入


#得到了要写入的正样本列表
f4 = open("F:/ACCV/cub_baseline-master/models/pos_concat_5000_65.txt", "a")
for t in range(len(write_list_total)):
    f4.write(write_list_total[t])

#记录大于90的ID
f5 = open("F:/ACCV/cub_baseline-master/models/Id_bigger_than_90_5000_65.txt", "a")
for h in range(len(write_id_bigger_than_90)):
    num = str(write_id_bigger_than_90[h])
    f5.write(num + '\n')





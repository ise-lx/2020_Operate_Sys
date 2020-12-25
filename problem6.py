import numpy as np
import math
import matplotlib.pyplot as plt
import os
import random
import queue

# 为作业分配的物理块数
global_block_num = 3


# 定义一个page类,含有page_num、access和modification三个属性
class Page:
    def __init__(self, page_num=-1, access=0, modification=0):
        self.page_num = page_num
        self.access = access
        self.modification = modification


# generate command sequence
def generate_command():
    num = 320  # generate 320 commands
    sequence_list = []  # save commands in a list
    current_num = 0  # current number of commands
    while current_num < 320:
        m0 = random.randint(0, 319)  # select a random integer in [0,319]
        sequence_list.append(m0 + 1)  # add M+1 to sequence list, exc M+1
        m1 = random.randint(0, m0 + 1)  # select a random integer in [0, M+1]
        sequence_list.append(m1)  # 执行 M1
        sequence_list.append(m1 + 1)  # 顺序执行 M1+1
        m2 = random.randint(m1 + 2, 319)  # 随机选取并执行
        sequence_list.append(m2)  # 执行 m2
        current_num += 4  # 产生了4条指令地址
    return sequence_list


# 在列表中查找指定元素
def findindex(list, value):
    for i in range(len(list)):
        temp = list[i]
        if temp == value:
            return i
    return -1


# 指令地址转换页号
def convert_page(address):
    pages = []  # 存放页号
    for ad in address:
        pages.append(int(ad / 10))
    return pages


# 选择一个页面换入换出的置换算法
def select_algorithm(option='FIFO'):
    if option.strip() == 'FIFO':
        print("使用FIFO置换算法")
    elif option.strip() == 'LRU':
        print('使用LRU置换算法')
    elif option.strip() == 'LFU':
        print("使用LFU置换算法")
    elif option.strip() == 'CLOCK':
        print("使用CLOCK置换算法")
    elif option.strip() == 'OPT':
        print('使用OPT置换算法')
    else:
        print("输入错误,没有", option.strip(), "置换算法")
        print("请重新输入")


# 初始化物理块
# 页号  访问时间access
def init_block():
    block_list = []  # 存放页表项的列表
    for page in range(0, global_block_num):  # 初始化页表信息
        page_item = Page()
        page_item.page_num = -1  # 页号
        page_item.access = 0  # 访问字段，用于记录本页在一段时间内的访问次数或记录本页已多长时间未被访问
        block_list.append(page_item)
    return block_list


# 初始化作业
def init_pages(pages):
    pages_list = []
    for page in pages:
        page_item = Page()
        page_item.page_num = page
        page_item.access = 0  # 访问字段，用于记录本页在一段时间内的访问次数或记录本页已多长时间未被访问
        pages_list.append(page_item)
    return pages_list


# 根据页号blocks中查找
def isExist(pagenum, blocks):
    exist_flag = False  # 判断在快表中是否存在的标志
    for i in range(0, global_block_num):
        page = Page()
        page = blocks[i]
        if int(page.page_num) == int(pagenum):
            exist_flag = True
            return exist_flag
    return exist_flag


#
def find(pagenum, blocks):
    exist_flag = False  # 判断在快表中是否存在的标志
    for i in range(0, global_block_num):
        page = Page()
        page = blocks[i]
        if int(page.page_num) == int(pagenum):
            return i
    return -1


# 在内存块查找空闲区
def find_space(blocks):
    for i in range(len(blocks)):
        block = blocks[i]
        if int(block.page_num) == -1:
            return i  # 如果找到空闲区，返回下标否则返回-1
    return -1


# 找到一个access max的物理块,并返回下标
def find_time_max(blocks):
    max_time_index = 0
    for i in range(len(blocks)):
        temp_block = blocks[i]
        if temp_block.access > blocks[max_time_index].access:
            max_time_index = i
    return max_time_index


# 找到一个access min的物理块,并返回下标
def find_time_min(blocks):
    min_index = 0
    for i in range(len(blocks)):
        temp_block = blocks[i]
        if temp_block.access < blocks[min_index].access:
            min_index = i
    return min_index


# 找到将来最久的页号,并返回下标
def find_longest_future(blocks, pages, begin_index):  # pages = [2,2,4,......]
    return_index = -1
    max_index = -1
    length = len(blocks)
    for i in range(len(blocks)):
        temp_block = blocks[i]
        temp_block_num = temp_block.page_num

        index = findindex(pages[begin_index:], temp_block_num)  # 对物理块号i对应的页号在pages列表中查询
        if index == -1:
            return i
        else:
            if index > max_index:
                max_index = index
                return_index = i
    return return_index


# 找到最近用的最少的页号,并返回下标
def find_min_use_recently(blocks, pages, end_index):  # pages = [2,2,4,......]
    return_index = -1
    min_index = 100000
    for i in range(len(blocks)):
        temp_block = blocks[i]
        temp_block_num = temp_block.page_num

        index = findindex(pages[:end_index], temp_block_num)  # 对物理块号i对应的页号在pages列表中查询
        if index > -1:
            if index < min_index:
                max_index = index
                return_index = i
    return return_index


# 打印物理块的分配情况
def show_blocks(blocks):
    for i in range(len(blocks)):
        temp_block = blocks[i]
        print("block{}: {}".format(i, temp_block.page_num),end='\t\t')
    print('\n')
    print("-------------------------")


# FIFO算法
def FIFO(blocks, pages_list):
    not_lack_num = 0
    for page in pages_list:
        print("等待分配物理快的页号： ", page.page_num)
        page_num = page.page_num
        if isExist(page_num, blocks):  # 页号在内存, 未发生缺页
            print("该页号已在内存中")
            not_lack_num += 1  # 未发生缺页的数量 +1
        else:
            index = find_space(blocks)
            if index == -1:  # 找到空闲物理块号
                max_time_index = find_time_max(blocks)
                print("换出pagenum:",blocks[max_time_index].page_num,end='\t\t')
                blocks[max_time_index] = page  # 放入物理块中
                print("换入:",page.page_num)
            else:
                blocks[index] = page  # 放入空闲块中

        for bpage in blocks:  # 对于每个page number != -1的物理块的access+1
            if bpage.page_num != -1:
                bpage.access += 1
        show_blocks(blocks)  # 打印一次分配情况

    lack_page_rate = 1 - (not_lack_num / 320.)  # 计算缺页率
    print("缺页率为： ", lack_page_rate)
    print("命中率为： ", (1 - lack_page_rate))
    return lack_page_rate




# 最佳置换算法
def OPT(blocks, pages):
    print("OPT置换算法")
    pages_list = init_pages(pages)
    not_lack_num = 0
    for i in range(len(pages_list)):
        page = pages_list[i]
        print("等待分配物理快的页号： ", page.page_num)
        page_num = page.page_num
        if isExist(page_num, blocks):  # 页号在内存, 未发生缺页
            print("该页号已在内存中")
            not_lack_num += 1  # 未发生缺页的数量 +1
        else:
            index = find_space(blocks)
            if index == -1:  # 未找到空闲物理块号
                min_use_index = find_longest_future(blocks, pages, i)
                # print("最近最少使用的下标为：", min_use_index)
                print("换出pagenum:",blocks[min_use_index].page_num,end='\t\t')
                print("换入:",page.page_num)
                blocks[min_use_index] = page  # 放入物理块中
            else:
                blocks[index] = page  # 放入空闲块中
        show_blocks(blocks)  # 打印一次分配情况

    lack_page_rate = not_lack_num / 320.  # 计算缺页率
    print("缺页率为： ", lack_page_rate)
    print("命中率为： ", (1 - lack_page_rate))
    return  lack_page_rate


# 最近最久未使用算法
def LRU(blocks, pages_list):
    print("LRU置换算法")
    not_lack_num = 0
    for page in pages_list:
        print("等待分配物理快的页号： ", page.page_num)
        page_num = page.page_num
        if isExist(page_num, blocks):  # 页号在内存, 未发生缺页
            print("该页号已在内存中")  # 若在内存access = 1
            block_index = find(page_num, blocks)
            blocks[block_index].access = 0  # 清零

            not_lack_num += 1  # 未发生缺页的数量 +1
        else:
            index = find_space(blocks)
            if index == -1:  # 未找到空闲物理块号
                max_time_index = find_time_max(blocks)
                print("换出pagenum:",blocks[max_time_index].page_num,end='\t\t')
                print("换入:",page.page_num)
                blocks[max_time_index] = page  # 放入物理块中
            else:
                blocks[index] = page  # 放入空闲块中

        for bpage in blocks:  # 对于每个page number != -1的物理块的access+1
            if bpage.page_num != -1:
                bpage.access += 1
        show_blocks(blocks)  # 打印一次分配情况

    lack_page_rate = 1 - (not_lack_num / 320.)  # 计算缺页率
    print("缺页率为： ", lack_page_rate)
    print("命中率为： ", (1 - lack_page_rate))
    return lack_page_rate


# 最近最少使用算法
def LFU(blocks, pages):
    print("最近最少使用算法")
    pages_list = init_pages(pages)
    not_lack_num = 0
    for i in range(len(pages_list)):
        page = pages_list[i]
        print("等待分配物理快的页号： ", page.page_num)
        page_num = page.page_num
        if isExist(page_num, blocks):  # 页号在内存, 未发生缺页
            print("该页号已在内存中")
            block_index = find(page_num, blocks)
            blocks[block_index].access += 1
            not_lack_num += 1  # 未发生缺页的数量 +1
        else:
            index = find_space(blocks)
            if index == -1:  # 未找到空闲物理块号
                min_use_index = find_time_min(blocks)
                print("换出pagenum:",blocks[min_use_index].page_num,end='\t\t')
                print("换入:",page.page_num)
                blocks[min_use_index] = page  # 放入物理块中
                blocks[min_use_index].access = 1
            else:
                blocks[index] = page  # 放入空闲块中
                blocks[index].access = 1
        show_blocks(blocks)  # 打印一次分配情况

    lack_page_rate = 1-(not_lack_num / 320.)  # 计算缺页率
    print("缺页率为： ", lack_page_rate)
    print("命中率为： ", (1 - lack_page_rate))
    return lack_page_rate


# 改进前循环队列
def circlequeue(blocks):
    index = -1
    for i in range(len(blocks)):
        temp_block = blocks[i]
        temp_block_access = temp_block.access
        if temp_block.access == 1:
            blocks[i].access = 0
        else:
            blocks[i].access = 1
            index = i
            break
    if index == -1:  # 没有空闲块
        for i in range(len(blocks)):
            temp_block = blocks[i]
            if temp_block.access == 1:
                blocks[i].access = 0
            else:
                blocks[i].access = 1
                index = i
                break
    return index


# 改进后循环队列
def impcirclequeue(blocks):
    index = -1
    count_zero_list = []
    for i in range(len(blocks)):
        temp_block = blocks[i]
        temp_block_access = temp_block.access
        if temp_block.access == 1:
            blocks[i].access = 0
        else:
            # blocks[i].access = 1
            index = i
            count_zero_list.append(i)
            # break
    if index == -1:  # 没有空闲块
        for i in range(len(blocks)):
            temp_block = blocks[i]
            if temp_block.access == 1:
                blocks[i].access = 0
            else:
                # blocks[i].access = 1
                index = i
                count_zero_list.append(i)
                # break

    first_flag = 0  # 第一类情况
    second_flag = 0  # 第二类情况

    for i in count_zero_list:
        temp = blocks[i]
        if temp.access == 0 and temp.modification == 0:
            index = i
            blocks[index].access = 1
            first_flag = 1
            break
    if first_flag == 0:
        for i in count_zero_list:
            temp = blocks[i]
            if temp.access == 0 and temp.modification == 1:
                index = i
                blocks[index].access = 1
                second_flag = 1
                break

    return index


# CLOCK算法
def CLOCK(blocks, pages):
    print("CLOCK算法")
    pages_list = init_pages(pages)
    not_lack_num = 0
    for i in range(len(pages_list)):
        page = pages_list[i]
        print("等待分配物理快的页号： ", page.page_num,end='\t\t')
        page_num = page.page_num
        if isExist(page_num, blocks):  # 页号在内存, 未发生缺页
            print("该页号已在内存中")
            block_index = find(page_num, blocks)
            blocks[block_index].access = 1
            not_lack_num += 1  # 未发生缺页的数量 +1
        else:
            index = find_space(blocks)
            if index == -1:  # 未找到空闲物理块号
                min_use_index = circlequeue(blocks)
                # print("clock下标为：", min_use_index)
                print("换出pagenum:",blocks[min_use_index].page_num,end='\t\t')
                print("换入:",page.page_num)
                blocks[min_use_index] = page  # 放入物理块中
                blocks[min_use_index].access = 1
            else:
                print()
                blocks[index] = page  # 放入空闲块中
                blocks[index].access = 1
        show_blocks(blocks)  # 打印一次分配情况

    lack_page_rate = 1-(not_lack_num / 320.)  # 计算缺页率
    print("缺页率为： ", lack_page_rate)
    print("命中率为： ", (1 - lack_page_rate))
    return lack_page_rate


# 改进型Clock算法
def IMCLOCK(blocks, pages):

    print("改进后的CLOCK算法")
    pages_list = init_pages(pages)
    not_lack_num = 0
    for i in range(len(pages_list)):
        random_write(blocks)  # 随机写入
        page = pages_list[i]
        print("等待分配物理快的页号： ", page.page_num)
        page_num = page.page_num
        if isExist(page_num, blocks):  # 页号在内存, 未发生缺页
            print("该页号已在内存中")
            block_index = find(page_num, blocks)
            blocks[block_index].access = 1
            not_lack_num += 1  # 未发生缺页的数量 +1
        else:
            index = find_space(blocks)
            if index == -1:  # 未找到空闲物理块号
                min_use_index = impcirclequeue(blocks)
                # print("clock下标为：", min_use_index)
                print("换出pagenum:",blocks[min_use_index].page_num,end='\t\t')
                print("换入:",page.page_num)
                blocks[min_use_index] = page  # 放入物理块中
                blocks[min_use_index].access = 1
            else:
                print()
                blocks[index] = page  # 放入空闲块中
                blocks[index].access = 1
        show_blocks(blocks)  # 打印一次分配情况

    lack_page_rate = 1-(not_lack_num / 320.)  # 计算缺页率
    print("缺页率为： ", lack_page_rate)
    print("命中率为： ", (1 - lack_page_rate))
    return lack_page_rate


# 修改位随机写入
def random_write(blocks):
    print("出现随机写入",end='\t\t')
    write_flag = random.randint(0,100)
    if write_flag < 10:                 # 有10%的概率能写入
        ran_block_index = random.randint(0,global_block_num-1)            # 随机选择一个物理块进行修改
        blocks[ran_block_index].modification = 1
        print("写入的页号：",blocks[ran_block_index].page_num)






# 清空物理块信息
def clear_blocks(blocks):
    for i in range(len(blocks)):
        blocks[i].access = 0
        blocks[i].page_num = -1









def main():
    # print("main函数")
    seq = generate_command()
    print("随机生成的指令序列：")
    for i in range(len(seq)):
        if i % 20 == 0:
            print()
        print(seq[i],end=',')
    print()



    pages = convert_page(seq)  # 转换页号
    print("页面引用串：")
    for i in range(len(pages)):
        if i % 20 == 0:
            print()
        print(pages[i],end=',')
    print()





    block_list = init_block()  # 初始化
    test_list = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    pages_list = init_pages(pages)  # 初始化
    test_list_pages = init_pages(test_list) #测试初始化


    while True:
        print("---------请选择使用的置换算法----------")
        print("1. FIFO算法", end='\t\t')
        print("2.OPT算法", end='\n')
        print("3.LRU算法", end='\t\t')
        print("4.LFU算法", end='\n')
        print("5.CLOCK算法", end='\t\t')
        print("6.改进后CLOCK算法",end='\n')
        print("7.运行所有置换算法",end='\t\t')
        print("0.退出")
        print("----------------------------------")
        select = input("请输入0-7:\t")
        select = select.strip('\n')
        select = select.strip()
        select = int(select)
        if select == 1:
            print("FIFO算法")
            FIFO(block_list, pages_list)
            clear_blocks(block_list)
        elif select == 2:
            print("OPT算法")
            OPT(block_list, pages)
            clear_blocks(block_list)
        elif select == 3:
            print("LRU算法")
            LRU(block_list, pages_list)
            clear_blocks(block_list)
        elif select == 4:
            print("LFU算法")
            LFU(block_list, pages)
            clear_blocks(block_list)
        elif select == 5:
            print("CLOCK算法")
            CLOCK(block_list, pages)
            clear_blocks(block_list)
        elif select == 6:
            print("改进后的CLOCK算法")
            # random_write(block_list)        # 随机写入
            IMCLOCK(block_list,pages)
            clear_blocks(block_list)
        elif select == 7:
            print("所有置换算法：")
            lack_all_list = []

            print("FIFO算法")
            fifolack = FIFO(block_list, pages_list)
            clear_blocks(block_list)
            print("OPT算法")
            optlack = OPT(block_list, pages)
            clear_blocks(block_list)
            print("LRU算法")
            lrulack= LRU(block_list, pages_list)
            clear_blocks(block_list)
            print("LFU算法")
            lfulack = LFU(block_list, pages)
            clear_blocks(block_list)
            print("CLOCK算法")
            clocklack = CLOCK(block_list, pages)
            clear_blocks(block_list)
            print("改进后的CLOCK算法")
            random_write(block_list)        # 随机写入
            imclocklack = IMCLOCK(block_list,pages)
            clear_blocks(block_list)
            lack_all_list.append(fifolack)
            lack_all_list.append(optlack)
            lack_all_list.append(lrulack)
            lack_all_list.append(lfulack)
            lack_all_list.append(clocklack)
            lack_all_list.append(imclocklack)

            x = ['FIFO','OPT','LRU','LFU','CLOCK','IMCLOCK']
            y = lack_all_list
            plt.plot(x,y)
            # plt.xlabel("FIFO，OPT,LRU,LFU,CLOCK,IMCLOCK")
            plt.ylabel("lack page rate")
            plt.show()

        elif select == 0:
            break
        else:
            print("输入不合法,请重新输入")

    # FIFO(block_list, pages_list)  # FIFO调度算法
    # OPT(block_list,pages)       # 最佳置换算法
    # OPT(block_list,test_list)     # 最佳置换 test
    # LRU(block_list,pages_list)       # 最近最久未使用置换算法
    # LFU(block_list, test_list)  # 最少使用置换算法test
    # LFU(block_list,pages)       # 最少使用算法
    # CLOCK(block_list,pages)         # CLOCK算法
    # CLOCK(block_list,test_list)         # CLOCK算法 test
    # IMCLOCK(block_list,test_list)         # CLOCK算法 test


if __name__ == '__main__':
    main()

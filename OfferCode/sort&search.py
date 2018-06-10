# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 11:13:29 2018

@author: lenovo
"""
# 插入排序
def insert_sort(array):
    for i in range(len(array)):
        for j in range(i):
            if array[i] < array[j]:
                array.insert(j, array.pop(i))
                break
    return array

# 希尔排序
def shell_sort(array):
    gap = len(array)
    while gap > 1:
        gap = gap // 2
        for i in range(gap, len(array)):
            for j in range(i % gap, i, gap):
                if array[i] < array[j]:
                    array[i], array[j] = array[j], array[i]
    return array

# 选择排序
def select_sort(array):
    for i in range(len(array)):
        x = i  # min index
        for j in range(i, len(array)):
            if array[j] < array[x]:
                x = j
        array[i], array[x] = array[x], array[i]
    return array

# 冒泡排序
def bubble_sort(array):
    for i in range(len(array)):
        for j in range(i, len(array)):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]
    return array

# 快速排序
def quick_sort(array, left, right):
    start = left
    finish = right
    if left < right:
        key = array[left]
        while left < right:
            while left < right and array[right] >= key:
                right -= 1
            array[left] = array[right]
            while left < right and array[left] <= key:
                left += 1
            array[right] = array[left]
        array[left] = key
        quick_sort(array, start, left-1)
        quick_sort(array, left+1, finish)

# 归并排序
def merge_sort(array, low, high):
    if low < high:
        mid = (low+high)/2
        merge_sort(array, low, mid)
        merge_sort(array, mid+1, high)
        i = low
        j = mid+1
        temp = []
        while i <= mid and j <= high:
            if array[i] <= array[j]:
                temp.append(array[i])
                i += 1
            else:
                temp.append(array[j])
                j += 1
        while i <= mid:
            temp.append(array[i])
            i += 1
        while j <= high:
            temp.append(array[j])
            j += 1
        array[low : high+1] = temp

# 建立一个二叉树
class Tree:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def make_tree(val, deep):
    if deep < 4:
        root = Tree(val)
        root.left = make_tree(val*2, deep+1)
        root.right = make_tree(val*2+1, deep+1)
        return root
    else:
        return None
root = make_tree(1, 1)

# 二分查找
def binary_search(find, list1) :
  low = 0
  high = len(list1)
  while low <= high :
    mid = (low + high) / 2
    if list1[mid] == find :
      return mid
    #左半边
    elif list1[mid] > find:
      high = mid -1
    #右半边
    else :
      low = mid + 1
  #未找到返回-1
  return -1

a = [1,2,3,3,4,5,6]
print binary_search(3, a)



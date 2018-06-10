# -*- coding: utf-8 -*-
"""
Created on Tue May 15 15:16:58 2018

@author: lenovo
"""
import numpy as np  # 引入numpy  
import scipy as sp  
from scipy.optimize import leastsq  # 引入最小二乘函数 
import xlwt

# 目标函数  
def fit_func(p, x):    
    return p*x  
    
# 损失函数  
def residuals_func(p, y, x, errorTerm, regularTerm, regularCoe, positiveTerm):
    ret = np.array(fit_func(p, x) - y)
    ret = ret.tolist()
    ret = ret[0]
    err, reg, po = 0, 0, 0
    # 选择误差项类别
    if errorTerm == 'gaussian':
        err = [r**2 for r in ret]
    elif errorTerm == 'laplace':
        err = [abs(r) for r in ret]
    # 选择正则项类别
    if regularTerm == 'L1':
        reg = sum([abs(i) for i in p])
    elif regularTerm == 'L2':
        reg = sum([i**2 for i in p])
    elif regularTerm == 'L1+L2':
        reg = sum([abs(i)+(i**2) for i in p])
    # 选择正定项类别
    if positiveTerm == 'sign':
        po = sum([-1000*min(i, 0) for i in p])
    elif positiveTerm == 'relu':
        po = sum([-1*min(i, 0) for i in p])
    # 返回损失函数a
    residuals = []
    for e in err:
        residuals.append(e + regularCoe*reg + 0.05*po)
    return residuals

if __name__ == '__main__':
    # load data
    data = sp.io.loadmat('input.mat')
    x = np.mat(data['center'])
    y = np.mat(data['data'])
    p = np.random.random(size=(y.shape[0], x.shape[0]))
    # 定义超参数
    errorTerms = ['gaussian', 'laplace']
    regularTerms = ['L1', 'L2', 'L1+l2', 'uniform']    
    #regularCoes = [i/float(100) for i in xrange(1, 11)]
    regularCoes = [0.08]
    positiveTerms = ['relu']
    # 创建Excel
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # training model
    modelTerms = []
    for errorTerm in  errorTerms:
        for regularTerm in regularTerms:
            for positiveTerm in positiveTerms:
                for regularCoe in regularCoes:    
                    for num in range(len(p)):                    
                        plsq = leastsq(residuals_func, p[num], args=(y[num], x, errorTerm, regularTerm, regularCoe, positiveTerm))
                        p[num] = plsq[0]
                        s = sum(p[num])
                        for c in xrange(len(p[num])):
                            p[num][c] = p[num][c]/s
                    # 初始化 误差(RSS), 稳定性(stability), 稀疏性(sparsity), 正定性(nonNegativity)
                    RSS, stability, sparsity, nonNegativity = [], [], [], []
                    # 计算 stability
                    for r in range(0, len(p)-5, 5):
                        sta = []
                        for num in range(5):
                            s = ''
                            for c in p[r+num, -2:]:
                                if c > 0.1:
                                    s += '1'
                                else:
                                    s += '0'
                            sta.append(s)
                        stability.append(len(set(sta)))
                    # 计算 RSS, sparsity, nonNegativity
                    for r in range(len(p)):
                        sparsity.append(0)
                        nonNegativity.append(0)
                        ret = np.array(fit_func(p[r], x) - y[r])
                        ret = ret.tolist()
                        ret = ret[0]
                        rs = []
                        for i in ret:
                            rs.append(i**2)
                        RSS.append(sum(rs)/len(rs))
                        for c in range(len(p[r])):
                            if p[r][c] < 0:
                                nonNegativity[r] += abs(p[r][c])
                            elif p[r][c] > 0.1:
                                sparsity[r] += 1
                    # 保存结果
                    worksheet = workbook.add_sheet(errorTerm+' '+regularTerm+' '+positiveTerm+' '+str(regularCoe))
                    for i in range(len(p)):
                        for j in range(len(p[i])):
                            worksheet.write(i, j, label = p[i][j])
                    modelTerms.append([errorTerm, regularTerm, regularCoe, positiveTerm, sum(RSS)/len(RSS), sum(stability)/len(stability), sum(sparsity)/len(sparsity), sum(nonNegativity)/len(nonNegativity)])
                print [errorTerm, regularTerm, positiveTerm]
    # 将结果导出到Excel
    worksheet = workbook.add_sheet('modelTerms')
    title = ['误差项', '正则项', 'λ', '正定项', '误差(RSS)', '稳定性(stability)', '稀疏性(sparsity)', '正定性(nonNegativity)']
    for i in range(len(title)):
        worksheet.write(0, i, label = title[i])
    for i in range(len(modelTerms)):
        for j in range(len(modelTerms[i])):
            worksheet.write(i+1, j, label = modelTerms[i][j])
    workbook.save('modelTerms.xls')
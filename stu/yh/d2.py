import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import operator


# 数据预处理
def fileRead(fileName):
    # 打开文件
    fr = open(fileName)
    # 读取全部内容
    arraryOfLines = fr.readlines()
    # 求行数
    numberOfLines = len(arraryOfLines)
    # 生成numberOfLines行,3列的矩阵，方便后面存放数据
    returnMat = np.zeros((numberOfLines, 3))
    # 用于存放类别
    classLabelVector = []
    # 设置索引,用于循环
    index = 0
    # 开始循环读取
    for line in arraryOfLines:
        # 去除掉文件中的多余字符
        line = line.strip()
        # 用空格对内容进行分割
        listFormLine = line.split('\t')
        # 赋值
        returnMat[index, :] = listFormLine[0:3]
        # 对类别数组进行赋值
        if listFormLine[-1] == 'didntLike':
            classLabelVector.append(1)
        if listFormLine[-1] == 'smallDoses':
            classLabelVector.append(2)
        if listFormLine[-1] == 'largeDoses':
            classLabelVector.append(3)
        index += 1
    return returnMat, classLabelVector


# 数据展示
def showData(datingDataMat, datingLabels):
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False, figsize=(13, 8))

    LabelsColors = []
    for i in datingLabels:
        if i == 1:
            LabelsColors.append('black')
        if i == 2:
            LabelsColors.append('orange')
        if i == 3:
            LabelsColors.append('red')
    axs[0][0].scatter(x=datingDataMat[:, 0], y=datingDataMat[:, 1], color=LabelsColors, s=15, alpha=.5)
    axs0_title_text = axs[0][0].set_title('flight_play')
    axs0_xlabel_text = axs[0][0].set_xlabel('flight_time')
    axs0_ylabel_text = axs[0][0].set_ylabel('play_time')
    plt.setp(axs0_title_text, size=9, weight='bold', color='red')
    plt.setp(axs0_xlabel_text, size=7, weight='bold', color='black')
    plt.setp(axs0_ylabel_text, size=7, weight='bold', color='black')
    axs[0][1].scatter(x=datingDataMat[:, 0], y=datingDataMat[:, 2], color=LabelsColors, s=15, alpha=.5)
    # 设置标题,x轴label,y轴label

    axs1_title_text = axs[0][1].set_title('flight_eat')
    axs1_xlabel_text = axs[0][1].set_xlabel('flight')
    axs1_ylabel_text = axs[0][1].set_ylabel('eat')
    plt.setp(axs1_title_text, size=9, weight='bold', color='red')
    plt.setp(axs1_xlabel_text, size=7, weight='bold', color='black')
    plt.setp(axs1_ylabel_text, size=7, weight='bold', color='black')

    # 画出散点图,以datingDataMat矩阵的第二(玩游戏)、第三列(冰激凌)数据画散点数据,散点大小为15,透明度为0.5
    axs[1][0].scatter(x=datingDataMat[:, 1], y=datingDataMat[:, 2], color=LabelsColors, s=15, alpha=.5)
    # 设置标题,x轴label,y轴label
    axs2_title_text = axs[1][0].set_title('play_eat')
    axs2_xlabel_text = axs[1][0].set_xlabel('play_time')
    axs2_ylabel_text = axs[1][0].set_ylabel('eat_weight')
    plt.setp(axs2_title_text, size=9, weight='bold', color='red')
    plt.setp(axs2_xlabel_text, size=7, weight='bold', color='black')
    plt.setp(axs2_ylabel_text, size=7, weight='bold', color='black')
    # 设置图例
    didntLike = mlines.Line2D([], [], color='black', marker='.',
                              markersize=6, label='didntLike')
    smallDoses = mlines.Line2D([], [], color='orange', marker='.',
                               markersize=6, label='smallDoses')
    largeDoses = mlines.Line2D([], [], color='red', marker='.',
                               markersize=6, label='largeDoses')
    # 添加图例
    axs[0][0].legend(handles=[didntLike, smallDoses, largeDoses])
    axs[0][1].legend(handles=[didntLike, smallDoses, largeDoses])
    axs[1][0].legend(handles=[didntLike, smallDoses, largeDoses])
    # 显示图片
    plt.show()


# 数据归一化
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)

    ranges = maxVals - minVals
    normalDataSet = np.zeros(np.shape(dataSet))

    m = dataSet.shape[0]
    normalDataSet = dataSet - np.tile(minVals, (m, 1))
    normalDataSet = normalDataSet / np.tile(ranges, (m, 1))
    return normalDataSet, ranges, minVals

#分类器
def classify(input, dataSet, labels, k):
    # numpy中的shape方法用于计算形状 eg: dataSet: 4*2
    # print(dataSet.shape)
    dataSetSize = dataSet.shape[0]
    # numpy中的tile方法,用于对矩阵进行填充
    # 将inX矩阵填充至与dataSet矩阵相同规模,后相减
    diffMat = np.tile(input, (dataSetSize, 1)) - dataSet
    # 平方
    sqDiffMat = diffMat ** 2
    # 求和
    sqDistance = sqDiffMat.sum(axis=1)
    # 开方
    distance = sqDistance ** 0.5
    # argsort()方法进行直接排序
    sortDist = distance.argsort()
    classCount = {}
    for i in range(k):
        # 取出前k个元素的类别
        voteIlabel = labels[sortDist[i]]
        # dict.get(key,default=None),字典的get()方法,返回指定键的值,如果值不在字典中返回默认值。
        # 计算类别次数
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 排序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    # 返回次数最多的类别,即所要分类的类别
    return sortedClassCount[0][0]

fileName = 'datingTestSet.txt'
datingDataMat, datingLabels = fileRead(fileName)
showData(datingDataMat, datingLabels)
percent = 0.10
normalDataMat, ranges, minvals = autoNorm(dataSet=datingDataMat)
m = normalDataMat.shape[0]
numTestVecs = int(m*percent)
errorCount = 0.0
for i in range(numTestVecs):
    classifyResult = classify(normalDataMat[i,:],normalDataMat[numTestVecs:m,:],
                              datingLabels[numTestVecs:m],4)
    print("分类结果：%d,真实类别：%d" % (classifyResult,datingLabels[i]))
    if(classifyResult!=datingLabels[i]):
        errorCount += 1.0
print("错误率：%f%%" %(errorCount/float(numTestVecs)*100))

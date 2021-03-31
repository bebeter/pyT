#基于这个分布，我们来使用Kmeans进行聚类
from sklearn.cluster import KMeans


from sklearn.datasets import make_blobs #make_blobs是帮我做几个簇的意思
import matplotlib.pyplot as plt
#自己创建数据集
X, y = make_blobs(n_samples=500,n_features=2,centers=4,random_state=1) #500个数据 2个特征，4个簇，随机性规定，让数据稳定
X.shape
#(500, 2)
y.shape
#(500,)


fig, ax1 = plt.subplots(1) #生成子图1个：子图由两部分组成，画布fig 对象ax1
ax1.scatter(X[:, 0], X[:, 1] #将二维数据两列全部画进去
                ,marker='o' #点的形状
                ,s=8 #点的大小
                )
plt.show()



n_clusters = 3 #假设分为了3簇
#KMeans目的就是求出质心，已经把簇分好了，不需要接口
cluster = KMeans(n_clusters=n_clusters, random_state=0).fit(X) #实例化，训练，random_state也是为了模型稳定


# 重要属性labels_,查看聚好的类别，每个样本所对应的类，即标签
y_pred = cluster.labels_
y_pred


#但其实KMeans也有接口predict和fit_predict，表示学习数据X并对X的类进行预测
#但所得的结果和直接fit之后调用属性lables_一模一样
pre = cluster.fit_predict(X)
pre == y_pred


#但是数据量大的时候，可以先使用部分数据来确定质心
#在用法剩下的数据聚类结果，使用predict来调用，这样计算量会少很多
cluster_smallsub = KMeans(n_clusters=n_clusters, random_state=0).fit(X[:200]) #X[:200]切片取200行进行质心计算
y_pred_ = cluster_smallsub.predict(X) #再用整体数据做predict
y_pred == y_pred_ #这说明整体数据不完全相似，但是在数据量很大的时候，效果还是比较好的


#如果我们想要看见这个点的分布，怎么办？
color = ["red","pink","orange","gray"]
fig, ax1 = plt.subplots(1)
for i in range(4):
    ax1.scatter(X[y==i, 0], X[y==i, 1] #就是取出y_pred是0，1，2，3的那一簇的X
                ,marker='o' #点的形状
                ,s=8 #点的大小
                ,c=color[i]
                )
plt.show()



#基于这个分布，我们来使用Kmeans进行聚类
from sklearn.cluster import KMeans
n_clusters = 3 #假设分为了3簇
#KMeans目的就是求出质心，已经把簇分好了，不需要接口
cluster = KMeans(n_clusters=n_clusters, random_state=0).fit(X) #实例化，训练，random_state也是为了模型稳定


# 重要属性labels_,查看聚好的类别，每个样本所对应的类，即标签
y_pred = cluster.labels_
y_pred


#但其实KMeans也有接口predict和fit_predict，表示学习数据X并对X的类进行预测
#但所得的结果和直接fit之后调用属性lables_一模一样
pre = cluster.fit_predict(X)
pre == y_pred


#但是数据量大的时候，可以先使用部分数据来确定质心
#在用法剩下的数据聚类结果，使用predict来调用，这样计算量会少很多
cluster_smallsub = KMeans(n_clusters=n_clusters, random_state=0).fit(X[:200]) #X[:200]切片取200行进行质心计算
y_pred_ = cluster_smallsub.predict(X) #再用整体数据做predict
y_pred == y_pred_ #这说明整体数据不完全相似，但是在数据量很大的时候，效果还是比较好的


#重要属性cluster_centers_，查看质心
centroid = cluster.cluster_centers_
print(centroid)
centroid.shape

#重要属性inertia_，查看总距离平方和，越小，模型效果越好。
inertia = cluster.inertia_
inertia


color = ["red","pink","orange","gray"]
fig, ax1 = plt.subplots(1)
for i in range(n_clusters):
    ax1.scatter(X[y_pred==i, 0], X[y_pred==i, 1] #就是取出y_pred是0，1，2的那一类的X
                ,marker='o' #点的形状
                ,s=8 #点的大小
                ,c=color[i]
                )
#对不同颜色的簇找出质心
ax1.scatter(centroid[:,0],centroid[:,1]
            ,marker="x"
            ,s=20
            ,c="black")
plt.show()


#如果聚类效果更好的话，inertia应该更低
#随着n_cluster越来越大，inertia可以等于0；所以模型的效果调整只有在K不变的时候，调整才对。
#可见，inertia不是一个有效的评估指标
n_clusters = 4
cluster_ = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
inertia_ = cluster_.inertia_
inertia_


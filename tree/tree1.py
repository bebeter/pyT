#1.导入包
#代表画图的时候，需要这个环境
#%matplotlib inline
from sklearn.tree import DecisionTreeClassifier #决策树
from sklearn.ensemble import RandomForestClassifier #集成学习中的随机森林
from sklearn.datasets import load_wine#wine数据集

#2 导入数据集
wine = load_wine()
print(len(wine.data))
print(wine.target)


from sklearn.model_selection import train_test_split
Xtrain,Xtest,Ytrain,Ytest = train_test_split(wine.data,wine.target,test_size=0.3)

#复习:sklearn建模的基本流程
clf = DecisionTreeClassifier(random_state=0)
rfc = RandomForestClassifier(random_state=0)

clf = clf.fit(Xtrain,Ytrain)
rfc = rfc.fit(Xtrain,Ytrain)

score_c = clf.score(Xtest,Ytest) #是精确度
score_r = rfc.score(Xtest,Ytest)

print('Single Tree:{}'.format(score_c)
     ,'Random Forest:{}'.format(score_r)) #format是将分数转换放在{}中



#4. 画出随机森林和决策树在一组交叉验证下的效果对比
#交叉验证：是数据集划分为n分，依次取每一份做测试集，每n-1份做训练集，多次训练模型以观测模型稳定性的方法



from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
''' 
rfc = RandomForestClassifier(n_estimators=25)
rfc_s = cross_val_score(rfc,wine.data,wine.target,cv=10)
clf = DecisionTreeClassifier()
clf_s = cross_val_score(clf,wine.data,wine.target,cv=10)

plt.plot(range(1,11),rfc_s,label = "RandomForest")
plt.plot(range(1,11),clf_s,label = "Decision Tree")
plt.legend()
plt.show()
'''

#上述交叉验证更为简单的实现方式
# for循环两种交叉验证，先计算RandomForest，再计算DecisionTree
label = "RandomForest"
for model in [RandomForestClassifier(n_estimators=25),DecisionTreeClassifier()]:
    score = cross_val_score(model,wine.data,wine.target,cv=10)
    print("{}:".format(label)),print(score.mean()) #这边打印的是计算10次得到的acuraccy的平均值
    plt.plot(range(1,11),score,label = label)
    plt.legend()
    label = "DecisionTree"


#6. n_estimators的学习曲线
superpa = []
for i in range(200):
    rfc = RandomForestClassifier(n_estimators=i+1,n_jobs=-1) #这里就是进行了200次的随机森林计算，每次的n_estimator设置不一样
    rfc_s = cross_val_score(rfc,wine.data,wine.target,cv=10).mean()
    superpa.append(rfc_s)
print(max(superpa),superpa.index(max(superpa)))
plt.figure(figsize=[20,5])
plt.plot(range(1,201),superpa)
plt.show()
# list.index(object) >>>返回对象object在列表list中的索引 68是i值，但是n_estimators=i+1，所以最大准确率对应的n_estimators是69.



rfc = RandomForestClassifier(n_estimators=25,random_state=2)
rfc = rfc.fit(Xtrain,Ytrain)
# #随机森林的重要属性之一：estimators，查看森林中树的状况
rfc.estimators_[0].random_state #就是查看第0棵树的randomstate是多少
#1872583848

#通过循环将随机森林中所有决策树的random_state导出
for i in range(len(rfc.estimators_)):
    print(rfc.estimators_[i].random_state)

    # 无需划分训练集和测试集，用袋外数据来测试模型
    rfc = RandomForestClassifier(n_estimators=25, oob_score=True)  # oob_score默认是FALSE,bootstrap默认是TRUE.
    rfc = rfc.fit(wine.data, wine.target)  # 用所有的数据来训练
    # 重要属性oob_score_
    rfc.oob_score_  # 查看袋外数据在模型上的测试结果
    # 0.9606741573033708


rfc = RandomForestClassifier(n_estimators=25)
rfc = rfc.fit(Xtrain, Ytrain) #fit接口是训练集用的
rfc.score(Xtest,Ytest)
rfc.feature_importances_ #得出所有特征的重要性数值
rfc.apply(Xtest) #返回测试集每个样本在所在树的叶子节点的索引
rfc.predict(Xtest) #返回对测试集的预测标签
rfc.predict_proba(Xtest) #每一个样本分配到每一个标签的概率
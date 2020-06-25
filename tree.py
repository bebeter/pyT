from sklearn import tree

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import sklearn.tree.export
import numpy as np

iris = load_iris()
decision_tree = DecisionTreeClassifier(random_state=0, max_depth=2)
decision_tree = decision_tree.fit(iris.data, iris.target)
r = sklearn.tree.export_text(decision_tree, feature_names=iris['feature_names'])
print(r)



from sklearn.datasets import load_iris
from sklearn import tree
X, y = load_iris(return_X_y=True)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)
print(clf)
tree.plot_tree(clf.fit(iris.data, iris.target))






dot_data = tree.export_graphviz(clf, out_file=None, feature_names=iris.feature_names,class_names=iris.target_names,  filled=True,rounded=True,  special_characters=True)
#graph = graphviz.Source(dot_data)
print(dot_data)



mask = np.random.rand(len(10)) < 5
print(mask)

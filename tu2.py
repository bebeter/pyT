import numpy as np
import matplotlib.pyplot as plt

N = 13
S = (52, 49, 48, 47, 44, 43, 41, 41, 40, 38, 36, 31, 29)
C = (38, 40, 45, 42, 48, 51, 53, 54, 57, 59, 57, 64, 62)

d = []
for i in range(0, len(S)):
    sum = S[i] + C[i]
    d.append(sum)
M = (10, 11, 7, 11, 8, 6, 6, 5, 3, 3, 7, 5, 9)
# menStd = (2, 3, 4, 1, 2)
# womenStd = (3, 5, 2, 3, 3)
ind = np.arange(N)  # the x locations for the groups
width = 0.35  # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, S, width, color='#d62728')  # , yerr=menStd)
p2 = plt.bar(ind, C, width, bottom=S)  # , yerr=womenStd)
p3 = plt.bar(ind, M, width, bottom=d)

plt.ylabel('Scores')
plt.title('Scores by group and gender')
plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13'))
plt.yticks(np.arange(0, 81, 20))
plt.legend((p1[0], p2[0], p3[0]), ('S', 'C', 'M'))

plt.show()
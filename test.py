import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# font = FontProperties(fname="simsun.ttc", size=14)

name_list = ['周一','周二','周三','Sunday']
num_list = [1.5,0.6,7.8,6]

# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.bar(range(len(num_list)), num_list,color='rgb',tick_label=name_list)
plt.show()

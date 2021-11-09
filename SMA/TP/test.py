import scipy.stats
import numpy as np


x_min = 0.0
x_max = 24.0

mean = 14.0 
std = 3.0

x = np.linspace(x_min, x_max,48)

y = scipy.stats.norm.pdf(x,mean,std)
y = y*750

print(y.astype(int))
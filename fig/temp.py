# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:25:27 2013

@author: Yuxiang Wang
"""

import numpy as np
import matplotlib.pyplot as plt


fig, axs = plt.subplots(3, 3)
fig.subplots_adjust(top=.3)

import numpy as np
import matplotlib.pyplot as plt

f = np.random.random(100)
g = np.random.random(100)
fig = plt.figure()
fig.suptitle('Long Suptitle', fontsize=24)
plt.subplot(121)
plt.plot(f)
plt.title('Very Long Title 1', fontsize=20)
plt.subplot(122)
plt.plot(g)
plt.title('Very Long Title 2', fontsize=20)
plt.subplots_adjust(top=0.85)
plt.show()
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 16:30:28 2015

@author: Administrator
"""

import os
import cPickle
from scipy.io import savemat

for fname in os.listdir('../pickles'):
    if fname.endswith('r1750_stip.pkl'):
        with open('../pickles/%s' % fname, 'r') as f:
            data = cPickle.load(f)
#        savemat(fname.replace('pkl', 'mat'), data, do_compression=True)
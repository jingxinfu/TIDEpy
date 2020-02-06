#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################################
# Created Date : Wednesday February 5th 2020                                   #
# Author: Jingxin Fu (jingxinfu.tj@gmail.com)                                  #
# ----------                                                                   #
# Last Modified: Wednesday February 5th 2020 6:19:01 pm                        #
# Modified By: Jingxin Fu (jingxinfu.tj@gmail.com)                             #
# ----------                                                                   #
# Copyright (c) Jingxin Fu 2020                                                #
# Licence : MIT https://opensource.org/licenses/MIT                            #
################################################################################

__doc__="""
"""

import pandas as pd
import numpy as np
from tidepy import utils
from tidepy import model
from tidepy import MODEL_DB_PATH
MODEL_DB = pd.read_pickle(MODEL_DB_PATH)
def TIDE(expression, cancer, pretreat=False, vthres=0):
    # translate the number of expression
    expression = utils.toEntrez(expression)
    is_normalized = utils.is_normalized(exprsn=expression)
    if not is_normalized:
        print("[WARN] Start normalizing the input expression profile by: 1. Do the log2(x+1) transformation. 2. Subtract the average across your samples.")
        expression = np.log2(expression + 1)
        expression = expression.apply(lambda v: v-v.mean(),axis=1)
	### Combine all biomarkers together
	# TIDE
    result = model.tide_pred(exprsn=expression,cancer=cancer,tide_model=MODEL_DB['tide'],pretreat=pretreat,vthres=vthres)
    for k,v in MODEL_DB['biomarkers'].items():
        try:
            result[k] = model.sigGene_pred(expression,v)
        except KeyError as e:
            warnings.warn(e)
            result[v] = np.nan
    # MSI prediction
    result['MSI Score']= model.msi_pred(expression, msi_model=MODEL_DB['msi'])
    # No benefits
    result['No benefits'] = (result.TIDE > 1) & (result.IFNG < -1)

    result = result[['No benefits', 'Responder', 'TIDE', 'IFNG',  'MSI Score','CD274','CD8','CTL.flag', 'Dysfunction',
        'Exclusion', 'MDSC', 'CAF', 'TAM M2']].sort_values('TIDE', ascending=False)
    return result

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################################
# Created Date : Wednesday February 5th 2020                                   #
# Author: Jingxin Fu (jingxinfu.tj@gmail.com)                                  #
# ----------                                                                   #
# Last Modified: Wednesday February 5th 2020 6:07:38 pm                        #
# Modified By: Jingxin Fu (jingxinfu.tj@gmail.com)                             #
# ----------                                                                   #
# Copyright (c) Jingxin Fu 2020                                                #
# Licence : MIT https://opensource.org/licenses/MIT                            #
################################################################################


import pandas as pd
from tidepy import GENE_REF_PATH
GENE_REF = pd.read_pickle(GENE_REF_PATH)

def toEntrez(expression,gene_ref=GENE_REF):
    ''' Convert expression matrix with Ensemble ID or Gene symbol as index to expression matrix with Entrez ID

    Parameters
    ----------
    expression : pandas.DataFrame
        Expression matrix with gene identifier as index
    Returns
    -------
    None / pandas.DataFrame
        Expression matrix with Entrez ID as index
    None / str
        Error information
    '''

    # translate the number of expression
    cnt_nonint = sum(
        map(lambda v: not isinstance(v, (int, float)), expression.index))
    num_genes = float(expression.shape[0])
    if cnt_nonint > 0:

        ind_g = gene_ref['Symbol'][expression.index.map(lambda x:x.upper())]
        ind_e = gene_ref['ENSG'][expression.index.map(lambda x:x.upper())]

        map_count = len(ind_g.dropna()) - len(ind_e.dropna())
        expression.index = ind_g if map_count > 0 else ind_e
        flag = ~ pd.isnull(expression.index)

        # too few genes
        if sum(flag) < num_genes/2 or sum(flag) < 10:
           raise ValueError('Only ' + str(sum(flag)) + ' out of ' + str(expression.shape[0]) + \
               ' gene names are found. We only support: Ensembl ID, EntrezID (Without Version Digit), and Hugo symbol')
        elif sum(flag) < num_genes:
            miss_ratio = 1 - sum(flag)/num_genes
            print("[WARN] %.2f %% Genes are missing after converting to Entrez ID" % (miss_ratio*100) )
            expression = expression.loc[flag]

    expression = expression.groupby(level=0).mean()
    expression.index = expression.index.astype('int64')

    return expression

def is_normalized(exprsn):
    """ Check whether the expression profile has been normalized or not

    Parameters
    ----------
    exprsn : pd.DataFrame
        Gene expression profile, index by gene id and columns by sample id

    Returns
    -------
    Boolean
        Information about whether the expression profile has been normalized
    """
    posNegRatio = (exprsn > 0).unstack().value_counts() / \
        float(exprsn.shape[0]*exprsn.shape[1])
    sign = posNegRatio.max()

    if sign > 0.8:
        print('[WARN] The majority(>80%) of genes with {} expression in your inputted data. Please Normalize your data'.format({
            True: 'positive', False: 'negative'}[posNegRatio.idxmax()]))
        return False
    else:
        return True

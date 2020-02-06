#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################################
# Created Date : Wednesday February 5th 2020                                   #
# Author: Jingxin Fu (jingxinfu.tj@gmail.com)                                  #
# ----------                                                                   #
# Last Modified: Wednesday February 5th 2020 5:55:13 pm                        #
# Modified By: Jingxin Fu (jingxinfu.tj@gmail.com)                             #
# ----------                                                                   #
# Copyright (c) Jingxin Fu 2020                                                #
# Licence : MIT https://opensource.org/licenses/MIT                            #
################################################################################

__doc__="""
Prediction Module
"""
import numpy as np
import pandas as pd

CANCER_CHOICE = ['Melanoma','NSCLC','Other']
def msi_pred(exprsn,msi_model):
    """ Logistic model to estimate the MSI status

    Parameters
    ----------
    exprsn : pd.DataFrame
        Gene expression profile, index by gene id and columns by sample id
    msi_model : pd.DataFrame, optional
        MSI model, index by gene id with its coefficients
     Returns
    -------
    pd.Series
        MSI score for every samples
    """
    ol_gene = exprsn.index.intersection(msi_model.index)
    miss_gene = 1 - (float(len(ol_gene)) / msi_model.shape[0])
    if miss_gene == 1:
        raise ValueError('No MSI signature genes in the exprsn')
    elif miss_gene > 0.1:
        print('[WARN] %.1f%% MSI signature genes are missing on input expression profile.' % (miss_gene*100) )

    msi_score = np.exp(exprsn.T[ol_gene].dot(msi_model.loc[ol_gene]))
    msi_score = msi_score.apply(lambda v: v/msi_score.sum(axis=1), axis=0)
    # in case there is duplicated samples
    msi_score = msi_score.groupby(level=0).mean()
    return msi_score['MSI']


def tide_pred(exprsn, cancer,tide_model,pretreat=False,vthres=0):
    set_CTL = [925, 926, 3001, 3002, 5551]
    signature_sd = tide_model['SD']
    dysfunction_model = tide_model['Dysfunction']
    exclusion_model = tide_model['Exclusion']
    if cancer not in CANCER_CHOICE:
        raise ValueError("Please Choose Cancer types from this options: %s" ','.join(CANCER_CHOICE))
    # Only consider studied cancer types
    if cancer == 'Melanoma':
        signature_sd = signature_sd.loc['SKCM.RNASeq']
    elif cancer == 'NSCLC':
        signature_sd = (signature_sd.loc['LUSC.RNASeq.norm_subtract'] +
                        signature_sd.loc['LUAD.RNASeq.norm_subtract'])/2
    else:
        # use the melanoma rule for approximation
        signature_sd = signature_sd.loc['SKCM.RNASeq']

    CTL_flag = exprsn.loc[set_CTL].min() > 0
    CTL_flag.name = 'CTL.flag'
    correlation = dysfunction_model.apply(lambda v: exprsn.corrwith(v))
    correlation = correlation.divide(signature_sd)
    correlation['TIDE'] = correlation['Exclusion']

    # only TIDE model for no previous ICB treatment
    if not pretreat:
        correlation.loc[CTL_flag, 'TIDE'] = correlation.loc[CTL_flag, 'Dysfunction']

    response = correlation['TIDE'] < vthres
    response.name = 'Responder'

    # add in T-cell exclusion signatures
    correlation_exclusion = exclusion_model.apply(
        lambda v: exprsn.corrwith(v))
    result = pd.concat(
        [correlation, CTL_flag, response, correlation_exclusion], axis=1)

    return result


def sigGene_pred(exprsn,gene_list):
    """ Signature score calculation based on weighted average

    Parameters
    ----------
    exprsn : pd.DataFrame
        Gene expression profile, index by gene id and columns by sample id
    gene_list : pd.DataFram
        index by gene id with its weight
     Returns
    -------
    pd.Series
        signature score for every samples
    Raise
    -------
    KeyError
        None of genes in the expression profile
    """
    ol_gene = exprsn.index.intersection(gene_list.index)
    if len(ol_gene) < 0:
        raise KeyError('All of %s signatures is missing on your data.' % gene_list.name)
    elif len(ol_gene) != len(gene_list):
        print('[WARN] Missing Gene:'+','.join([str(x) for x in gene_list.index if not x in ol_gene]) + 'for signature %s' % gene_list.name)
    result = gene_list[ol_gene].dot(exprsn.loc[ol_gene, :])

    return result

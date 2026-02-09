#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################################
# Created Date : Wednesday February 5th 2020                                   #
# Author: Jingxin Fu (jingxinfu.tj@gmail.com)                                  #
# ----------                                                                   #
# Last Modified: Monday February 9th 2026 9:34:34 am                           #
# Modified By: Jingxin Fu (jingxin@broadinstitute.org)                         #
# ----------                                                                   #
# Copyright (c) Jingxin Fu 2020                                                #
# Licence : MIT https://opensource.org/licenses/MIT                            #
################################################################################


import io
from importlib import resources
import pandas as pd


def read_data_object(filename: str):
    """Load a bundled pickled object from the TIDEpy package.
    
    This function reads ``tidepy/data/<filename>`` using the standard library
    ``importlib.resources`` API and deserializes it with ``pandas.read_pickle``.
    It is a replacement for the legacy ``pkg_resources.resource_filename`` +
    ``pd.read_pickle(path)`` approach, which no longer works with modern
    setuptools versions (``pkg_resources`` was removed in setuptools>=82).

    Parameters
    ----------
    filename
        Name of the file inside the ``tidepy/data`` package directory
        (e.g. ``"model.pkl"`` or ``"Gene_Ref.pkl"``).

    Returns
    -------
    Any
        The deserialized Python object stored in the pickle.
    """
    data = resources.files("tidepy").joinpath("data", filename).read_bytes()
    return pd.read_pickle(io.BytesIO(data))

def toEntrez(expression,gene_ref=None):
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

    if gene_ref is None:
        gene_ref = read_data_object("Gene_Ref.pkl")
    # translate the number of expression
    cnt_nonint = sum(
        map(lambda v: not isinstance(v, (int, float)), expression.index))
    num_genes = float(expression.shape[0])
    if cnt_nonint > 0:

        ind_g = gene_ref['Symbol'].reindex(expression.index.map(lambda x:x.upper()))
        ind_e = gene_ref['ENSG'].reindex(expression.index.map(lambda x:x.upper()))

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

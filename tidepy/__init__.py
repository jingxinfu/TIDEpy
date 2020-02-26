#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author            : Jingxin Fu <jingxinfu.tj@gmail.com>
# Date              : 26/02/2020
# Last Modified Date: 26/02/2020
# Last Modified By  : Jingxin Fu <jingxinfu.tj@gmail.com>
import os
import pkg_resources
__version__="1.3.2"
DATA_DIR = pkg_resources.resource_filename('tidepy', 'data/')
MODEL_DB_PATH = os.path.join(DATA_DIR,'model.pkl')
GENE_REF_PATH = os.path.join(DATA_DIR,'Gene_Ref.pkl')

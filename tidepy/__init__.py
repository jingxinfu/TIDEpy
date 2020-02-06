import os
import pandas as pd
import pkg_resources
__version__="1.0"
DATA_DIR = pkg_resources.resource_filename('tidepy', 'data/')
MODEL_DB = pd.read_pickle(os.path.join(DATA_DIR,'model.pkl'))
GENE_REF = pd.read_pickle(os.path.join(DATA_DIR,'Gene_Ref.pkl'))

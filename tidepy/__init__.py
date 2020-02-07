import os
import pkg_resources
__version__="1.3.1"
DATA_DIR = pkg_resources.resource_filename('tidepy', 'data/')
MODEL_DB_PATH = os.path.join(DATA_DIR,'model.pkl')
GENE_REF_PATH = os.path.join(DATA_DIR,'Gene_Ref.pkl')

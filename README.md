
# TIDE command-line interface and python module

[![PyPI version](https://badge.fury.io/py/tidepy.svg)](https://badge.fury.io/py/tidepy) ![PyPI - Format](https://img.shields.io/pypi/format/tidepy?style=flat-square) [![License: GPL v2](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://www.gnu.org/licenses/old-licenses/gpl-3.0.en.html) [![Build Status](https://travis-ci.org/jingxinfu/TIDEpy.svg?branch=master)](https://travis-ci.org/jingxinfu/TIDEpy) [![PyPI - Downloads](https://img.shields.io/pypi/dm/tidepy?color=green&label=pypi%20download&logoColor=green&style=flat-square)](https://pypi.org/project/tidepy/)

**TIDE** (**T**umor **I**mmune **D**ysfunction and **E**xclusion)  is a computational framework developed to evaluate the potential of tumor immune escape from the gene expression profiles of cancer samples. This package provides a python implemented CLI, and python module with Pandas inputs and outputs. If you prefer to run TIDE online, please use `Response Prediction` module on our website : http://tide.dfci.harvard.edu/. 


## System requirements
- Linux/Unix
- Python (>=3.4)

## Installation
- Clone from github
```sehll
$ git clone git@github.com:jingxinfu/TIDEpy.git
$ cd TIDEpy
$ pip install .
```
- From the [pypi](https://pypi.org/project/tidepy/), a python package management tool
```
$ pip install tidepy
```



## What is the input data format?

The input data should be a square matrix of gene expression profiles for all patients. Each column represents the patient ID, and each row represents a gene name which can be either symbol name (e.g., TGFB1) or Entrez ID (e.g., 7040). Please see some samples from [anti-PD1](http://tide.dfci.harvard.edu/download/GSE78220.self_subtract.gz) or [anti-CTLA4](http://tide.dfci.harvard.edu/download/VanAllen.self_subtract.gz) therapies in melanoma. 

#### In detail:

**Expression File**

1. If it's possible, please input a normalized expression file follows the instruction:

   - The gene expression value should be normalized toward a control sample which could be either normal tissues related with a cancer type or mixture sample from diverse tumor samples. The log2(RPKM+1) values from a RNA-seq experiment may not be meaningful unless a good reference control is available to adjust the batch effect and cancer type difference. In our study, we used the all sample average in each study as the normalization control.
     
   - Otherwise, We'll do the normalization for you by:
         
        1. Do the log2(x+1) transformation
        2. Subtract the average across your samples.

2. If it's possible, please convert your gene identifier into Entrez ID based on your annotation GTF files. 
      Otherwise, we will use our annotation GTF to do the conversion, which is gencode v27.

**Cancer Type:**

 We validated TIDE performance on predicting anti-PD1 and anti-CTLA4 response across several melanoma datasets and a limited dataset  of non-small cell lung cancer (NSCLC). TIDE may not work on cancer types other than melanoma and NSCLC (e.g., glioblastoma, or renal cell carcinoma) and therapies other than anti-PD1 and anti-CTLA4 (e.g., anti-PDL1, or Car T). 

## Usage

### Run TIDE through command line:

```
usage: tidepy [-h] -o OUTPUT -c {Melanoma,NSCLC,Other} [--pretreat]
            [--vthres VTHRES]
            expression

positional arguments:
  expression            Path to expression profile.
  											

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output Path (default: None)
  -c {Melanoma,NSCLC,Other}, --cancer {Melanoma,NSCLC,Other}
                        Cancer Type (default: None)
  --pretreat            A previous immunotherapy (e.g., progressed after anti-
                        CTLA4 before current anti-PD1) will change the
                        response prediction rule. Please put the flag with
                        previous line of immunotherapy. However, earlier
                        treatments of targeted therapies or chemotherapies
                        should not be considered here, and please do not put
                        the flag. (default: False)
  --vthres VTHRES       Threshold to distinguish responder fron non-responder
                        based on TIDE value. (default: 0.0)
```

#### Example

Please download the first example file under **Response Prediction** module on our website: http://tide.dfci.harvard.edu. The file name should be `GSE78220.self_subtract.zip`. To obtain the immune-related metrics for this study, you can run following code on your terminal:

```shell
$ tidepy GSE78220.self_subtract.zip -o GSE78220.txt -c Melanoma
```

The output file `GSE78220.txt` has those columns: No benefits, Responder, TIDE, IFNG, MSI Score, CD274, CD8, CTL.flag, Dysfunction, Exclusion, MDSC, CAF, TAM M2, which are exactly the same with the result outputted from our website. 

```
$ head GSE78220.txt

	No benefits	Responder	TIDE	IFNG	MSI Score	CD274	CD8	CTL.flag	Dysfunction	Exclusion	MDSC	CAF	TAM M2
Pt10	True	False	2.9031378266316437	-2.3496942540874994	0.25805402238944347	-1.45699548307	-2.2538329160500004	False	-1.1904018820543425	2.9031378266316437	0.22023489119026698	0.2086109089536346	0.021521981442711974
Pt32	True	False	2.374656680742425	-1.251790579471	0.03317166493632983	-1.34396174667	-1.092551002026	False	0.7565819504165977	2.374656680742425	0.11720339003535449	0.23364173308834454	0.021349394169070356
Pt38	False	False	2.3272172094686367	1.421773451414	0.369744309404354	1.44922588993	1.67154054016	True	2.3272172094686367	-3.0384590803306617	-0.16135256818744914	-0.25075626440976084	-0.054974225801339455
Pt12	True	False	1.5872758043454305	-2.0323342892546665	0.42890701750431737	-1.0318990510700001	-2.235849307205	False	-0.37355955596879964	1.5872758043454305	0.1187563077904593	0.14157760370392405	-0.005648658414646455
Pt14	False	False	1.4617100514481065	0.08189238923924995	0.29446508349637074	2.7750512868299997	-1.004022775004	False	0.2613253541514945	1.4617100514481065	0.1495425400268765	0.09892114074144391	-0.032482034306099805
Pt20	False	False	1.2040301004408855	2.682862982916667	0.8176690141355004	1.33916228496	3.756670182795	True	1.2040301004408855	-3.374284072367413-0.24958308053873887	-0.1817896254985925	-0.08581630042676716
Pt1	False	False	1.0412494657529983	0.7254327628349333	0.536995843539227	-0.156163548496	0.15697680025049998	False	-0.48094961955303106	1.0412494657529983	-0.046094357732277734	0.1997680886231509	0.009852881373563268
Pt9	False	False	0.8010709440747635	0.2580580358761666	0.7296845983437736	-0.582410268962	0.5549609285135	False	-0.11682795201511606	0.80107094407476350.05633802108085521	0.040839374451276424	0.020610152865016378
Pt7	False	False	0.6718349276249306	-0.7193369628115166	0.44483998965603927	-0.8181523873759999	-0.8982304490069999	False	-0.6222713974526163	0.6718349276249306	0.0767865719035387	-0.01954210031741603	0.048268448437660275
```

### Run TIDE inside python console:

Please download the first example file under **Response Prediction** module on our website: http://tide.dfci.harvard.edu. The file name should be `GSE78220.self_subtract.zip`. To obtain the immune-related metrics for this study, you can run following code inside python console:

```python
import pandas as pd
from tidepy.pred import TIDE
df = pd.read_csv("GSE78220.self_subtract.zip",sep='\t',index_col=0)
result = TIDE(df,cancer='Melanoma',pretreat=False,vthres=0.)
result.head(2)
"""
No benefits	Responder	TIDE	IFNG	MSI Score	CD274	CD8	CTL.flag	Dysfunction	Exclusion	MDSC	CAF	TAM M2
Pt10	True	False	2.9031378266316437	-2.3496942540874994	0.25805402238944347	-1.45699548307	-2.2538329160500004	False	-1.1904018820543425	2.9031378266316437	0.22023489119026698	0.2086109089536346	0.021521981442711974
Pt32	True	False	2.374656680742425	-1.251790579471	0.03317166493632983	-1.34396174667	-1.092551002026	False	0.7565819504165977	2.374656680742425	0.11720339003535449	0.23364173308834454	0.021349394169070356
"""
```

## Citation

-  Jingxin Fu, Karen Li, Wubing Zhang, Changxin Wan, Jing Zhang§, Peng Jiang§, Xiaole Shirley Liu§. ***"Large-scale public data reuse to model immunotherapy response and resistance."*** Genome Medicine. 2020 Dec;12(1):1-8.

- Peng Jiang\*, Shengqing Gu\*, Deng Pan\*, Jingxin Fu, Avinash Sahu, Xihao Hu, Ziyi Li, Nicole Traugh, Xia Bu, Bo Li, Jun Liu, Gordon J. Freeman, Myles A. Brown, Kai W. Wucherpfennig§, X. Shirley Liu§.***"Signatures of T cell dysfunction and exclusion predict cancer immunotherapy response."*** Nature medicine. 2018 Oct;24(10):1550-8. 



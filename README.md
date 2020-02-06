# TIDE (Tumor Immune Dysfunction and Exclusion)

##  Command-Line Usage

This is the script to calculate the TIDE score and immunesuppresive metrics for your gene expression profile. User needs to provide a gene expression file,  the cancer type, pre-treatment information.  

**Expression FIle:**

1. If it's possible, please input a normalized expression file follows the instruction:

   - The gene expression value should be normalized toward a control sample which could be either normal tissues related with a cancer type or mixture sample from diverse tumor samples. The log2(RPKM+1) values from a RNA-seq experiment may not be meaningful unless a good reference control is available to adjust the batch effect and cancer type difference. In our study, we used the all sample average in each study as the normalization control.
         
   - Otherwise, We'll do the normalization for you by:
         
        1. Do the log2(x+1) transformation
        2. Subtract the average across your samples.

2. If it's possible, please convert your gene identifier into Entrez ID based on your annotation GTF files. 
      Otherwise, we will use our annotation GTF to do the conversion, which is gencode v27.

**Cancer Type:**

 We validated TIDE performance on predicting anti-PD1 and anti-CTLA4 response across several melanoma datasets and a limited dataset  of non-small cell lung cancer (NSCLC). TIDE may not work on cancer types other than melanoma and NSCLC (e.g., glioblastoma, or renal cell carcinoma) and therapies other than anti-PD1 and anti-CTLA4 (e.g., anti-PDL1, or Car T). 

```
usage: TIDE [-h] -o OUTPUT -c {Melanoma,NSCLC,Other} [--pretreat]
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


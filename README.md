# A first-level heading
## A second-level heading
### A third-level heading
**This is bold text**
_This text is italicized_
**This text is _extremely_ important**
***All this text is important***
This is an <ins>underlined</ins> text

```
code text written like this
```




# BEQ CRISPResso pipeline
The BEQ (BaseEditingQuantifications) CRISPResso Pipeline is a library of functions designed to more efficently perfom CRISPResso functionality on numerous FASTQ files in quick succession. 

BEQ CRISPResso Pipeline recives an amplicon list from the user and runs through large amounts of fastq files directory by directory to eliminate the need for manual file manipulation from a user. 

Upon completion of CRISPRsso_Loop, CRISPResso output is placed in the directory beside coorisponding fastq file(s).

Upon completion of Read_based_quant, output files are written to a CSV file for the user containing:
- Directory the fastq file was from
- Read-based Lenient Correction Percentage (with tolerated bystanders)
- Read-based Strict Correction
- Independent Nucleotide Based Editing Quantification Percentage (taken from Quantification_window_nucleotide_percentage_table)
- Reads Aligned
- Reads Total
- Guide Sequence (reverse complement if guide is in reverse orientation from amplicon)
- Guide Sequence relative to amplicon
- Index of Intended Edit (+1 for position)
- Index of Permissible Bystanders (+1 for position)
- Strings used to search the Alleles_frequency_table in the CRISPResso output

<sub>BEQ CRISPResso Pipeline is distributed under the BSD license.</sub>
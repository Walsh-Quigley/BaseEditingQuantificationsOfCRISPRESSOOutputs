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

Requires CRISPResso to be installed on machine.

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


## Download ##

BEQ CRISPResso Pipeline can be downloaded from this repository for funciton use.

Additional information about function implementation can be found in the ```usage``` section

## Directory Format ##
Tree view of working directory before use should display as follows:

<pre><code>
userNamedDirectory/
├── firstDirectoryContainingFastQFiles
│   ├── firstFastqFile.fastq
│   └── optionalAdditionalFastqFile.fastq
├── secondDirectoryContainingFastQFiles
├── thirdDirectoryContainingFastQFiles
├── additionalDirectoryContainingFastQFiles
├── ampliconList.csv
├── CRISPResso_Loop.py
└── Read_based_quant.py
</code></pre>

Tree view of working directory after use will display as follows:

<pre><code>
userNamedDirectory/
├── firstDirectoryContainingFastQFiles
│   ├── firstFastqFile.fastq
│   ├── optionalAdditionalFastqFile.fastq
│   ├── AQLenientCorrection.CSV
│   ├── AQStrictCorrection.CSV
│   ├── CRISPREsso_on_firstFastqFile.html
│   └── CRISPREsso_on_firstFastqFile/
│       ├── 1a.Read_barplot.PDF
│       ├── 1a.Read_barplot.PNG
│       ├── 1b.Alignment_pi_chart.PDF
│       └── ...
├── secondDirectoryContainingFastQFiles
│   └── ...
├── thirdDirectoryContainingFastQFiles
│   └── ...
├── additionalDirectoryContainingFastQFiles
│   └── ...
├── unprocessed_data
│   └── ...
├── ampliconList.csv
├── AQ_Read_Based_Correction
├── CRISPResso_Loop.py
└── Read_based_quant.py
</code></pre>

## Usage ##

BEQ CRISPResso Pipline can be used by placing the CRISPResso_Loop.py file in your fastq data direcotry and then entering 
``` python CRISPResso_loop.py ```
while in that directory 
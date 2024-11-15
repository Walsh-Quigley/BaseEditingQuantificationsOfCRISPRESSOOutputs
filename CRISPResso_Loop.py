#location of .py file: /Users/aidanq/Desktop/Bash_Scripts/BaseEditingQuantificationsOfCRISPRESSOOutputs/CRISPResso_Loop.py


import os
import subprocess
import glob



# the function to retrieve the GuideSequence AmpliconSequence and GuideOrientation
def retrieveCRISPRessoInputs(search_term):
    guideSequence = ""
    ampliconSequence = ""
    guideOrientation = ""

    with open('./../Common_amplicon_list.csv', 'r') as file:
        for line in file:
            #Split the line by commas and clean up each column
            columns = line.strip().split(',')
            if columns[0].upper() == search_term:
                guideSequence = columns[1].upper().replace("\r", "").replace("-", "")[:20]
                ampliconSequence = columns[4].upper().replace("\r", "").strip()
                guideOrientation = columns[3].upper().replace("\r", "").strip()
                break

    # Print the retrieved variables
    print(f"Guide Sequence Variable: {guideSequence}")
    print(f"Amplicon Sequence Variable: {ampliconSequence}")
    print(f"Guide Orientation: {guideOrientation}")

    return guideSequence, ampliconSequence, guideOrientation



def run_CRISPResso(ampliconSequence, guideSequence, fastq_files):

    if len(fastq_files) == 2:
        subprocess.run([
            'CRISPResso',
            '--fastq_r1', fastq_files[0],
            '--fastq_r2', fastq_files[1],
            '--amplicon_seq', ampliconSequence,
            '--guide_seq', guideSequence,
            '--quantification_window_size', '10',
            '--quantification_window_center', '-10',
            '--base_editor_output'
        ])
    elif len(fastq_files) == 1:
        subprocess.run([
            'CRISPResso',
            '--fastq_r1', fastq_files[0],
            '--amplicon_seq', ampliconSequence,
            '--guide_seq', guideSequence,
            '--quantification_window_size', '10',
            '--quantification_window_center', '-10',
            '--base_editor_output'
        ])
    else:
        print("No fastq files found for this directory")



#find the fastq file names and see if it is single or paired end reads
def gather_fastqs():
        fastq_files = glob.glob('*R1_001.fastq*') + glob.glob('*R2_001.fastq*')
        return fastq_files




#Main Loop
for directory in os.listdir():
    if os.path.isdir(directory):
        print("-----------")

        os.chdir(directory)
        print(f"The Directory is: {directory}")

        #gather fastq files
        fastq_files = gather_fastqs()
        print(f"Our fastq file(s) are: {fastq_files}")

        #getting the search term from the directory name
        directoryName = os.path.basename(directory)
        searchTerm = directoryName.split('-')[1].upper()
        print(f"Search Term: {searchTerm}")

        #getting the CRISPResso variables using the search term
        guideSequence, ampliconSequence, guideOrientation = retrieveCRISPRessoInputs(searchTerm)

        #run CRISPResso
        run_CRISPResso(ampliconSequence, guideSequence, fastq_files)

        os.chdir('..')
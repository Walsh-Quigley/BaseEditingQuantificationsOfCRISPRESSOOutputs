#location of .py file: /Users/aidanq/Desktop/Bash_Scripts/BaseEditingQuantificationsOfCRISPRESSOOutputs/Read_based_quant.py

import os
import re
from itertools import combinations
import csv
import glob
from datetime import datetime

#rewriting the extractGuideInfo function
def gimmieDat(searchTerm):
    guideSequence = ""
    guideOrientation = ""
    correctionLocationIndex = -1
    permissibleEditsIndicies = []

    with open('./../Common_amplicon_list.csv', 'r') as file:
        for line in file:
            #split the line by commas and clean up each column
            columns = line.strip().split(',')
            if columns[0].upper() == searchTerm:
                guideSequence = columns[1].upper().replace("\r", "").replace("-", "")[:20]
                guideOrientation = columns[3].upper().replace("\r", "").strip()
                correctionLocationPosition = columns[8]
                correctionLocationIndex = int(correctionLocationPosition) - 1
                #this is called list Comprehension combining the iteration condition and 
                #transformatino onto one line and also faster than a for loop
                permissibleEditsIndicies = [int(x) - 1 for x in columns[7].split()]
                break

    # Print the retrieved variables
    print(f"Guide Sequence Variable: {guideSequence}")
    print(f"Intended Edit/Correction Position: {correctionLocationPosition}")
    print(f"Intended Edit/Correction Index (Position -1): {correctionLocationIndex}")
    print(f"Guide Orientation: {guideOrientation}")
    print(f"Permissible Edit Indicies (Position -1): {permissibleEditsIndicies}")

    #checking to see if the correction index is in a logical place
    if not (0 <= int(correctionLocationIndex) <= 19):
        print("\033[4mERROR:\033[0m CorrectionLocationIndex is empty, not a valid integer, or not in the range 0 to 19. i.e. position 1 to 20")
        return 1  # This assumes it's inside a function. Use sys.exit(1) if it's in the main script.

    #check to see if the correction index is an "A"
    if guideSequence[correctionLocationIndex] == 'A':
        print(f"The base at the intended edit index, {correctionLocationIndex}, is an 'A' ")
    else:
        print(f"\033[4mERROR:\033[0m the base at intended edit index, {correctionLocationIndex}, is {guideSequence[correctionLocationIndex]}")

    #check to see if the permissible edits are 'A's
    for index in permissibleEditsIndicies:
        if guideSequence[index] == 'A':
            print(f"The base at index {index} is an 'A'.")
        else:
            print(f"The base at index {index} is {guideSequence[index]}, not an 'A'.")

    #checking to see if the guide is in the forward orientation and calling reverse complement function if not
    if guideOrientation == 'F':
        print("Guide is in the forward orientation")
    else:
        print("the guide is in the reverse orientation, generating reverse complement...")
        guideSequence, correctionLocationIndex, permissibleEditsIndicies = reverseProcessing(guideSequence, correctionLocationIndex, permissibleEditsIndicies)

    return guideSequence, guideOrientation, correctionLocationIndex, permissibleEditsIndicies

def reverseProcessing(guideSequence, correctionLocationIndex, permissibleEditsIndicies):
    RCGuide = reverseComplement(guideSequence)
    print(f"reverse complement of guide sequence {RCGuide}")

    RCcorrectionLocationIndex = abs(correctionLocationIndex - 19)
    print(f"New correction location index: {RCcorrectionLocationIndex}")

    if RCGuide[RCcorrectionLocationIndex] == 'T':
        print(f"The base in the reverse complement guide at the intended edit index is a 'T' ")
    else:
        print(f"\033[4mERROR:\033[0m the base at intended edit index, {correctionLocationIndex}, is {guideSequence[correctionLocationIndex]}")

    RCpermissibleEdits = [abs(int(index) - 19) for index in permissibleEditsIndicies]
    print(f"the new reverse complement permissible edit locations are: {RCpermissibleEdits}")

    return RCGuide, RCcorrectionLocationIndex, RCpermissibleEdits

def reverseComplement(dna):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    # Replace each base with its complement and reverse the resulting sequence
    return ''.join(complement[base] for base in reversed(dna))

def generateSearchSequences(guideSequence, guideOrientation, correctionLocationIndex, permissibleEditsIndicies):
    toleratedSequences = []

    if guideOrientation == "F":
        # Replace the character at correctionLocationIndex with 'G'
        correctedSequence = (guideSequence[:correctionLocationIndex] + 'G' + 
                        guideSequence[correctionLocationIndex + 1:])
    elif guideOrientation == "R":
        # Replace the character at correctionLocationIndex with 'C'
        correctedSequence = (guideSequence[:correctionLocationIndex] + 'C' + 
                        guideSequence[correctionLocationIndex + 1:])
    else:
        print("Invalid guide orientation")
    
    print(f"the corrected guide sequence with intended edit: {correctedSequence}")

    if guideOrientation == "F":
        replacement_letter = "G"
    elif guideOrientation == "R":
        replacement_letter = "C"

    toleratedSequences = generate_toleratedSequences(correctedSequence, permissibleEditsIndicies, replacement_letter)

    toleratedSequences.append(correctedSequence)

    return toleratedSequences, correctedSequence

def generate_toleratedSequences(sequence, indices, replacement_letter):
    toleratedSequences = []

    # Iterate over all possible numbers of positions to replace (1 to len(indices))
    for r in range(1, len(indices) + 1):
        # Generate all combinations of r indices
        for combo in combinations(indices, r):
            # Create a new sequence for this combination of indices
            new_sequence = list(sequence)  # Convert to list for mutability
            for index in combo:
                new_sequence[index] = replacement_letter
            toleratedSequences.append(''.join(new_sequence))  # Convert back to string

    return toleratedSequences

def CRISPRessoDirectoryHelperFunction():
    # Get a list of all items in the current directory
    current_dir = os.getcwd()
    subdirs = [d for d in os.listdir(current_dir) if os.path.isdir(d) and d.startswith("CRISPResso_")]

    if not subdirs:
        print("No directory starting with 'CRISPResso_' found.")
        return False

    # Assuming you want to change to the first matching directory
    target_dir = subdirs[0]
    os.chdir(target_dir)
    return True

def sum_last_column(output_file):
    total = 0
    with open(output_file, 'r') as outfile:
        reader = csv.reader(outfile)
        next(reader)  # Skip the header row
        for row in reader:
            try:
                # Convert the last column to a float and add it to the total
                total += float(row[-1])  # Assuming the last column is numeric
            except ValueError:
                # Handle case where the last column is not numeric
                print(f"Skipping row with non-numeric value in the last column: {row}")
                continue

    return total

def append_header_and_timestamp(csv_file):
    # Check if the file exists
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, 'a', newline='') as result_file:
        writer = csv.writer(result_file)

        # Add header if the file doesn't exist
        if not file_exists:
            writer.writerow(['Directory',
                             'Read-based Lenient Correction Percentage (with tolerated bystanders)', 
                             'Read-based Strict Correction', 
                             'Independent Nucleotide Based Editing Quantification Percentage (taken from Quantification_window_nucleotide_percentage_table)',
                             'Reads Aligned', 
                             'Reads Total', 
                             'Guide Sequence (reverse complement if guide is in reverse orientation from amplicon)',
                             'Guide Sequence relative to amplicon',
                             'Index of Intended Edit (+1 for position)',
                             'Index of Permissible Bystanders (+1 for position)',
                             'Strings used to search the Alleles_frequency_table in the CRISPResso output'])  # Write the header

        # Get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Append the last run line with timestamp
        writer.writerow([f"the below analysis was run @ {current_time}"])

def allelesTableFilter(arrayOfStrings, output_file):
    if type(arrayOfStrings) == 'str':
        print(f"Incorrect Data Structure passed: {type(arrayOfStrings)}")

    correctionSum = -1
    CRISPRessoDirectoryHelperFunction()

    input_files = glob.glob("Alleles_frequency_table*.txt")

    if not input_files:
        print("No file starting with 'Alleles_frequency_table' found.")
    else:
        input_file = input_files[0]  # Take the first matching file
        print(f"Found alleles table input file: {input_file}")

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')  # Tab-delimited reader
        writer = csv.writer(outfile)  # Default is comma-delimited for CSV

        #move the ehader to the output file
        header = next(reader)
        writer.writerow(header)

        # Process each row
        for row in reader:
            row_first_column = row[0].strip().upper()
            # print(f"{row_first_column}")
            if any(s.strip().upper() in row_first_column for s in arrayOfStrings):  # Check if any string in the array matches
                writer.writerow(row)  # Write matching row to the output file

    correctionSum = sum_last_column(output_file)

    print(f"New file generated: {output_file}")

    os.chdir("..")

    return correctionSum

def extractReadCounts():
    readsAligned = -1
    readsTotal = -1

    CRISPRessoDirectoryHelperFunction()

    CRISPRessoMappingStatsFile = "CRISPResso_mapping_statistics.txt"
    
    with open(CRISPRessoMappingStatsFile, "r") as file:
        header = file.readline()
        data_line = file.readline().strip()
        col = data_line.split("\t")
        readsAligned = int(col[2])
        readsTotal = int(col[0])

    print(f"The number of reads that align is: {readsAligned}")
    print(f"The total number of reads: {readsTotal}")

    os.chdir("..")

    return readsAligned, readsTotal

def generateQuantificationOutput(directory, 
                                 lenient, 
                                 strict,
                                 independentQuant, 
                                 readsAligned, 
                                 readsTotal, 
                                 guideSequence,
                                 guideOrientation,
                                 correctionIndex,
                                 permissibleEdits,
                                 toleratedSequences):
        
        directoryTruncated = directory.split("_L001")[0]
        analysis_result_file = "../AQ_Read_Based_Correction.csv"

        print(f"Lenient correction percentage for {directoryTruncated}: {lenient}")
        with open(analysis_result_file, 'a', newline='') as result_file:
            writer = csv.writer(result_file)
            writer.writerow([directoryTruncated, lenient, strict, independentQuant, readsAligned, readsTotal, guideSequence, guideOrientation, correctionIndex, permissibleEdits, toleratedSequences])

def independentQuant(correctionLocationIndex, guideOrientation):
    independentQuantSum = -1

    CRISPRessoDirectoryHelperFunction()
    nucleotidePercentageFile = "Quantification_window_nucleotide_percentage_table.txt"
    print(correctionLocationIndex)
    print(guideOrientation)

    if guideOrientation == "R":
        row_index = 2
    else:
        row_index = 3

    col_index = int(correctionLocationIndex) + 1

    with open(nucleotidePercentageFile, "r") as file:
        lines = file.readlines()

        target_row = lines[row_index].strip()
        col = target_row.split("\t")
        independentQuantSum = col[col_index]

    os.chdir("..")
    return independentQuantSum

append_header_and_timestamp("AQ_Read_Based_Correction.csv")

#rewriting the main loop
for directory in os.listdir():
    #checks if the current item (directory) is a directory and not a file
    #if it returns true then the next block of code is allowed to run 
    if os.path.isdir(directory):
        print("-----------------")

        print(f"the Directory is: {directory}")

        #changes the working directory to the current directory meaning 
        #subsequent operations will be relative to this subdirectory
        os.chdir(directory)

        #getting the search term from the directory name using the dash delimiter
        directoryName = os.path.basename(directory)
        searchTerm = re.split('[-_]', directory)[1]. upper()
        print(f"The Search Term is: {searchTerm}")

        #passing that search term to the function that will extract all the info from 
        #common amplicons list
        guideSequence, guideOrientation, correctionLocationIndex, permissibleEditsIndicies = gimmieDat(searchTerm)

        #generating the sequences that we will filter for
        toleratedSequences, correctedSequence = generateSearchSequences(guideSequence, guideOrientation, correctionLocationIndex, permissibleEditsIndicies)

        #search the alleles freq table for our tolerated sequences
        lenientCorrectionFile = "../AQLenientCorrection.csv"
        lenientCorrectionSum = allelesTableFilter(toleratedSequences, lenientCorrectionFile)
        print(f"the lenient correction percentage is: {lenientCorrectionSum}")

        #search alleles freq table for the strict edit
        correctedSequenceArray = [correctedSequence]
        strictCorrectionFile = "../AQStrictCorrection.csv"
        strictCorrectionSum = allelesTableFilter(correctedSequenceArray, strictCorrectionFile)
        print(f"the strict correction percentage is: {strictCorrectionSum}")

        #grabbing the read counts
        readsAligned, readsTotal = extractReadCounts()

        #grabbing independent editing quantification data from quantification_window_nucleotide_percentage_table.txt
        independentQuantSum = independentQuant(correctionLocationIndex, guideOrientation)

        print(f"the independent quant sum is: {independentQuantSum}")


        #generate the table containing the quantification output
        generateQuantificationOutput(directory, lenientCorrectionSum, strictCorrectionSum, independentQuantSum, readsAligned, readsTotal, guideSequence, guideOrientation, correctionLocationIndex, permissibleEditsIndicies, toleratedSequences)

        os.chdir("..")


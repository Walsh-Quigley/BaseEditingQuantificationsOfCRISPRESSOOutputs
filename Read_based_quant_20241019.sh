# Function to generate reverse complement of a DNA sequence
reverse_complement() {
    local seq="$1"
    # Reverse the sequence and replace the nucleotides with their complements
    echo "$seq" | rev | tr 'ATCG' 'TAGC'
}

# Editing quantification loop
for DIR in */; do

    # Move into the directory
    cd "$DIR";

    # Get the directory name
    directoryName=$(basename "$DIR")

    # Turn the name into a search term for searching the spreadsheet
    searchTerm=$(echo "$directoryName" | awk -F'[-]' '{print $2}')

    # Print the search term for visibility
    echo "The search term is: $searchTerm"
    
    # Grab relevant variables
    guideSeqVar=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $2}' ./../Common_amplicon_list.csv | tr '[:lower:]' '[:upper:]' | tr -d '\r' | tr -d '-' | xargs | cut -c1-20 )
    ampSeqVar=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $5}' ./../Common_amplicon_list.csv | tr '[:lower:]' '[:upper:]' | tr -d '\r' | xargs)
    guideOrientation=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $4}' ./../Common_amplicon_list.csv | tr '[:lower:]' '[:upper:]' | tr -d '\r' | xargs)
    intendedEditIndex=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $9}' ./../Common_amplicon_list.csv )
    PermissibleEditIndex=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $8}' ./../Common_amplicon_list.csv )

    echo "LINE 29: This is the Index of the Intended Edit: $intendedEditIndex"

    PermissibleEditArray=($PermissibleEditIndex)

    # Print the array elements
    echo "LINE 36: The silent or tolerated bystanders are at positions: ${PermissibleEditArray[@]}"

    # Check if the character at intendedEditIndex in guideSeqVar is "A"
    index=$((intendedEditIndex - 1)) # Adjust for 0-based indexing
    charAtIndex=${guideSeqVar:$index:1}

    if [[ "$charAtIndex" == "A" ]]; then
        echo "LINE 43: The character at position $intendedEditIndex in guideSeqVar is A."
    else
        echo "The character at position $intendedEditIndex in guideSeqVar is not A, it's $charAtIndex."
    fi

    # Create an array of modified guideSeqVar with A switched to G at intendedEditIndex
    permissibleEditStrings=()

    # Replace A with G at the intendedEditIndex and add to the array
    if [[ "$charAtIndex" == "A" ]]; then
        modifiedSeqVar="${guideSeqVar:0:$index}G${guideSeqVar:$((index + 1))}" # Replace A at intended index
        permissibleEditStrings+=("$modifiedSeqVar")
    else
        echo "LINE 75: No replacement was made as the character at intendedEditIndex: $intendedEditIndex is not A."
    fi

    # For each permissible index, create a new sequence with A replaced by G
    for permissibleIndex in "${PermissibleEditArray[@]}"; do
        index=$((permissibleIndex - 1))  # Convert 1-based index to 0-based
        charAtPermissibleIndex=${guideSeqVar:$index:1}
        
        # Create a new modified sequence if the character at the permissible index is A
        if [[ "$charAtPermissibleIndex" == "A" ]]; then
            # Construct the new sequence by switching A to G at permissible index
            newModifiedSeq="${modifiedSeqVar:0:$index}G${modifiedSeqVar:$((index + 1))}"  # Use modifiedSeqVar
            permissibleEditStrings+=("$newModifiedSeq")  # Add the new sequence to the array
            echo "LINE 85: New modified sequence after replacing A with G at position $permissibleIndex: $newModifiedSeq"
        fi
    done

        # Check if guideOrientation is R, and if so, replace all elements with their reverse complements
    if [[ "$guideOrientation" == "R" ]]; then
        echo "Guide orientation is R. Generating reverse complements..."
        for (( i=0; i<${#permissibleEditStrings[@]}; i++ )); do
            reverseComp=$(reverse_complement "${permissibleEditStrings[$i]}")
            permissibleEditStrings[$i]="$reverseComp"
            echo "Reverse complement of ${permissibleEditStrings[$i]}: $reverseComp"
        done
    else
    echo "The guide is in the same orientation as the amplicon."
    fi

    # Print the final array of modified sequences
    echo "Final search terms with permissible edits: ${permissibleEditStrings[@]}"
    disclaimerText="This is only the intended edit and single chances at permissible locations. it is not combinations of permissible locations"
    echo "$disclaimerText"



    #go into the CRISPResso folder and pull out the alleles_freq table and turn it into a csv
    echo "LINE 85:$PWD"
    ls
    cd CRISPR*
    readBasedAlignmentTxt=$(ls Alleles_frequency_table_around_sgRNA_*.txt 2>/dev/null)
    readBasedAlignmentTable="Alleles_frequency_table_around_sgRNA.csv"
    sed 's/\t/,/g' "$readBasedAlignmentTxt" > "$readBasedAlignmentTable"
    lenientCorrection="corrected_lenient.csv"

    header=$(head -n 1 "$readBasedAlignmentTable")
    echo "$header" > "$lenientCorrection"

    for string in "${permissibleEditStrings[@]}"; do
        awk -v search="$string" -F',' '$1 ~ search {print $0}' "$readBasedAlignmentTable" >> "$lenientCorrection"
    done

    # Sum the last column of the output file (excluding the header)
    lenientCorrectionSum=$(awk -F',' 'NR>1 { total += $NF } END { print total }' "$lenientCorrection")

    # Print the sum to the console
    echo "Sum of the last column: $lenientCorrectionSum"

    cd ..

    # Combine searchTerm with extracted values and write to CSV
    final="$directoryName,$lenientCorrectionSum,$disclaimerText"
    echo "$final" >> ./../Correction_Example.csv

    # Move back out of the directory to the main directory
    cd ..;

done

# Function to generate reverse complement of a DNA sequence
reverse_complement() {
    local seq="$1"
    # Reverse the sequence and replace the nucleotides with their complements
    echo "$seq" | rev | tr 'ATCG' 'TAGC'
}

# Function to generate all combinations of permissible edits
generate_combinations() {
    local baseSeq="$1"
    local intendedEditIndex="$2"
    local permissibleEditArray=("${!3}")

    # Create an array to hold all possible sequences with combinations of permissible edits
    local result=()

    # Start with the intended edit (replace 'A' at intendedEditIndex with 'G')
    local index=$((intendedEditIndex - 1))  # Convert to 0-based index
    local firstEdit="${baseSeq:0:$index}G${baseSeq:$((index + 1))}"
    result+=("$firstEdit")

    # Generate all combinations of permissible edits
    local numPermissible=${#permissibleEditArray[@]}
    local numCombinations=$((2 ** numPermissible))


    for (( i=1; i<numCombinations; i++ )); do
        modifiedSeq="$firstEdit"  

        for (( j=0; j<numPermissible; j++ )); do
            if (( (i >> j) & 1 )); then
                permissibleIndex=$((permissibleEditArray[j] - 1))
                charAtPermissibleIndex=${modifiedSeq:$permissibleIndex:1}

                # Only replace 'A' with 'G' at permissible positions
                if [[ "$charAtPermissibleIndex" == "A" ]]; then
                    modifiedSeq="${modifiedSeq:0:$permissibleIndex}G${modifiedSeq:$((permissibleIndex + 1))}"
                fi
            fi
        done

        result+=("$modifiedSeq")
    done

    echo "${result[@]}"
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
    guideSeq=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $2}' ./../Common_amplicon_list.csv | tr '[:lower:]' '[:upper:]' | tr -d '\r' | tr -d '-' | xargs | cut -c1-20 )
    ampSeqVar=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $5}' ./../Common_amplicon_list.csv | tr '[:lower:]' '[:upper:]' | tr -d '\r' | xargs)
    guideOrientation=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $4}' ./../Common_amplicon_list.csv | tr '[:lower:]' '[:upper:]' | tr -d '\r' | xargs)
    intendedEditIndex=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $9}' ./../Common_amplicon_list.csv )
    permissibleEditIndex=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $8}' ./../Common_amplicon_list.csv )

    echo "LINE 29: This is the Index of the Intended Edit: $intendedEditIndex"

    permissibleEditArray=($permissibleEditIndex)

    # Print the array elements
    echo "LINE 36: The silent or tolerated bystanders are at positions: ${permissibleEditArray[@]}"

    # Check if the character at intendedEditIndex in guideSeq is "A"
    index=$((intendedEditIndex - 1)) # Adjust for 0-based indexing
    charAtIndex=${guideSeq:$index:1}

    if [[ "$charAtIndex" == "A" ]]; then
        echo "LINE 43: The character at position $intendedEditIndex in guideSeq is A."
    else
        echo "The character at position $intendedEditIndex in guideSeq is not A, it's $charAtIndex."
    fi

    # Generate all combinations of permissible edits
    permissibleEditStrings=($(generate_combinations "$guideSeq" "$intendedEditIndex" permissibleEditArray[@]))
    echo "Permissible edit combinations generated: ${#permissibleEditStrings[@]} sequences."

    # # Replace A with G at the intendedEditIndex and add to the array
    # if [[ "$charAtIndex" == "A" ]]; then
    #     modifiedSeqVar="${guideSeq:0:$index}G${guideSeq:$((index + 1))}" # Replace A at intended index
    #     permissibleEditStrings+=("$modifiedSeqVar")
    # else
    #     echo "LINE 75: No replacement was made as the character at intendedEditIndex: $intendedEditIndex is not A."
    # fi

    # # For each permissible index, create a new sequence with A replaced by G
    # for permissibleIndex in "${permissibleEditArray[@]}"; do
    #     index=$((permissibleIndex - 1))  # Convert 1-based index to 0-based
    #     charAtPermissibleIndex=${guideSeq:$index:1}
        
    #     # Create a new modified sequence if the character at the permissible index is A
    #     if [[ "$charAtPermissibleIndex" == "A" ]]; then
    #         # Construct the new sequence by switching A to G at permissible index
    #         newModifiedSeq="${modifiedSeqVar:0:$index}G${modifiedSeqVar:$((index + 1))}"  # Use modifiedSeqVar
    #         permissibleEditStrings+=("$newModifiedSeq")  # Add the new sequence to the array
    #         echo "LINE 85: New modified sequence after replacing A with G at position $permissibleIndex: $newModifiedSeq"
    #     fi
    # done

    # Handle guideOrientation being "R" for reverse complement
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
    final="$directoryName,$lenientCorrectionSum"
    echo "$final" >> ./../Correction_Example.csv

    # Move back out of the directory to the main directory
    cd ..;

done

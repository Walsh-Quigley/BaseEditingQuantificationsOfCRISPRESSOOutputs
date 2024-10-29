for DIR in */; do

    echo "----------"

    #move into the directory
    cd "$DIR";

    #get the directory name
    directoryName=$(basename "$DIR")

    #turn the name into a search term for searching the spreadsheet
    searchTerm=$(echo "$directoryName" | awk -F'[-]' '{print $2}')


    #Print the search term so we can have some visibility in the console
    echo "Search Term: $searchTerm"
    

    #grab relevant variables
    guideSeqVar=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $2}' ./../Common_amplicon_list.csv | tr '[:lower:]' '[:upper:]' | tr -d '\r' | tr -d '-' | xargs | cut -c1-20 )
    ampSeqVar=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $5}' ./../Common_amplicon_list.csv | tr '[:lower:]' '[:upper:]' | tr -d '\r' | xargs)
    guideOrientation=$(awk -F',' -v searchTerm="$searchTerm" '$1 == searchTerm {print $4}' ./../Common_amplicon_list.csv | tr '[:lower:]' '[:upper:]' | tr -d '\r' | xargs)


    #Print these variables so we have visibility in the console
    echo "$guideSeqVar"
    echo "$ampSeqVar"
    echo "$directoryName"
    echo "$guideOrientation"
# check if the directory contains two fastq files
    fastqFiles=(*.fastq*)
    if [[ ${#fastqFiles[@]} -eq 2 ]]; then
        # run CRISPResso with both R1 and R2
        CRISPResso \
        --fastq_r1 *R1_001.fastq* \
        --fastq_r2 *R2_001.fastq* \
        --amplicon_seq "$ampSeqVar" \
        --guide_seq "$guideSeqVar" \
        --quantification_window_size 10 \
        --quantification_window_center -10 \
        --base_editor_output;
    else
        # run CRISPResso with only R1
        CRISPResso \
        --fastq_r1 *R1_001.fastq* \
        --amplicon_seq "$ampSeqVar" \
        --guide_seq "$guideSeqVar" \
        --quantification_window_size 10 \
        --quantification_window_center -10 \
        --base_editor_output;
    fi
    #move back out of the directory to the main directory
    cd ..;

done


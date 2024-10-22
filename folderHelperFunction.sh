
#here we make a txt list of all the directories we want to create
for file in *; do 
	echo "$file" | cut -d "." -f 1 >> DIRlist.txt;
done

#we then sort the list so that we get rid of duplicates
sort DIRlist.txt | uniq > DIRlist2.txt

#we then make the directories from the sorted list
cat DIRlist2.txt | xargs -L 1 mkdir


#we then put the files into the specific directories that they belong in
for file in *; do

	if [[ $file == *"fastq.gz" ]]; then

		currentfile=$file;
		currentfolder=($(echo $currentfile | cut -d "." -f 1));
		mv $file $currentfolder
		echo $currentfolder
	
	fi;
done
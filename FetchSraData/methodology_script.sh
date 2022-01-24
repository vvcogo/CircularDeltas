#!/bin/bash
if [ "$#" -ne "1" ]; then
    echo "Error. Not enough arguments."
	echo "EXAMPLE: ./methodology_script.sh [file]input.txt"
    exit 1
fi

# Constants
NUM_READS_PER_QUERY=99
MAX_LEN=1005

# Args
INPUT=$1
INPUT_FILENAME=`basename $INPUT`

# Loop
for ACCESSION in `cat $INPUT | cut -d, -f1`
do
#	echo $ACCESSION
	NUM_ENTRIES=`cat accession_sizes.log | grep $ACCESSION | cut -d, -f2`
	HASH=`cksum <<< $ACCESSION | cut -f 1 -d ' '`
#	echo $HASH
#	echo $NUM_ENTRIES
	RND_POS=`python3 rng.py $HASH 1 $NUM_ENTRIES`
#	echo $RND_POS
	RND_POS_END=`echo "$RND_POS+$NUM_READS_PER_QUERY" | bc`
#	fastq-dump -N $RND_POS -X $RND_POS_END --skip-technical -Z $ACCESSION >> results/$INPUT_FILENAME.fastq 2>>errors/$INPUT_FILENAME.errors
	ENTRIES=`fastq-dump -N $RND_POS -X $RND_POS_END --skip-technical -Z $ACCESSION 2>>/dev/null`
	SUCCESS=$?
#	echo $SUCCESS
	
	
	if [ "$SUCCESS" == "0" ]
	then
		I=0
		while IFS= read -r LINE
		do		
			I=`echo "($I+1)%4" | bc`
			case "$I" in
#				1)
#				echo -n "C1 "
#				;;

				"2")
				DNA=`echo $LINE |  tr -d '\001'-'\011''\013''\014''\016'-'\037''\200'-'\377'`
				DNA_LEN=`echo $DNA | wc -m`
				DNA_HAS_ID=`echo "$DNA" | grep $ACCESSION | wc -l`
				;;

#				"3")
#				echo -n "C2 "
#				;;
				
				"0")
				QS=`echo $LINE |  tr -d '\001'-'\011''\013''\014''\016'-'\037''\200'-'\377'`
				QS_LEN=`echo $QS | wc -m`
				QS_HAS_ID=`echo "$QS" | grep $ACCESSION | wc -l`
				if [ "$DNA_LEN" == "$QS_LEN" -a "$QS_LEN" -lt "$MAX_LEN" -a "$DNA_HAS_ID" == "0" -a "$QS_HAS_ID" == "0" ]
				then
					echo $LINE
				fi
				;;

#				*)
#				echo -n "unknown"
#				;;
			esac
#			echo "$LINE"		
		done < <(printf '%s\n' "$ENTRIES")
#		for ENTRY in $ENTRIES
#		do
#			ENTRY_LENGTH=`echo $ENTRY | wc -m`
#			if [ "$ENTRY_LENGTH" -lt "$MAX_LENGTH" ]
#			then
#				echo $ENTRY
#			fi
#		done
	fi
done

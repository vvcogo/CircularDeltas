#!/bin/bash
if [ "$#" -ne "2" ]; then
    echo "Error. Not enough arguments."
        echo "EXAMPLE: ./methodology_script.sh [file]input.txt"
    exit 1
fi

INPUT=$1
INPUT_FILENAME=`basename $INPUT`
FILE_SIZE=$2
#FILE_SIZE=`declare -i $INPUT_SIZE`


mkdir -p -- "results_fastq_$INPUT_FILENAME"
mkdir -p -- "errors_fastq_$INPUT_FILENAME"
D=`date +%s`

                # awk '(NR>1)'  para pular a primeira linha
for ACCESSION in `cat $INPUT | awk '(NR>1)' | cut -d, -f1`       #pega os SRR do argumento
do
        NUM_ENTRIES=`cat $INPUT | grep $ACCESSION | cut -d, -f2`       # para cada SRR pega os spots
        HASH=`cksum <<< $ACCESSION | cut -f 1 -d ' '`
        echo "$NUM_ENTRIES"
        PERCENTAGE_SPOTSAVG=`cat $INPUT | grep $ACCESSION | cut -d, -f5`
        AVGLENGTH=`cat $INPUT | grep $ACCESSION | cut -d, -f3`

        NUM_READS_PER_QUERY=`python3 calculate_num_entries.py $PERCENTAGE_SPOTSAVG $FILE_SIZE $AVGLENGTH`
        echo "$NUM_READS_PER_QUERY"
        MAXIMUN_ENTRIES=`echo "$NUM_ENTRIES - $NUM_READS_PER_QUERY" | bc`
        echo "$MAXIMUN_ENTRIES"
        RND_POS=`python3 rng.py $HASH $MAXIMUN_ENTRIES `
        echo "$RND_POS"
        RND_POS_END=`echo "$RND_POS+$NUM_READS_PER_QUERY" | bc`
        fastq-dump -N $RND_POS -X $RND_POS_END --skip-technical -Z $ACCESSION >> results_fastq_$INPUT_FILENAME/$INPUT_FILENAME-${D}.fastq 2>>errors_fastq_$INPUT_FILENAME/$INPUT_FILENAME-${D}.errors
        #fastq-dump -N 0 -X 1 --skip-technical -Z $ACCESSION >> results_fastq_$INPUT_FILENAME/$INPUT_FILENAME-${D}.fastq 2>>errors_fastq_$INPUT_FILENAME/$INPUT_FILENAME-${D}.errors



done

awk 'NR%4 == 0 {print}' results_fastq_$INPUT_FILENAME/$INPUT_FILENAME-${D}.fastq >> results_fastq_$INPUT_FILENAME/$INPUT_FILENAME-${D}_reduced.txt

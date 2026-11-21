#!/bin/bash

# Usage Instructions
function usage() {
    cat <<USAGE

    Usage: $0 [-f FILENAME]

    Options:
	-f, --filename: The input file containing a list of datafiles to download
USAGE
    exit 1
}

# Checking for empty input
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

FILENAME="download.txt"

# Reading inputs
while [ "$1" != "" ]; do
    case $1 in
    -f | --filename)
	shift
	FILENAME=$1
	;;
    -h | --help)
        usage # run usage function
        ;;
    *)
        echo "Unknown option $1"
        usage
        exit 1
        ;;
    esac
    shift
done

mapfile -t files < $FILENAME

echo $files

for file in "${files[@]}"; do
    curl -k -o "$file" "https://eas.esac.esa.int/sas-dd/data?file_name="$file"&release=sedm&RETRIEVAL_TYPE=FILE'"
done




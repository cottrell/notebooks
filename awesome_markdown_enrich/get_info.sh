#!/bin/bash
if [[ "$#" -ne 1 ]]; then
    >&2 echo usage: $0 file
    exit 1
fi
DIR="$( cd "$(dirname "$0")" ; pwd -P )"
echo name,url,date
$DIR/get_links.sh $1 | while read x; do
    name=$(echo $x | cut -d, -f1)
    url=$(echo $x | cut -d, -f2)
    latest_date=$($DIR/get_date_latest_commit.bash $url)
    echo $name,$url,$latest_date
done

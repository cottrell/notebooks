#!/bin/bash

# brew install poppler

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
[[ -d "$DIR/pdf" ]] || mkdir -p $DIR/pdf
[[ -d "$DIR/text" ]] || mkdir -p $DIR/text

for x in $(seq 1 678); do
    pdf=work"$x".pdf
    text=work"$x".text
    echo $pdf $text
    [[ -e "$DIR/pdf/$pdf" ]] || curl https://www.bis.org/publ/$pdf -o $DIR/pdf/$pdf
    # TODO should remove text if pdf not exist
    [[ -e "$DIR/text/$text" ]] || pdftotext $DIR/pdf/$pdf -nopgbrk $DIR/text/$text
    # [[ $(( $x % 10 )) -eq 0 ]] && wait
done
# wait

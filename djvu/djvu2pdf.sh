#!/bin/bash -e

# Method found here https://askubuntu.com/a/122604/423332

# Dependencies:
# On ubuntu, you can install ocrodjvu and pdfbeads with:
#   sudo apt install ocrodjvu
#   gem install pdfbeads

# The path and filename given can only contain ascii characters
f=$1

# Get filename
filename=$(basename -- "$f")
extension="${filename##*.}"
file_no_ext="${filename%.*}"

# Count number of pages
p=$(djvused -e n "$f")
echo -e "The document contains $p pages.\n"

# Number of digits
pp=${#p}

echo "###############################"
echo "### Extracting page by page ###"
echo "###############################"

# For each page, extract the text, and the image
for i in $( seq 1 $p)
do
    ii=$(printf %0${pp}d $i)
    djvu2hocr -p $i "$f" | sed 's/ocrx/ocr/g' > pg$ii.html
    ddjvu -format=tiff -page=$i "$f" pg$ii.tiff
done

echo ""
echo "##############################"
echo "### Building the final pdf ###"
echo "##############################"

# Build the final pdf
pdfbeads > $file_no_ext.pdf

echo ""
echo "Done"


# Remove temp files
echo ""
read -p "Do you want to delete temp files ? (pg*.html,  pg*.tiff,  pg*.bg.jpg) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    rm pg*.html pg*.tiff pg*.bg.jpg
fi



sed 's/,$//g' Francisella\ tularensis-goa-association.txt > test.txt
sed 's/,/;/g' test.txt > test2.txt
cat test2.txt > Francisella\ tularensis-goa-association.txt

sed 's/,$//g' Bacillus\ anthracis-goa-association.txt > test.txt
sed 's/,/;/g' test.txt > test2.txt
cat test2.txt > Bacillus\ anthracis-goa-association.txt

sed 's/,$//g' Yersinia\ pestis-goa-association.txt > test.txt
sed 's/,/;/g' test.txt > test2.txt
cat test2.txt > Yersinia\ pestis-goa-association.txt

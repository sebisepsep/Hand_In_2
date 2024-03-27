echo "Hello :)"

echo "1a" 
python3 a1.py

echo "1b" 
python3 b1.py

echo "1c" 
python3 c1.py

echo "1d" 
python3 d1.py

echo "2a" 
python3 a2.py

echo "2b" 
python3 b2.py

echo "Generating the pdf"
pdflatex template.tex
bibtex template.aux
pdflatex template.tex
pdflatex template.tex
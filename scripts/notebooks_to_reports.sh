mkdir reports

./venv/bin/jupyter nbconvert ./notebooks/report.ipynb --no-input --output-dir='./reports' --to 'html' 

# Requires having wkhtmltopdf installed
wkhtmltopdf ./reports/report.html ./reports/report.pdf

rm ./reports/report.html

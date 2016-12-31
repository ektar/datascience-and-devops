all: last_output.txt

last_output.txt: *ipynb
	mkdir -p nbconvert/html
	mkdir -p nbconvert/python
	jupyter-nbconvert *ipynb --to python --output-dir=nbconvert/python
#	jupyter-nbconvert "$?" --to html --output-dir=nbconvert/html
	date > last_output.txt
	git rev-parse HEAD >> last_output.txt

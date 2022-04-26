.PHONY: clean

clean:
	rm -r __pycache__
	rm -r src/__pycache__
	rm -r src/config/__pycache__
	rm -r src/model/__pycache__

run:
	python app.py


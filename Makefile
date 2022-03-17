.PHONY: clean

clean:
	rm -r __pycache__
	rm -r src/__pycache__
	rm -r src/model/__pycache__
	rm -r src/controller/__pycache__

run:
	python app.py


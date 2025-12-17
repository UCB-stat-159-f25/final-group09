.PHONY: env test all pdf clean
env:
	mamba env create -f environment.yml || mamba env update -f environment.yml
test:
	pytest tests/ -v
all:
	jupyter nbconvert --to notebook --execute analysis/*.ipynb
pdf:
	jupyter nbconvert --to pdf analysis/*.ipynb --output-dir pdf_builds/
clean:
	rm -rf __pycache__ .pytest_cache
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf .ipynb_checkpoints
	rm -rf analysis/.ipynb_checkpoints

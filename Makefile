.PHONY: env test all pdf clean

env:
	mamba env create -f environment.yml || mamba env update -f environment.yml

test:
	pytest tests/ -v

all:
	jupyter nbconvert --to notebook --execute notebooks/*.ipynb

pdf:
	cd notebooks && myst build --pdf

clean:
	rm -rf __pycache__ .pytest_cache
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf .ipynb_checkpoints
	rm -rf notebooks/.ipynb_checkpoints

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = TenGP
SOURCEDIR     = sphinx/source
BUILDDIR      = sphinx/build
DOCSDIR       = docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

test:
	python -m pytest -s -v

develop:
	python setup.py develop

baseline:
	python -m experiments.baseline nguyen4 -d train -t 50 -o results/baseline-nguyen4.log &
	python -m experiments.baseline nguyen7 -d train -t 50 -o results/baseline-nguyen7.log &
	python -m experiments.baseline nguyen8 -d train -t 50 -o results/baseline-nguyen8.log &
	python -m experiments.baseline nguyen10 -d train -t 50 -o results/baseline-nguyen10.log &
	python -m experiments.baseline keijzer4 -d train -t 50 -o results/baseline-keijzer4.log &
	python -m experiments.baseline keijzer11 -d train -t 50 -o results/baseline-keijzer11.log &
	python -m experiments.baseline keijzer12 -d train -t 50 -o results/baseline-keijzer12.log &
	python -m experiments.baseline korns1 -d train -t 50 -o results/baseline-korns1.log &
	python -m experiments.baseline korns7 -d train -t 50 -o results/baseline-korns7.log &
	python -m experiments.baseline korns12 -d train -t 50 -o results/baseline-korns12.log &
	python -m experiments.baseline pagie1 -d train -t 50 -o results/baseline-pagie1.log &
	python -m experiments.baseline vladislasleva4 -d train -t 50 -o results/baseline-vladislasleva4.log && fg


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp -r $(BUILDDIR)/html/. $(DOCSDIR)


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

install:
	pip install .

html:
	@$(SPHINXBUILD) -Eab html "$(SOURCEDIR)" "$(BUILDDIR)"  $(SPHINXOPTS) $(O)
	echo 'copy'
	cp -r $(BUILDDIR)/. $(DOCSDIR)

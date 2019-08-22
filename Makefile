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


pso:
	python -m experiments.pso nguyen4 -d train -t 50 -o results/pso-nguyen4.log &
	python -m experiments.pso nguyen7 -d train -t 50 -o results/pso-nguyen7.log &
	python -m experiments.pso nguyen8 -d train -t 50 -o results/pso-nguyen8.log &
	python -m experiments.pso nguyen10 -d train -t 50 -o results/pso-nguyen10.log &
	python -m experiments.pso keijzer4 -d train -t 50 -o results/pso-keijzer4.log &
	python -m experiments.pso keijzer11 -d train -t 50 -o results/pso-keijzer11.log &
	python -m experiments.pso keijzer12 -d train -t 50 -o results/pso-keijzer12.log && fg


ffrpso:
	python -m experiments.ffrpso nguyen4 -d train -t 50 -o results/ffrpso-nguyen4.log &
	python -m experiments.ffrpso nguyen7 -d train -t 50 -o results/ffrpso-nguyen7.log &
	python -m experiments.ffrpso nguyen8 -d train -t 50 -o results/ffrpso-nguyen8.log &
	python -m experiments.ffrpso nguyen10 -d train -t 50 -o results/ffrpso-nguyen10.log &
	python -m experiments.ffrpso keijzer4 -d train -t 50 -o results/ffrpso-keijzer4.log &
	python -m experiments.ffrpso keijzer11 -d train -t 50 -o results/ffrpso-keijzer11.log &
	python -m experiments.ffrpso keijzer12 -d train -t 50 -o results/ffrpso-keijzer12.log && fg

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp -r $(BUILDDIR)/html/. $(DOCSDIR)


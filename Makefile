# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = TenGP
SOURCEDIR     = sphinx/source
BUILDDIR      = sphinx/build
DOCSDIR       = docs
DIST          = $(shell git rev-parse --short HEAD)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile


test:
	python -m pytest -s -v

develop:
	python setup.py develop

baseline:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.baseline $$bench -d train -t 50 -o results/${DIST}/baseline-$$bench.jsonl & \
	done
	fg && fg

	
pso:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.pso $$bench -d train -t 50 -o results/${DIST}/pso-$$bench.jsonl & \
	done
	fg && fg

sea:
	python -m experiments.sea nguyen4 -d train -t 50 -o results/sea-nguyen4.log &
	python -m experiments.sea nguyen7 -d train -t 50 -o results/sea-nguyen7.log &
	python -m experiments.sea nguyen8 -d train -t 50 -o results/sea-nguyen8.log &
	python -m experiments.sea nguyen10 -d train -t 50 -o results/sea-nguyen10.log &
	python -m experiments.sea keijzer4 -d train -t 50 -o results/sea-keijzer4.log &
	python -m experiments.sea keijzer11 -d train -t 50 -o results/sea-keijzer11.log &
	python -m experiments.sea keijzer12 -d train -t 50 -o results/sea-keijzer12.log && fg

xnes:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.xnes $$bench -d train -t 50 -o results/${DIST}/xnes-$$bench.jsonl & \
	done
	fg && fg

cmaes:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.cmaes $$bench -d train -t 50 -o results/${DIST}/cmaes-$$bench.jsonl & \
	done
	fg && fg

sa:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.sa $$bench -d train -t 50 -o results/${DIST}/sa-$$bench.jsonl & \
	done
	fg && fg

psoc:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.psoc $$bench -d train -t 50 -o results/${DIST}/psoc-$$bench.jsonl & \
	done
	fg && fg


psow:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.psow $$bench -d train -t 50 -o results/${DIST}/psow-$$bench.jsonl & \
	done
	fg && fg


ffrcpso:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.ffrcpso $$bench -d train -t 50 -o results/${DIST}/ffrcpso-$$bench.jsonl & \
	done
	fg && fg

ffrwpso:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.ffrwpso $$bench -d train -t 50 -o results/${DIST}/ffrwpso-$$bench.jsonl & \
	done
	fg && fg


ffrwcmaes:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.ffrwcmaes $$bench -d train -t 50 -o results/${DIST}/ffrwcmaes-$$bench.jsonl & \
	done
	fg && fg

ffrwde:
	mkdir -p results/$(DIST)/
	for bench in nguyen4 nguyen7 nguyen8 nguyen10 keijzer4 keijzer11 keijzer12 ; do \
					python -m experiments.ffrwde $$bench -d train -t 50 -o results/${DIST}/ffrwde-$$bench.jsonl & \
	done
	fg && fg

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


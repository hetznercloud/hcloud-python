SHELL := bash
.PHONY: test coverage docs clean

venv:
	python3 -m venv venv
	venv/bin/pip install -e .[docs,test]

test: venv
	venv/bin/pytest -v

coverage: venv
	venv/bin/coverage run -m pytest -v
	venv/bin/coverage report --show-missing
	venv/bin/coverage html
	xdg-open htmlcov/index.html

export SPHINXBUILD=../venv/bin/sphinx-build
docs: venv
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	xdg-open docs/_build/html/index.html

docs-dev: venv docs
	venv/bin/watchmedo shell-command \
		--patterns="*.py;*.rst;*.md" \
		--ignore-pattern=".git/*" \
		--recursive \
		--drop \
		--command="$(MAKE) -C docs html" \
		.

clean:
	git clean -xdf

clean:
	black lambchop && isort lambchop && autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive lambchop

build:
	python setup.py sdist --formats=gztar,zip

publish:
	twine upload dist/* --verbose
	
cleanup:
	rm -rf build dist .egg lambchop.egg-info

build-publish: build publish cleanup
PKGNAME=delaunayextrapolation
all: $(OBJ) README.md
	echo Done.

test-deploy: build
	twine upload -r pypitest dist/*
test-install:
	pip install --index-url https://test.pypi.org/simple/ $(PKGNAME)


install:
	./setup.py install
uninstall:
	-pip uninstall -y delaunayextrapolation
build: README.md
	./setup.py sdist bdist_wheel


deploy: build
	twine upload --repository pypi dist/*
check:
	./setup.py check


clean:
	-rm $(ALL) *.so *~ */*~ *.o *.gro *.rdf
	-rm -rf build dist
	-rm -rf PairList.egg-info

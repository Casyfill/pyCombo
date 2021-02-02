test:
	poetry install
	poetry run pytest tests/  --log-level DEBUG


install_git:
	pip install git+https://github.com/Casyfill/pyCombo.git@pybind11

install_tarball:
	python -m pip install https://github.com/Casyfill/pyCombo/archive/943f786c25daf3bdd22e95c5b059516666e3cdb6.tar.gz

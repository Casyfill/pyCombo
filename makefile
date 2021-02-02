test:
	poetry install
	poetry run pytest tests/  --log-level DEBUG


install_git:
	pip install git+https://github.com/Casyfill/pyCombo.git@pybind11

install_tarball:
	python -m pip install https://github.com/Casyfill/pyCombo/archive/c09dbe078d93a6abc3fa3027916092ccac17c4ab.tar.gz

PYTHON_BIN=$(shell which python3.8 )
SHELLCHECK := $(shell if [ -f "/bin/zsh" ]; then echo /bin/zsh; else echo /bin/bash; fi)
SHELL := $(SHELLCHECK)
VENV_DIR := venv


env:
	${PYTHON_BIN} -m venv ./venv
	${PYTHON_BIN} -m pip install --upgrade pip
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt
	${PYTHON_BIN} src/download_file.py


add-pkg: $(VENV_DIR)/bin/activate
ifndef package
	$(error Debes proporcionar el nombre del paquete usando 'package=<nombre_del_paquete>')
endif
ifndef version
	$(error Debes proporcionar la versión del paquete usando 'version=<version_del_paquete>')
endif
	. $(VENV_DIR)/bin/activate && pip install $(package)==$(version) && pip freeze > requirements.txt

pyspy: $(VENV_DIR)/bin/activate
ifndef file
	$(error Debes proporciar el nombre del programa en python a ejecutar con py-spy usando 'file=<nombre_del_programa>' )
endif
	sudo py-spy top -S $(PYTHON_BIN) src/q1_memory.py

memprofile:
ifndef file
	$(error Debes proporciar el nombre del programa en python a ejecutar con memory_profiler usando 'file=<nombre_del_programa>' )
endif
	rm -f output/$(file).dat
	. $(VENV_DIR)/bin/activate && mprof run --output output/$(file).dat $(PYTHON_BIN) src/$(file).py
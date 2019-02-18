RM = rm -rf

TUTORIAL_GRPC_DB_PORT ?= 5432
TUTORIAL_GRPC_GRAPHITE_PORT ?= 81

# all: docker-build

protos:
	@ python setup.py build_proto_modules

wheel:
	@echo "Building python project..."
	@python setup.py build_ext --inplace --force
	@python setup.py bdist_wheel

sdist:
	@echo "Building python project..."
	@python setup.py sdist

pip-install-edit-mode:
	@pip install -e .

launch-search-server:
	search_server

launch-search-client:
	@python src/tutorial/grpc/geodatas/search_client.py --request_position_latlng 42 50 --m

up:
	@TUTORIAL_GRPC_DB_PORT=$(TUTORIAL_GRPC_DB_PORT) TUTORIAL_GRPC_GRAPHITE_PORT=$(TUTORIAL_GRPC_GRAPHITE_PORT) docker-compose up

re: fclean all

fclean:
	# https://stackoverflow.com/questions/10722723/find-exec-echo-missing-argument-to-exec
	# @find src/tutorial/grpc/geodatas/proto/ ! -name '__init__.py' ! -name '*.proto' -name '*.py' -type f -exec rm '{}' \;
	@find . -name "*.pyc" -exec git rm --cached {} \;
	# @$(RM) ./src/crawlertv/__pycache__
	# @$(RM) ./src/crawlertv/protos/__pycache__
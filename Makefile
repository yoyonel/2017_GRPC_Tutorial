RM = rm -rf

TUTORIAL_GRPC_PG_PORT ?= 5432
TUTORIAL_GRPC_GRAPHITE_PORT ?= 81

# all: docker-build

protos:
	@python setup.py build_proto_modules

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
	@TUTORIAL_GRPC_PG_PORT=$(TUTORIAL_GRPC_PG_PORT) \
	TUTORIAL_GRPC_GRAPHITE_PORT=$(TUTORIAL_GRPC_GRAPHITE_PORT) \
	docker-compose up

07b7c9a2-d1e2-4da6-9f20-01a7b72d4b12:
    # https://superuser.com/questions/283481/how-do-i-properly-set-wget-to-download-only-new-files/848558
	@wget -c -N \
		https://www.data.gouv.fr/fr/datasets/r/07b7c9a2-d1e2-4da6-9f20-01a7b72d4b12 \
		-O /tmp/07b7c9a2-d1e2-4da6-9f20-01a7b72d4b12

/tmp/communes-20190101.json:
    # https://unix.stackexchange.com/questions/59276/how-to-extract-only-a-specific-folder-from-a-zipped-archive-to-a-given-directory
	@unzip /tmp/07b7c9a2-d1e2-4da6-9f20-01a7b72d4b12 communes-20190101.json -d /tmp/.

ogrgeojson: /tmp/communes-20190101.json
	@ogr2ogr \
	    -f "PostgreSQL" \
	    PG:"host=localhost dbname=test user=docker password=docker port=2345" \
	    "/tmp/communes-20190101.json"

say_hello:
	@echo "Hello World"

re: fclean all

fclean:
	# https://stackoverflow.com/questions/10722723/find-exec-echo-missing-argument-to-exec
	# @find src/tutorial/grpc/geodatas/proto/ ! -name '__init__.py' ! -name '*.proto' -name '*.py' -type f -exec rm '{}' \;
	@find . -name "*.pyc" -exec git rm --cached {} \;
	# @$(RM) ./src/crawlertv/__pycache__
	# @$(RM) ./src/crawlertv/protos/__pycache__
	@find . -type d -name "__pycache__" -exec rm -Rf {} \;
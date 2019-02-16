RM = rm -rf

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

re: fclean all

fclean:
	# https://stackoverflow.com/questions/10722723/find-exec-echo-missing-argument-to-exec
	# @find src/tutorial/grpc/geodatas/proto/ ! -name '__init__.py' ! -name '*.proto' -name '*.py' -type f -exec rm '{}' \;
	@find . -name "*.pyc" -exec git rm --cached {} \;
	# @$(RM) ./src/crawlertv/__pycache__
	# @$(RM) ./src/crawlertv/protos/__pycache__
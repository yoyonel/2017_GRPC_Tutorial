# https://hub.docker.com/r/continuumio/anaconda/
FROM continuumio/anaconda

# make bash default shell
USER root
RUN ln -snf /bin/bash /bin/sh

RUN apt-get update && apt-get install -y \
        jq \
        make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev   \
        libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev          \
        xz-utils tk-dev libffi-dev liblzma-dev python-openssl git && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN conda install -y -q conda-build xlrd xlwt &&\
    conda update -y -q notebook numpy scipy matplotlib ipython && \
    conda clean --all

RUN mkdir /opt/notebooks

# Jupyter notebook
RUN /opt/conda/bin/conda install jupyter -y --quiet

# RISE: Live Reveal
# https://github.com/damianavila/RISE
RUN conda install -c conda-forge rise

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents
# kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

RUN curl https://pyenv.run | bash

ENV HOME  /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN git clone -b 0.1.2 \
        https://github.com/yoyonel/2017_GRPC_Tutorial.git \
        /opt/notebooks/2017_GRPC_Tutorial

WORKDIR /opt/notebooks/2017_GRPC_Tutorial

RUN pip install pipenv

RUN PIPENV_YES=1 pipenv install

RUN pipenv run pip install . && \
    pipenv run pip install ipykernel && \
    pipenv run python -m ipykernel install --user --name=2017_GRPC_Tutorial

# https://stackoverflow.com/questions/33159518/collapse-cell-in-jupyter-notebook
RUN pip install hide_code                       && \
    jupyter nbextension install --py hide_code  && \
    jupyter nbextension enable --py hide_code   && \
    jupyter serverextension enable --py hide_code

RUN pipenv run pip install geopandas matplotlib descartes

RUN rm -rf /opt/notebooks/2017_GRPC_Tutorial

EXPOSE 8888
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--notebook-dir=/opt/notebooks"]

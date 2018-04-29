# https://github.com/frol/docker-alpine-miniconda3/blob/master/Dockerfile
FROM frolvlad/alpine-glibc:alpine-3.7

ENV CONDA_DIR="/opt/conda"
ENV PATH="$CONDA_DIR/bin:$PATH"

# Install conda
RUN CONDA_VERSION="4.3.14" && \
    CONDA_MD5_CHECKSUM="fc6fc37479e3e3fcf3f9ba52cae98991" && \
    \
    apk add --no-cache --virtual=.build-dependencies wget ca-certificates bash && \
    \
    mkdir -p "$CONDA_DIR" && \
    wget "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh" -O miniconda.sh && \
    echo "$CONDA_MD5_CHECKSUM  miniconda.sh" | md5sum -c && \
    bash miniconda.sh -f -b -p "$CONDA_DIR" && \
    echo "export PATH=$CONDA_DIR/bin:\$PATH" > /etc/profile.d/conda.sh && \
    rm miniconda.sh && \
    \
    conda update --all --yes && \
    conda config --set auto_update_conda False && \
    rm -r "$CONDA_DIR/pkgs/" && \
    \
    apk del --purge .build-dependencies && \
    \
    mkdir -p "$CONDA_DIR/locks" && \
    chmod 777 "$CONDA_DIR/locks"
# everything in one is bad idea ... just for notes
RUN pip install pip -U
RUN pip install pandas
RUN pip install argh
RUN pip install sklearn
# https://github.com/Nexosis/alpine-xgboost
RUN apk add --update --no-cache \
    --virtual=.build-dependencies \
    make gfortran \
    python3-dev \
    py-setuptools g++ && \
    apk add --no-cache openblas lapack-dev libexecinfo-dev libstdc++ libgomp && \
    pip install xgboost --no-build-isolation && \
    apk del .build-dependencies
RUN pip install tensorflow
RUN pip install catboost
RUN pip install lightgbm
RUN pip install pytorch
RUN pip install pyro

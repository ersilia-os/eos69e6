FROM bentoml/model-server:0.11.0-py38
MAINTAINER ersilia

RUN conda install -c conda-forge libstdcxx-ng
RUN python -m pip install torch==1.12.1+cpu torchvision==0.13.1+cpu torchaudio==0.12.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu
RUN python -m pip install fairseq==0.10.2
RUN python -m pip install einops==0.6.0
RUN python -m pip install tqdm==4.66.2
RUN python -m pip install rdkit==2022.09.1
RUN python -m pip install pandas==2.0.3
RUN conda install -y -c dglteam dgl=0.9.1
RUN conda install -y -c conda-forge numpy==1.19.5

WORKDIR /repo
COPY . /repo

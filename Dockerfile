FROM bentoml/model-server:0.11.0-py38
MAINTAINER ersilia

RUN python -m pip install torch==1.12.1+cpu torchvision==0.13.1+cpu torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/
RUN python -m pip install fairseq==0.10.2
RUN python -m pip install einops==0.6.0
RUN python -m pip install tqdm==4.66.2
RUN python -m pip install rdkit==2022.09.1
RUN python -m pip install pandas==2.0.3
RUN python -m pip install numpy==1.22.4
RUN conda install -c dglteam dgl=0.9.1

WORKDIR /repo
COPY . /repo

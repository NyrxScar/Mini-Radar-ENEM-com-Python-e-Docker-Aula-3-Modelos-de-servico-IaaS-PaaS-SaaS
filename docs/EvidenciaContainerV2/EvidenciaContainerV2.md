(venv) PS C:\Users\nyrx_farias\Downloads\Mini-Radar-ENEM-com-Python-e-Docker-Aula-3-Modelos-de-servico-IaaS-PaaS-SaaS> docker build -t radar-enem:v2 .
[+] Building 2.1s (11/11) FINISHED                                                                    docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                  0.0s
 => => transferring dockerfile: 240B                                                                                  0.0s 
 => [internal] load metadata for docker.io/library/python:3.13-slim                                                   1.4s 
 => [auth] library/python:pull token for registry-1.docker.io                                                         0.0s
 => [internal] load .dockerignore                                                                                     0.0s
 => => transferring context: 2B                                                                                       0.0s 
 => [1/5] FROM docker.io/library/python:3.13-slim@sha256:ffb752e139c0a19692a43af8d8523b274222dd68eebad5d583b45c2201c  0.1s 
 => => resolve docker.io/library/python:3.13-slim@sha256:ffb752e139c0a19692a43af8d8523b274222dd68eebad5d583b45c2201c  0.1s 
 => [internal] load build context                                                                                     0.0s 
 => => transferring context: 935B                                                                                     0.0s 
 => CACHED [2/5] WORKDIR /app                                                                                         0.0s 
 => CACHED [3/5] COPY requirements.txt .                                                                              0.0s 
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt                                                   0.0s 
 => [5/5] COPY app.py .                                                                                               0.0s 
 => exporting to image                                                                                                0.4s
 => => exporting layers                                                                                               0.1s 
 => => exporting manifest sha256:508fa7fc315ec5226aade5f5e4c25206d2044d67013a3206fb7231f28aa06a24                     0.0s
 => => exporting config sha256:3f8ecaadd1bb3b62d56204b7c6264e32cf2fe543340fda13472502113c2a7369                       0.0s 
 => => exporting attestation manifest sha256:62ac1a1bba0e2620c37092a1938e2067b4475bcb6a5ed474a4eac45c28bcaacb         0.0s 
 => => exporting manifest list sha256:b8bc266e4a2784c7cc28703bfea8f3cdf3a13bd5d4c879e853cc044609dcb6ad                0.0s 
 => => naming to docker.io/library/radar-enem:v2                                                                      0.0s
 => => unpacking to docker.io/library/radar-enem:v2                                                                   0.0s 
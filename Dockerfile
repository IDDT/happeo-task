# syntax=docker/dockerfile:1.2


# build
FROM python:3.11.1-slim-bullseye AS build
RUN apt update && apt install -y build-essential curl
WORKDIR /build
COPY requirements.txt .
RUN pip3 wheel \
  --wheel-dir=/wheels \
  -r requirements.txt
WORKDIR /temp
RUN curl -sLo model.gguf \
  "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf?download=true"


# prod
FROM python:3.11.1-slim-bullseye AS prod
WORKDIR /app
COPY . .
COPY --from=build /temp temp/
COPY --from=build /wheels /wheels
RUN pip3 install \
  --no-index \
  --no-cache-dir \
  --find-links=/wheels \
  -r requirements.txt
EXPOSE 5000/tcp
ENV FLASK_APP=src
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]

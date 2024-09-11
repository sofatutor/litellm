ARG LITELLM_BUILD_IMAGE=python:3.11.8-slim
ARG LITELLM_RUNTIME_IMAGE=python:3.11.8-slim

FROM $LITELLM_BUILD_IMAGE as builder

WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apt,id=litellm_apt \
    apt-get update && \
    apt-get install -y gcc python3-dev

RUN --mount=type=cache,target=/root/.cache/pip,id=litellm_pip \
    pip install --upgrade pip build

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip,id=litellm_pip \
    pip wheel --no-cache-dir --wheel-dir=/wheels/ -r requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip,id=litellm_pip \
    pip install redisvl==0.0.7 --no-deps

RUN pip uninstall jwt PyJWT -y && \
    pip install PyJWT --no-cache-dir

COPY . .

RUN chmod +x build_admin_ui.sh && ./build_admin_ui.sh

RUN rm -rf dist/* && python -m build

RUN --mount=type=cache,target=/root/.cache/pip,id=litellm_pip \
    pip install dist/*.whl

FROM $LITELLM_RUNTIME_IMAGE as runtime

WORKDIR /app

COPY --from=builder /wheels/ /wheels/
COPY --from=builder /app/dist/*.whl .

RUN --mount=type=cache,target=/root/.cache/pip,id=litellm_pip \
    pip install *.whl /wheels/* --no-index --find-links=/wheels/ && \
    rm -f *.whl && \
    rm -rf /wheels

COPY . .

RUN prisma generate

RUN chmod +x entrypoint.sh

EXPOSE 4000/tcp

ENTRYPOINT ["litellm"]

CMD ["--port", "4000"]

# DOCKER_BUILDKIT=1 docker build -t app:latest .
FROM python:3.13-slim-bookworm AS base
COPY --from=ghcr.io/astral-sh/uv:0.7 /uv /uvx /bin/


FROM base AS builder
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY uv.lock pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev


FROM base AS runtime
WORKDIR /app
ENV USER=app
RUN adduser --gecos "" --disabled-password --shell /sbin/nologin ${USER} \
    && chown ${USER}:${USER} ./

COPY --chown=root:root --chmod=644 ./infra/app/locale.gen /etc/locale.gen
# Packages needed:
    # locales (and locale-gen): App dependency
    # sudo curl nano iputils-ping htop: For debug
RUN apt update \
    && apt install -y --no-install-recommends locales sudo curl nano iputils-ping iproute2 htop \
    && locale-gen

USER ${USER}

COPY --from=builder /app/.venv/ ./.venv/
COPY --chown=${USER}:${USER} . .

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="./src/"
ENV PYTHONUNBUFFERED=1

HEALTHCHECK CMD curl --fail http://localhost:8000/-/health

EXPOSE 8000
# CMD ["fastapi", "run", "src/main.py", "--port", "8000"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# If running behind a proxy like Nginx or Traefik add --proxy-headers
# https://fastapi.tiangolo.com/pt/deployment/docker/#por-tras-de-um-proxy-de-terminacao-tls
# CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

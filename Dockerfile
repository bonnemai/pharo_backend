FROM public.ecr.aws/lambda/python:3.12 AS builder
WORKDIR /app

COPY pyproject.toml README.md ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir '.[test]'

COPY app ./app
COPY tests ./tests
RUN ruff check
RUN pyrefly check
RUN pytest

FROM public.ecr.aws/lambda/python:3.12
WORKDIR ${LAMBDA_TASK_ROOT}

ARG BUILD_DATE
ENV BUILD_DATE=${BUILD_DATE}

COPY pyproject.toml README.md ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir .

COPY app ./app

CMD ["app.main.handler"]

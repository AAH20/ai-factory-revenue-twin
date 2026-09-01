FROM python:3.12-slim
WORKDIR /app
RUN useradd --system --uid 10001 aifactory
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY examples ./examples
RUN pip install --no-cache-dir .
USER 10001
ENTRYPOINT ["aifactory-twin"]
CMD ["examples/256-gpu-factory.json", "--output", "/tmp/aifactory-output"]

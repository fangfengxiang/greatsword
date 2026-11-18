FROM node:22-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN npm install -g @opencode/cli
WORKDIR /workspace
COPY skills/greatsword/ /workspace/skills/greatsword/
COPY evals/datasets/development.jsonl /workspace/evals/datasets/development.jsonl
COPY evals/opencode/run.py /workspace/evals/opencode/run.py
COPY evals/opencode/select_model.py /workspace/evals/opencode/select_model.py
ENTRYPOINT ["python3", "evals/opencode/run.py"]

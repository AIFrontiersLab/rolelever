# Rolelever

Orchestrate specialized AI agents to execute complex, multi-step tasks with improved accuracy and modularity.

# TextProcessor MVP

A simple FastAPI service that processes text (uppercase, lowercase, reverse).

## Usage

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Demo

```bash
python -c "from main import demo; print(demo())"
```

## Architecture

![Architecture](docs/architecture.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    Client[Client] --> API[FastAPI Service]
    API --> Agent[Agent Module]
    Agent --> Cache[Result Cache]
    Agent --> Logic[Operation Logic]
    Logic --> API
    API --> Client
```

</details>

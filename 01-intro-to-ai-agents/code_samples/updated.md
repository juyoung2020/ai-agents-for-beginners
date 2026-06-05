# Fix Notes — `01-python-agent-framework.ipynb`

## What was wrong

The notebook imported `AzureAIProjectAgentProvider`:

```python
from agent_framework import AzureAIProjectAgentProvider, tool
```

This class **does not exist** in `agent_framework` 1.7.0 (the installed version), so the
cell raised:

```
ImportError: cannot import name 'AzureAIProjectAgentProvider' from 'agent_framework'
```

The downstream code also used the old provider pattern
(`await provider.create_agent(...)`), which is likewise gone in 1.7.0.

## Current (1.7.0) API

- `tool` is still exported at the top level: `from agent_framework import tool`
- The Azure AI Foundry client now lives under `agent_framework.foundry`:
  `from agent_framework.foundry import FoundryChatClient`
- Agents are created from the client with **`client.as_agent(...)`**, which is
  **synchronous** (returns an `Agent`) — it is not awaited.
- `FoundryChatClient` reads `FOUNDRY_PROJECT_ENDPOINT` / `FOUNDRY_MODEL` from the
  environment, but you can also pass `project_endpoint` and `model` explicitly.
- `agent.run(...)` is awaitable and supports `stream=True` for streaming.

## What I changed

### 1. Import cell

Before:

```python
from agent_framework import AzureAIProjectAgentProvider, tool
from azure.identity import AzureCliCredential

provider = AzureAIProjectAgentProvider(credential=AzureCliCredential())
```

After:

```python
from agent_framework import tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

chat_client = FoundryChatClient(
    project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    credential=AzureCliCredential(),
)
```

The endpoint/model are passed explicitly so the existing env var names documented in
the notebook's Setup section (`AZURE_AI_PROJECT_ENDPOINT`,
`AZURE_AI_MODEL_DEPLOYMENT_NAME`) keep working without renaming.

### 2. Create-agent cell

Before:

```python
agent = await provider.create_agent(
    tools=[get_destinations],
    name="TravelAgent",
    instructions=(...),
)
```

After:

```python
agent = chat_client.as_agent(
    tools=[get_destinations],
    name="TravelAgent",
    instructions=(...),
)
```

`as_agent` is synchronous, so the `await` was removed. The `await agent.run(...)` call
below it is unchanged.

### 3. Summary markdown

Updated wording to reference `FoundryChatClient` and `chat_client.as_agent(...)` instead
of the removed `AzureAIProjectAgentProvider`.

### Not changed

The streaming cell `agent.run(..., stream=True)` works as-is on 1.7.0.

## Verification

Imports, client construction, and `as_agent(...)` were verified to succeed against
`agent_framework` 1.7.0 (using a dummy endpoint, no network call). Running the notebook
end-to-end still requires a real Azure AI Foundry project: valid
`AZURE_AI_PROJECT_ENDPOINT` / `AZURE_AI_MODEL_DEPLOYMENT_NAME` and `az login`.

# Environment Fix Log — `02-semantic-kernel.ipynb`

**Date:** 2026-06-05
**Conda env:** `ms_agentic` (`/Users/juyoungjung/miniforge3/envs/ms_agentic`)

## Original Error

```
ModuleNotFoundError: No module named 'semantic_kernel'
```

The `semantic-kernel` package was not installed in the active `ms_agentic` conda
environment. It was also missing from the project's `requirements.txt`.

## Investigation

1. **Conda availability check** — searched both default channels and `conda-forge`:
   ```
   conda search semantic-kernel            -> PackagesNotFoundError
   conda search -c conda-forge semantic-kernel -> not found
   ```
   `semantic-kernel` is **not distributed via conda**, so `pip` is the correct
   install method inside the conda env.

2. **Dependency side effect** — installing `semantic-kernel` via pip downgraded
   `azure-ai-projects` from `2.2.0` -> `1.0.0`, which broke
   `agent-framework-foundry 1.7.0` (requires `azure-ai-projects >=2.1.0,<3.0`).

## Changes Made

| Step | Command | Result |
|------|---------|--------|
| Install Semantic Kernel | `pip install semantic-kernel` | `semantic-kernel 1.43.0` installed |
| Restore Azure projects pkg | `pip install "azure-ai-projects==2.2.0"` | `azure-ai-projects 2.2.0` restored |

### Final package versions
- `semantic-kernel` = **1.43.0**
- `azure-ai-projects` = **2.2.0**

## Verification

All imports used by `02-semantic-kernel.ipynb` resolve successfully:

```python
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import FunctionCallContent, FunctionResultContent, StreamingTextContent
from semantic_kernel.functions import kernel_function
from agent_framework.foundry import FoundryChatClient
# -> All notebook imports OK
```

(The `ExperimentalWarning` messages from `agent_framework` are informational only,
not errors.)

## Remaining (Harmless) Note

`pip check` reports a declared version mismatch:

```
semantic-kernel 1.43.0 has requirement azure-ai-projects~=1.0.0b12,
but you have azure-ai-projects 2.2.0.
```

This constraint only affects Semantic Kernel's **Azure AI Agent** integration,
which **this notebook does not use** — lesson 02 uses `ChatCompletionAgent` +
`OpenAIChatCompletion`. Safe to ignore for this tutorial. Keeping
`azure-ai-projects 2.2.0` preserves compatibility with `agent-framework-foundry`
used elsewhere in the course (e.g. lesson 01).

## Follow-up Suggestion

`semantic-kernel` is missing from the project `requirements.txt` despite being a
dependency of lesson 02. Consider adding it:

```
# Microsoft Agent Framework
agent-framework
a2a-sdk
semantic-kernel   # <- add this
```

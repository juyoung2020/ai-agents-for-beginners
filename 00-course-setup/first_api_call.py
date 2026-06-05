from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "https://ms-tutorial-ai-agents-resource.services.ai.azure.com/api/projects/ms-tutorial-ai-agents"
print (f"PROJECT_ENDPOINT = {PROJECT_ENDPOINT}")
MODEL_DEPLOYMENT_NAME = "gpt-4o"
print (f"MODEL_DEPLOYMENT_NAME = {MODEL_DEPLOYMENT_NAME}")

# Create project and openai clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Run a responses API call
response = openai.responses.create(
    model=MODEL_DEPLOYMENT_NAME,
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")
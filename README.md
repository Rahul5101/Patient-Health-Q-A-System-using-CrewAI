### Patient-Health-Q-A-System-using-CrewAI

An end-to-end Retrieval-Augmented Generation (RAG) based Agentic system for patient reports using crewai, integrated with Langfuse for observability and monitoring


## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/rag_crew/config/agents.yaml` to define your agents
- Modify `src/rag_crew/config/tasks.yaml` to define your tasks
- Modify `src/rag_crew/crew.py`  defing the crew logic
- Modify `src/rag_crew/tools/custom_tools.py`  building the custom tool for the agent  

## Running the Project

To kickstart your crew of AI agents and begin task execution, run app.py file from the root folder of your project:

streamlit run app.py

This command initializes the rag_crew Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Understanding Your Crew

The rag_crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the RagCrew Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

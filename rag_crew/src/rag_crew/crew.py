# rag_crew/src/rag_crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.chat_models import ChatOpenAI
import os
os.environ["CREWAI_TELEMETRY"] = "false"

from rag_crew.src.rag_crew.tools.custom_tool import BM25ChunkRetrieverTool


llm = ChatOpenAI(model="gpt-4", temperature=0.2)


@CrewBase
class RagCrew():
    """RagCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    
 

    @agent
    def content_retriver(self) -> Agent:
        return Agent(
            config=self.agents_config['content_retriver'],
            tools=[BM25ChunkRetrieverTool()],
            verbose=True
        )

    @agent
    def result_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['result_generator'],
            llm=llm,
            verbose=True
        )

  

    @task
    def content_retriver_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_retriver_task'],
            input_keys=["query"]  
        )

    @task
    def result_generator_task(self) -> Task:
        return Task(
            config=self.tasks_config['result_generator_task'],
            context=[self.content_retriver_task()],
        )


    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

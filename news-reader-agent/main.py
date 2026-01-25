import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, agent, task, crew
from tools import count_letters, search_tool, scrape_tool

# 두개써보려고 했는데 오류나서 찾아보니...
# TranslatorCrew와 NewsReaderAgent가 같은 tasks.yaml을 공유하면서 서로 다른 agent를 참조해 충돌이 발생함
# 두개의 tasks.yaml파일로 분리해줘야함

@CrewBase
class TranslatorCrew:
    """TranslatorCrew configuration."""
    tasks_config = "config/translator_tasks.yaml"
    
    @agent
    def translator_agent(self):
        return Agent(
            config=self.agents_config["translator_agent"],
        )
    
    @agent
    def counter_agent(self):
         return Agent(
            config=self.agents_config["counter_agent"],
            tools=[count_letters]
        )
    @task
    def translate_task(self):
        return Task(
            config=self.tasks_config["translate_task"]
        )
    @task
    def retranslate_task(self):
        return Task(
            config=self.tasks_config["retranslate_task"]
        )
    
    @task
    def count_task(self):
        return Task(
            config=self.tasks_config["count_task"]
        )
    
    
    @crew
    def assemble_crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )


TranslatorCrew().assemble_crew().kickoff(inputs={"sentence" : "나는 소망. 그리고 나는 나폴리에서 쳇바퀴타는걸 좋아해"})


@CrewBase
class NewsReaderAgent:
    """NewsReaderAgent configuration."""
    tasks_config = "config/news_tasks.yaml"

    @agent
    def news_hunter_agent(self):
        return Agent(
            config=self.agents_config["news_hunter_agent"],
            tools=[search_tool, scrape_tool],
        )

    @agent
    def summarizer_agent(self):
        return Agent(
            config=self.agents_config["summarizer_agent"],
            tools=[
                scrape_tool,
            ],
        )

    @agent
    def curator_agent(self):
        return Agent(
            config=self.agents_config["curator_agent"],
        )

    @task
    def content_harvesting_task(self):
        return Task(
            config=self.tasks_config["content_harvesting_task"],
        )

    @task
    def summarization_task(self):
        return Task(
            config=self.tasks_config["summarization_task"],
        )

    @task
    def final_report_assembly_task(self):
        return Task(
            config=self.tasks_config["final_report_assembly_task"],
        )

    @crew
    def crew(self):
        return Crew(
            tasks=self.tasks,
            agents=self.agents,
            verbose=True,
        )


result = NewsReaderAgent().crew().kickoff(inputs={"topic": "Cambodia Thailand War."})

for task_output in result.tasks_output:
    print(task_output)
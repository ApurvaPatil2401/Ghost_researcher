import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ResearchCrew:
    def __init__(self):
        # 1. Setup the LLM (Groq) inside the class for reliability
        # Using Llama 3.3 70B for high-quality reasoning
        self.my_llm = LLM(
            model="groq/llama-3.3-70b-versatile", 
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY")
        )

        # 2. Define specialized Agents
        self.researcher = Agent(
            role='Senior Market Researcher',
            goal='Find the latest breakthroughs and data points in {topic} for 2026',
            backstory=(
                'You are a world-class researcher. You excel at finding '
                'high-signal information from reputable sources and identifying '
                'emerging trends before they become mainstream.'
            ),
            llm=self.my_llm,
            allow_delegation=False,
            verbose=True
        )

        self.analyst = Agent(
            role='Chief Industry Analyst',
            goal='Synthesize research into a structured, high-value report on {topic}',
            backstory=(
                'You are a strategic analyst. You take raw data and turn it into '
                'actionable insights. You are known for your ability to find '
                'a "Unique Angle" that others miss.'
            ),
            llm=self.my_llm,
            allow_delegation=True,
            verbose=True
        )

    def run(self, topic):
        # 3. Define the Tasks
        search_task = Task(
            description=(
                f"Identify the top 3 critical trends or breakthroughs in {topic}. "
                "Focus on developments occurring or predicted for 2026. "
                "Provide sources where possible."
            ),
            expected_output="A structured list of 3 key trends with supporting context.",
            agent=self.researcher
        )

        write_task = Task(
            description=(
                "Review the research provided. Write a professional report. "
                "The report must include an Executive Summary, Key Trends, "
                "and a 'Unique Angle' section offering a deep strategic insight."
            ),
            expected_output="A professional 4-paragraph report formatted in Markdown.",
            agent=self.analyst,
            context=[search_task]  # This creates the collaborative handover
        )

        # 4. Orchestrate the Crew
        crew = Crew(
            agents=[self.researcher, self.analyst],
            tasks=[search_task, write_task],
            process=Process.sequential,
            verbose=True
        )

        # kickoff() returns a CrewOutput object
        return crew.kickoff(inputs={'topic': topic})

# Allows for testing the script directly in the terminal
if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found in environment.")
    else:
        crew = ResearchCrew()
        # Test with a sample topic
        print(crew.run("AI Agents in Renewable Energy"))
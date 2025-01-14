import os
from dotenv import load_dotenv
from langchain.chains.summarize.refine_prompts import prompt_template

from tools.tools import get_profile_url_tavily

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor, # This is the runtime of the agent
)
from langchain import hub # This is a way to download pre-made prompts.


def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini"
        # model_name = "gpt-3.5-turbo"  # Used in code but told to use gpt-4o-mini instead
    )
    # template = """given the full name {name_of_person} I want you to get me a link to their Linkedin profile page.
    #             Your answer should contain only a URL"""  # This is an output indicator

    template = """given the full name of {name_of_person} I want to get it me a link to their LinkedIn profile page.
                    The URL can NOT contain the word posts.
                    Your answer should only contain a Linkedin URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",  # Name of tool to be used
            func=get_profile_url_tavily,  # function to run
            description="useful for when you need get the Linkedin Page URL", # Very important as LLM uses this to decide whether to use this tool or not
        )
    ]

    react_prompt = hub.pull("hwchase17/react")  # Harrison Chase CEO LangChain - pulls prompt that he wrote
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    # Invoke the agent
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    # parse the result
    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = lookup(name="Eden Marco Udemy")
    print(linkedin_url)
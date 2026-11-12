from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from prompts import RAG_WORKFLOW_INSTRUCTIONS,SUBAGENT_DELEGATION_INSTRUCTIONS,CHUNK_ANALYST_INSTRUCTIONS
from tools import search_documentation,backend
from langchain.messages import HumanMessage

max_concurrent_analysts =3 

INSTRUCTIONS =(

    RAG_WORKFLOW_INSTRUCTIONS
    + "\n\n"
    + "="*80
    +"\n\n"
    +SUBAGENT_DELEGATION_INSTRUCTIONS.format(max_concurrent_analysts=max_concurrent_analysts)


)


chunk_analyst_subagent = { #says how the subagent is created
    "name": 'chunk-analyst',
    "description":(
        "analyse one retrieved documentation chunk file "
        "Pass the user question and a single file path under  /retrieved."
    ),
    "system_prompt": CHUNK_ANALYST_INSTRUCTIONS #analyszie every chink of the retrieved chinks and then put the aqnalysis in the retrieved folder 

}

model=init_chat_model(model="claude-sonnet-5-5")


agent = create_deep_agent(
    model=model,
    tool=[search_documentation],
    backend=backend,
    system_prompt=INSTRUCTIONS,
    subagents=[chunk_analyst_subagent]



)

Example_query=" what are the attendance policies"

result=agent.invoke(
    {"messages": [HumanMessage(content=Example_query)]}
)

print(result["messages"][-1].content)
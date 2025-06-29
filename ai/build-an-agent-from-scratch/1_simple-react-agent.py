# A simple python script that implements Re-Act (Reasoning and Acting) agent pattern.
# It's a pattern where you implement additional actions that an LLM can take 
# - searching Wikipedia or running calculations for example - and then teach it how to request 
# that those actions are run, then feed their results back into the LLM.
# Read more about it here: https://til.simonwillison.net/llms/python-react-pattern

from textwrap import dedent
import openai
import re
import httpx
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from openai import OpenAI

_ = load_dotenv()

client = OpenAI()

chat_completion = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat.completions.create(model="gpt-4o",temperature=0,messages=self.messages)
        return completion.choices[0].message.content

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()

def calculate(what):
    return eval(what)

def average_dog_weight(name):
    if name in "Scottish Terrier": 
        return("Scottish Terriers average 20 lbs")
    elif name in "Border Collie":
        return("a Border Collies average weight is 37 lbs")
    elif name in "Toy Poodle":
        return("a toy poodles average weight is 7 lbs")
    else:
        return("An average dog weights 50 lbs")

known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}

abot = Agent(prompt)

# -----
# Basic implementation
# We ask LLM about a problem, and we manually execute the action it suggests (assumes we know what it is)
result = abot("How much does a toy poodle weigh?")
print(f"=== Question result:\n", result)
result = average_dog_weight("Toy Poodle")
print(f"=== Func calling result:\n", result)
next_prompt = "Observation: {}".format(result)
print(f"=== Next prompt:\n", next_prompt)
abot(next_prompt)
print(f"=== LLM messages:\n", abot.messages)
# -----



# -----
# Manual implementation, but this time we use tried to ask LLM about a problem that requires multiple calls to the action
abot = Agent(prompt)
question = """I have 2 dogs, a border collie and a scottish terrier. \
What is their combined weight"""
abot(question)
next_prompt = "Observation: {}".format(average_dog_weight("Border Collie"))
print(next_prompt)
abot(next_prompt)
next_prompt = "Observation: {}".format(average_dog_weight("Scottish Terrier"))
print(next_prompt)
abot(next_prompt)
next_prompt = "Observation: {}".format(eval("37 + 20"))
print(next_prompt)
abot(next_prompt)
# -----


# -----
# Automatic implementation
action_re = re.compile('^Action: (\w+): (.*)$') # python regular expression to selection action

def query(question, max_turns=5):
    i = 0
    # Initialize the agent with the default system prompt
    bot = Agent(prompt)

    # The first prompt is the question
    next_prompt = question

    # Loop until we reach the maximum number of turns or the agent outputs an answer
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)

        # Find actions in the result from LLM
        actions = [
            action_re.match(a) 
            for a in result.split('\n') 
            if action_re.match(a)
        ]

        # If there is an action to run
        if actions:
            # Get the action and its input
            action, action_input = actions[0].groups()

            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return

question = """I have 2 dogs, a border collie and a scottish terrier. What is their combined weight?"""

query(question)
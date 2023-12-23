from dotenv import load_dotenv
from openai import OpenAI
from openai.types.beta.assistant_create_params import ToolAssistantToolsFunction

load_dotenv()
client = OpenAI()

image_to_netlist_function: ToolAssistantToolsFunction = {
    "type": "function",
    "function": {
        "name": "Image to netlist",
        "description": "Convert an image of a circuit to a SPICE netlist",
        "parameters": {
            "type": "object",
            "properties": {
                "image_id": {
                    "type": "string",
                    "description": "The image ID user provided",
                },
            },
        },
    },
}

schemdraw_interpreter: ToolAssistantToolsFunction = {
    "type": "function",
    "function": {
        "name": "",
        "description": "",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        }
    },
}

spice_simulator_function: ToolAssistantToolsFunction = {
    "type": "function",
    "function": {
        "name": "SPICE netlist simulator",
        "description": "Simulate a SPICE netlist and return the results",
        "parameters": {
            "type": "object",
            "properties": {
                "netlist": {
                    "type": "string",
                    "description": "The SPICE netlist to simulate",
                },
                "node": {
                    "type": "string",
                    "description": "The node to query the voltage of",
                },
            },
            "required": ["netlist", "node"],
        },
    },
}

assistant = client.beta.assistants.create(
    name="Circuit Solver",
    model="gpt-4-1106-preview",
    instructions="""Read the circuit from either an image, \
a netlist or the user's description \
and solve the circuit's parameters based on the user's question.""",
    tools=[image_to_netlist_function, spice_simulator_function],
)


# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "system",
#             "content": "The user uploaded an image with an ID of 1."
#         },
#         {
#             "role": "user",
#             "content": "I want to simulate this circuit.",
#         },
#         {
#             "role": "tool"
#         },
#         {
#             "role": "assistant",
#             "content": """Sure, here are the nodes:
# * Node 1: connected to R1 and R2
# * Node 2: connected to R2 and R3
#
# What node do you want to query the voltage of, or do you want to analyze a
# specific component?
#             """,
#         },
#         {
#             "role": "user",
#             "content": "I want to query the voltage drop of R1.",
#         },
#         {
#             "role": "tool"
#         },
#         {
#             "role": "assistant",
#             "content": "The voltage drop of R1 is 1.5 V.",
#         },
#     ]
# )


def multiline_input() -> str:
    contents = []
    print(">>>", end=" ")
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        print("...", end=" ")
        contents.append(line)

    return "\n".join(contents)


print(multiline_input())

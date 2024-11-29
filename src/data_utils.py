import importlib
import os
from llama_index.core.tools import FunctionTool


# Function to dynamically load modules and extract functions
def load_functions_from_directory(directory):
    tools = []
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            module_name = filename[:-3]  # Strip .py extension
            module_path = f"{directory.replace('/', '.')}.{module_name}"
            module = importlib.import_module(module_path)
            # print(f"Found Module: {module.__name__}")
            for attr_name in dir(module):
                # print(f"Found Attribute: {attr_name}")
                attr = getattr(module, attr_name)
                if callable(attr):  # Ensure it's a function
                    if attr_name.__contains__("fetch_data"): # skip fetch_data
                        continue
                    tool = FunctionTool.from_defaults(fn=attr)
                    tools.append(tool)
    return tools

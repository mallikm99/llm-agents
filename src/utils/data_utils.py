import importlib
import os
from llama_index.core.tools import FunctionTool


# Function to dynamically load modules and extract functions
def load_functions_from_directory(directory):
    tools = []
    # Resolve the absolute path of the directory
    # directory_path = os.path.abspath(directory)
    # Get the absolute path of the project root (assuming `src` is one level below the root)
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Project root
    directory_path = os.path.join(base_path, directory)  # Absolute path to the directory

    # Debugging: Print resolved directory path
    print(f"Resolved directory path: {directory_path}")

    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    # Get the module base path (e.g., src.functions)
    module_base = directory.replace("/", ".").lstrip(".")

    for filename in os.listdir(directory_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]  # Strip .py extension
            module_path = f"{module_base}.{module_name}"  # Construct the absolute module path

            # module_path = f"{directory.replace('/', '.')}.{module_name}"

            module = importlib.import_module(module_path)
            # print(f"Found Module: {module.__name__}")
            for attr_name in dir(module):
                # print(f"Found Attribute: {attr_name}")
                attr = getattr(module, attr_name)
                if callable(attr) and hasattr(attr, "__name__"):  # Ensure it's a function
                    if attr_name.__contains__("fetch_data"): # skip fetch_data
                        continue
                    tool = FunctionTool.from_defaults(fn=attr)
                    tools.append(tool)
    return tools

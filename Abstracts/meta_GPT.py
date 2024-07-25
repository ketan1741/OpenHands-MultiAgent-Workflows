# Global message pool
message_pool = []

PRODUCT_MANAGER_PROMPT = """The user requirements are:
{requirements}

You are a Product Manager responsible for analyzing these requirements and creating a Product Requirements Document (PRD), which includes User Stories and a Requirement Pool.
"""

ARCHITECT_PROMPT = """The Product Requirements Document (PRD) is:
{prd}

You are an Architect responsible for translating these requirements into system design components, including File Lists, Data Structures, and Interface Definitions.
"""

PROJECT_MANAGER_PROMPT = """The system design components are:
{system_design}

You are a Project Manager responsible for decomposing the project into smaller tasks and assigning them to the appropriate agents (Engineers and QA Engineers).
"""

ENGINEER_PROMPT = """The task assigned to you is:
{task}

You are an Engineer responsible for developing the code as specified in the system design documents.
"""

QA_ENGINEER_PROMPT = """The developed code is:
{code}

You are a QA Engineer responsible for testing the code, performing code reviews, and ensuring it meets quality standards.
"""

def generate_from_llm(prompt: str, data: str) -> str:
    # This function would interface with the LLM to generate the required document or output
    if "Product Manager" in prompt:
        return "Product Requirements Document (PRD) with User Stories and Requirement Pool."
    elif "Architect" in prompt:
        return "System Design with File Lists, Data Structures, and Interface Definitions."
    elif "Project Manager" in prompt:
        return ["Develop module A", "Develop module B", "Test module A", "Test module B"]
    elif "Engineer" in prompt:
        return "Developed code for module."
    elif "QA Engineer" in prompt:
        return "Tested and validated codebase."

def product_manager(requirements: str):
    prd = generate_from_llm(PRODUCT_MANAGER_PROMPT, requirements)
    message_pool.append({"role": "Product Manager", "output": prd})

def architect():
    prd = next((msg["output"] for msg in message_pool if msg["role"] == "Product Manager"), None)
    if prd:
        system_design = generate_from_llm(ARCHITECT_PROMPT, prd)
        message_pool.append({"role": "Architect", "output": system_design})

def project_manager():
    system_design = next((msg["output"] for msg in message_pool if msg["role"] == "Architect"), None)
    if system_design:
        task_distribution = generate_from_llm(PROJECT_MANAGER_PROMPT, system_design)
        message_pool.append({"role": "Project Manager", "output": task_distribution})

def engineer():
    task_distribution = next((msg["output"] for msg in message_pool if msg["role"] == "Project Manager"), None)
    if task_distribution:
        for task in task_distribution:
            if "Develop" in task:
                developed_code = generate_from_llm(ENGINEER_PROMPT, task)
                message_pool.append({"role": "Engineer", "task": task, "output": developed_code})

def qa_engineer():
    developed_codes = [msg for msg in message_pool if msg["role"] == "Engineer"]
    for code in developed_codes:
        qa_result = generate_from_llm(QA_ENGINEER_PROMPT, code["output"])
        message_pool.append({"role": "QA Engineer", "task": code["task"], "output": qa_result})

# Simulate the workflow
user_requirements = "Define User requirements."
product_manager(user_requirements)

while True:
    roles_completed = {msg["role"] for msg in message_pool}
    
    if "Product Manager" not in roles_completed:
        product_manager(user_requirements)
    if "Product Manager" in roles_completed and "Architect" not in roles_completed:
        architect()
    if "Architect" in roles_completed and "Project Manager" not in roles_completed:
        project_manager()
    if "Project Manager" in roles_completed and not any(msg["role"] == "Engineer" for msg in message_pool):
        engineer()
    if any(msg["role"] == "Engineer" for msg in message_pool) and not any(msg["role"] == "QA Engineer" for msg in message_pool):
        qa_engineer()

    # Check if all roles have completed their tasks
    if "QA Engineer" in roles_completed:
        break


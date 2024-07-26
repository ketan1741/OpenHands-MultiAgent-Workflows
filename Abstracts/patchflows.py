'''
This is an example for resolving github issues
Multiple custom workflows can be created using this patchflows workflow
Maybe for OpenDevin each step could be an agent and a custom workflow of multiple agents can be defined
Generated using https://chatgpt.com/g/g-0G4sCAd2y-patchwork-assistant
'''

from typing import List, Dict, Any
import requests

class Step:
    def __init__(self, name: str):
        self.name = name
    
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Each step must implement the run method")

class FetchIssues(Step):
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Running {self.name}")
        repo = data['repo']
        token = data['token']
        issues_url = f"https://api.github.com/repos/{repo}/issues"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(issues_url, headers=headers)
        if response.status_code == 200:
            data['issues'] = response.json()
        else:
            data['issues'] = []
        return data

class AnalyzeIssues(Step):
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Running {self.name}")
        # Perform some analysis to categorize issues
        issues = data['issues']
        data['analyzed_issues'] = [{"number": issue["number"], "title": issue["title"], "body": issue["body"], "type": "bug" if "bug" in issue["labels"] else "feature"} for issue in issues]
        return data

class PreparePrompts(Step):
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Running {self.name}")
        analyzed_issues = data['analyzed_issues']
        prompts = []
        for issue in analyzed_issues:
            if issue["type"] == "bug":
                prompts.append(f"Please provide a solution for the following bug:\nTitle: {issue['title']}\nDescription: {issue['body']}")
            else:
                prompts.append(f"Please suggest a feature implementation for the following request:\nTitle: {issue['title']}\nDescription: {issue['body']}")
        data['prompts'] = prompts
        return data

class CallOpenAI(Step):
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Running {self.name}")
        # Mocked call to an LLM API like OpenAI
        responses = []
        for prompt in data['prompts']:
            responses.append(f"Generated response for prompt: {prompt[:50]}...")  # Mocked response
        data['responses'] = responses
        return data

class CreateComments(Step):
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Running {self.name}")
        repo = data['repo']
        token = data['token']
        responses = data['responses']
        issues = data['analyzed_issues']
        headers = {"Authorization": f"token {token}"}
        for issue, response in zip(issues, responses):
            comment_url = f"https://api.github.com/repos/{repo}/issues/{issue['number']}/comments"
            comment_body = {"body": response}
            requests.post(comment_url, headers=headers, json=comment_body)
        return data

# Patchflow class to manage and run steps
class Patchflow:
    def __init__(self, name: str, steps: List[Step]):
        self.name = name
        self.steps = steps
    
    def run(self, initial_data: Dict[str, Any] = None) -> Dict[str, Any]:
        data = initial_data if initial_data else {}
        print(f"Running patchflow: {self.name}")
        for step in self.steps:
            data = step.run(data)
        return data

# Define the GitHub issue resolving patchflow
github_issue_resolving_steps = [
    FetchIssues(name="fetchIssues"),
    AnalyzeIssues(name="analyzeIssues"),
    PreparePrompts(name="preparePrompts"),
    CallOpenAI(name="callOpenAI"),
    CreateComments(name="createComments"),
]

github_issue_resolving_patchflow = Patchflow(name="github_issue_resolving", steps=github_issue_resolving_steps)

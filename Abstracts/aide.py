'''
Aide’s SOTA multi-agent coding framework. 
[Online]. Available: https://aide.dev/blog/sota-on-swe-bench-lite
'''

class CodeSymbolAgent:
    def __init__(self, symbol, codebase):
        self.symbol = symbol
        self.codebase = codebase
        self.context = None

    def understand_symbol(self):
        self.context = f"Context for {self.symbol} in {self.codebase}"
        print(f"CodeSymbolAgent: Understanding {self.symbol}")
        return self.context

    def provide_insights(self):
        insights = f"Insights and tasks for {self.symbol}"
        print(f"CodeSymbolAgent: Providing insights for {self.symbol}")
        return insights

    def propose_change(self, change_description):
        print(f"CodeSymbolAgent: Proposing change for {self.symbol}: {change_description}")
        return f"Proposed change for {self.symbol}: {change_description}"

    def run_tests(self):
        test_results = f"Test results for changes in {self.symbol}"
        print(f"CodeSymbolAgent: Running tests for {self.symbol}")
        return test_results

    def gather_feedback(self, test_results):
        feedback = f"Feedback from tests: {test_results}"
        print(f"CodeSymbolAgent: Gathering feedback for {self.symbol}")
        return feedback

class DeveloperInLoop:
    def approve_change(self, proposed_change):
        print(f"DeveloperInLoop: Approving change: {proposed_change}")
        if proposed_change:
            return True
        else:
            return False

# Simulate the workflow
codebase = "example_codebase"
# symbols are extracted from abstract syntax trees
symbols = ["function1", "class1", "function2"]

# Initialize agents for each code symbol
agents = [CodeSymbolAgent(symbol, codebase) for symbol in symbols]
developer = DeveloperInLoop()

# Each agent understands their symbol and provides insights
for agent in agents:
    context = agent.understand_symbol()
    insights = agent.provide_insights()

# Propose changes, gather feedback, and run tests
for agent in agents:
    proposed_change = agent.propose_change("Optimize performance")
    if developer.approve_change(proposed_change):
        test_results = agent.run_tests()
        feedback = agent.gather_feedback(test_results)
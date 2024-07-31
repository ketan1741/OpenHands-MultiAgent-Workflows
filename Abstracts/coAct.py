'''
X. Hou, M. Yang, W. Jiao, X. Wang, Z. Tu, and W. X. Zhao, “CoAct: A Global-Local Hierarchy for Autonomous Agent Collaboration,” June 2024, arXiv:2406.13381 [cs]. 
[Online]. Available: http://arxiv.org/abs/2406.13381
'''

class GlobalPlanningAgent:
    def __init__(self, task):
        self.task = task
        self.subtasks = []
        self.current_phase = 0

    def decompose_task(self):
        self.subtasks = [f"Phase {i+1}" for i in range(5)]  # Example decomposition
        print(f"Global Planning Agent: Decomposed task into subtasks: {self.subtasks}")
        return self.subtasks

    def review_and_replan(self, feedback):
        if "Error" in feedback:
            print("Global Planning Agent: Received error feedback, replanning...")
            self.subtasks = [f"Revised Phase {i+1}" for i in range(5)]  # Example replanning
        print(f"Global Planning Agent: Reviewed and modified plan: {self.subtasks}")
        return self.subtasks


class LocalExecutionAgent:
    def __init__(self, subtasks):
        self.subtasks = subtasks
        self.current_phase = 0
        self.feedback = []

    def execute_subtasks(self):
        for phase in self.subtasks:
            result = self.execute_phase(phase)
            self.feedback.append(result)
            if "Error" in result:
                print(f"Local Execution Agent: Error in {phase}. Requesting replanning.")
                break
        return self.feedback

    def execute_phase(self, phase):
        # Example execution with random success or error
        if "Revised" in phase:
            result = f"{phase} executed successfully."
        else:
            result = f"{phase} executed with Error."
        print(f"Local Execution Agent: {result}")
        return result


# Simulate the workflow
task = "Complete a complex project."

# Global Planning Agent decomposes the task into subtasks
global_planner = GlobalPlanningAgent(task)
subtasks = global_planner.decompose_task()

# Local Execution Agent executes the subtasks
local_executor = LocalExecutionAgent(subtasks)
feedback = local_executor.execute_subtasks()

# If there is an error in the feedback, request replanning and execute again
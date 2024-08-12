'''
X. Hou, M. Yang, W. Jiao, X. Wang, Z. Tu, and W. X. Zhao, “CoAct: A Global-Local Hierarchy for Autonomous Agent Collaboration,” June 2024, arXiv:2406.13381 [cs]. 
[Online]. Available: http://arxiv.org/abs/2406.13381
'''

class GlobalPlanningAgent:
    def __init__(self):
        self.phases = []

    def decompose_task(self, task):
        # Decompose the task into phases
        # Example with 3 phases
        self.phases = [f"Phase {i+1}" for i in range(3)]  
        print(f"GlobalPlanningAgent: Decomposed task into phases: {self.phases}")
        return self.phases

    def assign_tasks(self, phases):
        # Assign tasks and subtasks to the local execution agent
        # Each phase usually has 1 subtask but we can have more
        # For example Each phase has 3 subtasks
        tasks = {
            phase: [f"Subtask {phase}.{i+1}" for i in range(3)]  
            for phase in phases
        }
        print(f"GlobalPlanningAgent: Assigned tasks: {tasks}")
        return tasks

    def review_progress(self, feedback):
        # Review progress and decide on replanning if necessary
        if any("Error" in f for f in feedback):
            print(f"GlobalPlanningAgent: Replanning due to error feedback: {feedback}")
            new_phases = self.decompose_task("Replanned task")
            return new_phases
        print(f"GlobalPlanningAgent: Progress satisfactory: {feedback}")
        return None

    def provide_guidance(self, feedback):
        # Provide guidance based on feedback
        guidance = f"Guidance based on feedback: {feedback}"
        print(f"GlobalPlanningAgent: Provided guidance: {guidance}")
        return guidance


class LocalExecutionAgent:
    def __init__(self):
        self.results = []

    def execute_subtask(self, subtask):
        # Simulate subtask execution
        result = f"Execution result for {subtask}"
        print(f"LocalExecutionAgent: Executing subtask: {subtask}")
        # Example of handling execution error
        if "Phase 2" in subtask:
            result += " - Error encountered"
        self.results.append(result)
        return result

    def collect_feedback(self, result):
        # Collect feedback from the execution
        feedback = f"Feedback for {result}"
        print(f"LocalExecutionAgent: Collected feedback: {feedback}")
        return feedback

    def replan_if_necessary(self, feedback, global_agent):
        # Replan if there is an error
        if "Error" in feedback:
            new_phases = global_agent.review_progress(feedback)
            if new_phases:
                return global_agent.assign_tasks(new_phases)
        return None


# Simulate the workflow
global_agent = GlobalPlanningAgent()
local_agent = LocalExecutionAgent()

# Decompose the main task into phases
phases = global_agent.decompose_task("Main task")
tasks = global_agent.assign_tasks(phases)

# Execute tasks and collect feedback
for phase, subtasks in tasks.items():
    # Usually each phase has only 1 subtask, but we can have more
    # This loop can be removed if a phase is a subtask
    for subtask in subtasks:
        result = local_agent.execute_subtask(subtask)
        feedback = local_agent.collect_feedback(result)
        guidance = global_agent.provide_guidance(feedback)
        replanned_tasks = local_agent.replan_if_necessary(feedback, global_agent)
        if replanned_tasks:
            for replanned_phase, replanned_subtasks in replanned_tasks.items():
                for replanned_subtask in replanned_subtasks:
                    result = local_agent.execute_subtask(replanned_subtask)
                    feedback = local_agent.collect_feedback(result)
                    guidance = global_agent.provide_guidance(feedback)

# Final output
print("All tasks and subtasks executed and feedback collected.")
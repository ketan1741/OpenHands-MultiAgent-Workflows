'''
Chatdev: Communicative agents for software development. 
[Online]. Available: https://arxiv.org/abs/2307.07924. 
GitHub: https://github.com/OpenBMB/ChatDev
'''

import re
from abc import ABC, abstractmethod


class ChatEnv():

    def __init__(self, task_prompt: str) -> None:
        self.task_prompt = task_prompt
        
        # maintain the state of the global chat environment for all the phases
        # e.g. intermediate conclusion, code files, etc
        self.env_dict: dict = {}
    

class SimplePhase(ABC):

    def __init__(self, 
                 user_role: str, 
                 assistant_role: str, 
                 phase_prompt: str) -> None:
        self.user_role = user_role # instructor role (I)
        self.assistant_role = assistant_role # assistant role (A)
        self.phase_prmopt = phase_prompt # to initiate and guide the phase towards the goal

        self.phase_env = {}
        self.conclusion = None # the conclusion of the discussion

    def execute(self, chat_env: ChatEnv, max_turn_step: int = 1) -> ChatEnv:
        # 1. Use the global chat env to populate the phase env
        self.update_phase_env(chat_env)
        # 2. Start the chatting between the user agent and assistant agent and save the conclusion
        self.conclusion = self.chatting(chat_env, max_turn_step)
        # 3. Update the global chat env with the phase env and the conclusion
        # of the chatting
        return self.update_chat_env(chat_env)
    
    @abstractmethod
    def update_phase_env(self, chat_env) -> None:
        pass
    
    @abstractmethod
    def update_chat_env(self, chat_env) -> ChatEnv:
        pass
    
    def chatting(self, chat_env: ChatEnv, max_turn_step: int):
        # ... chatting between the user agent and assistant agent
        # within the max_turn_step
        return "The conclusion is ..."


class ComposedPhase(SimplePhase):

    def __init__(self, 
                 cycle_num: str, 
                 phases_list: list[SimplePhase]) -> None:
        # initlize the composed phase with the phase configuration
        # populate the phases list with the phase instances
        self.cycle_num = cycle_num
        self.phases = phases_list
    
    def execute(self, chat_env: ChatEnv) -> ChatEnv:
        # 1. Use the global chat env to populate the phase env
        self.update_phase_env(chat_env)

        # 2. Start the chatting between the user agent and assistant agent
        for _ in range(self.cycle_num):
            for phase in self.phases:
                phase.execute(chat_env)
        
        # 3. Update the global chat env with the phase env and the conclusion
        # of the chatting
        return self.update_chat_env(chat_env)
    

class Design(SimplePhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        pass

    def extract_tag(text: str, tag_name: str) -> str:
        # Define the regex pattern to match the content inside <tag_name>...</tag_name>
        pattern = rf'<{tag_name}>(.*?)</{tag_name}>'
        
        # Find all matches
        return re.findall(pattern, text, re.DOTALL)[0]

    def update_chat_env(self, chat_env) -> ChatEnv:
        if len(self.seminar_conclusion) > 0:
            chat_env.env_dict['modality'] = self.extract_tag(self.conclusion, 'modality')
            chat_env.env_dict['programming_language'] = self.extract_tag(self.conclusion, 'language')
        return chat_env


class CodingWriting(SimplePhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"task": chat_env.env_dict['task_prompt'],
                               "modality": chat_env.env_dict['modality'],
                               "language": chat_env.env_dict['language']})

    def update_chat_env(self, chat_env) -> ChatEnv:
        chat_env.update_code(self.conclusion)
        return chat_env


class CodeComplete(SimplePhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"task": chat_env.env_dict['task_prompt'],
                               "modality": chat_env.env_dict['modality'],
                               "language": chat_env.env_dict['language'],
                               "codes": chat_env.get_codes(),
                               "unimplemented_file": ""})
        # ... read and populate unimplemented_file from the code files

    def update_chat_env(self, chat_env) -> ChatEnv:
        chat_env.update_code(self.conclusion)
        return chat_env


class CodeReviewComment(SimplePhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"task": chat_env.env_dict['task_prompt'],
                               "modality": chat_env.env_dict['modality'],
                               "language": chat_env.env_dict['language'],
                               "codes": chat_env.get_codes()})
        # ... read and populate comments from the code files

    def update_chat_env(self, chat_env) -> ChatEnv:
        chat_env.env_dict['review_comments'] = self.seminar_conclusion
        return chat_env


class CodeReviewModification(SimplePhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"task": chat_env.env_dict['task_prompt'],
                               "modality": chat_env.env_dict['modality'],
                               "language": chat_env.env_dict['language'],
                               "codes": chat_env.get_codes(),
                               "comments": chat_env.env_dict['review_comments']})
    
    def update_chat_env(self, chat_env) -> ChatEnv:
        chat_env.update_codes(self.conclusion)
        return chat_env


##### Usage #####
chat_env = ChatEnv(
    task_prompt="Implement a chatbot for software development. The chatbot should be able to \
        communicate with the user and assist in the software development process."
)
design = Design(user_role="Chief Executive Officer", 
            assistant_role="Chief Technology Officer", 
            phase_prompt="Choose the modality (web, desktop, mobile, cli...) and programming language for the project.")
coding_writing = CodingWriting(user_role="Chief Technology Officer",
                               assistant_role="Programmer", 
                               phase_prompt="Write one or multiple files and make sure that every detail of\
                                   the architecture is, in the end, implemented as code")

code_complete = CodeComplete(user_role="Programmer",
                             assistant_role="Chief Technology Officer",
                             phase_prompt="Complete the class, method unimplemented and make sure that all\
                                    the requirements are met.")
coding_complete_all = ComposedPhase(phases_list=[code_complete],
                                    cycle_num=10)
code_review_comment = CodeReviewComment(user_role="Programmer",
                                        assistant_role="Code Reviewer",
                                        phase_prompt="Review the codes in detail, propose one comment with the highest priority about the codes, and give me instructions on how to fix")
code_review_modification = CodeReviewModification(user_role="Code Reviewer",
                                                assistant_role="Programmer",
                                                phase_prompt="Modify the codes according to the comments given by the reviewer")
code_review_all = ComposedPhase(phases_list=[code_review_comment, code_review_modification],
                                cycle_num=3)
# test = ComposedPhase(phases_list=[test_error_summary, test_error_fix], 
#                                   cycle_num=3])
# environment_setup_doc = EnvironmentSetupDoc(user_role="Chief Technology Officer",
#                                             assistant_role="Programmer",
#                                             phase_prompt="Write a requirements.txt to setup for the project.")
# manual_writing = ManualWriting(user_role="Chief Executive Officer",
#                                assistant_role="Chief Product Officer",
#                                phase_prompt="Write a manual.md file in Markdown to instruct how to use the project.")

chat_env = design.execute(chat_env, max_turn_step=1)
chat_env = coding_writing.execute(chat_env, max_turn_step=1)
chat_env = coding_complete_all.execute(chat_env)
chat_env = code_review_all.execute(chat_env)
# chat_env = test.execute(chat_env)
# chat_env = environment_setup_doc.execute(chat_env)
# chat_env = manual_writing.execute(chat_env)
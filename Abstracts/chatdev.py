from abc import ABC, abstractmethod

class ChatEnv():
    # maintain the state of the global chat environment for all the phases
    # e.g. intermediate conclusion, code files, etc
    pass


class Phase(ABC):
    user_role: str # instructor role (I)
    assistant_role: str # assistant role (A)
    phase_prompt: str # to initiate and guide the phase towards the goal

    def __init__(self, user_role, assistant_role, phase_prompt) -> None:
        self.phase_env = dict()

    def execute(self, chat_env: ChatEnv, max_turn_step: int):
        # 1. Use the global chat env to populate the phase env
        self.update_phase_env(chat_env)
        # 2. Start the chatting between the user agent and assistant agent
        self.chatting(chat_env, max_turn_step)
        # 3. Update the global chat env with the phase env and the conclusion
        # of the chatting
        self.update_chat_env(chat_env)
    
    @abstractmethod
    def update_phase_env(self, chat_env):
        pass
    
    @abstractmethod
    def update_chat_env(self, chat_env) -> ChatEnv:
        pass
    
    def chatting(self, chat_env: ChatEnv, max_turn_step: int):
        # ... chatting between the user agent and assistant agent
        # within the max_turn_step
        return "The conclusion is ..."


class ComposedPhase(ABC):
    # similar interface as Phase
    cycle_num: int
    phases: list[Phase]

    def __init__(self, phase_config: dict) -> None:
        # initlize the composed phase with the phase configuration
        # populate the phases list with the phase instances
        pass
    
    # ... `update_phase_env` and `update_chat_env` methods
    
    def execute(self, chat_env: ChatEnv):
        # 1. Use the global chat env to populate the phase env
        self.update_phase_env(chat_env)

        # 2. Start the chatting between the user agent and assistant agent
        for _ in range(self.cycle_num):
            for phase in self.phases:
                phase.execute(chat_env)
        
        # 3. Update the global chat env with the phase env and the conclusion
        # of the chatting
        self.update_chat_env(chat_env)
    

class ChatChain:
    
    def __init__(self, chain_config: list[dict]) -> None:
        self.chain = chain_config
        self.chat_env = ChatEnv()
    
    def execute_chain(self):
        for phase in self.chain:
            self.execute_phase(phase)
        
    def execute_phase(self, phase: dict):
        if phase["phaseType"] == "SimplePhase":
            phase_instance = Phase(phase["user_role"], phase["assistant_role"], phase["phase_prompt"])
            phase_instance.execute(self.chat_env, phase["max_turn_step"])
        elif phase["phaseType"] == "ComposedPhase":
            # construct the composed phase instance
            composed_phase_instance = ComposedPhase(phase_config=phase)
            composed_phase_instance.execute(self.chat_env)


chat_chain_config = [
    {
        "phase": "Design",
        "phaseType": "SimplePhase",
        "max_turn_step": -1,
    },
    {
        "phase": "CodingWriting",
        "phaseType": "SimplePhase",
        "max_turn_step": 1,
        "need_reflect": "False"
    },
    {
        "phase": "CodeCompleteAll",
        "phaseType": "ComposedPhase",
        "cycleNum": 10, # number of cycles to repeat the phase
        "Composition": [{
            "phase": "CodeComplete",
            "phaseType": "SimplePhase",
            "max_turn_step": 1,
            "need_reflect": "False"
        }]
    },
    {
        "phase": "CodeReview",
        "phaseType": "ComposedPhase",
        "cycleNum": 3,
        "Composition": [{
                "phase": "CodeReviewComment",
                "phaseType": "SimplePhase",
                "max_turn_step": 1,
                "need_reflect": "False"
            },
            {
                "phase": "CodeReviewModification",
                "phaseType": "SimplePhase",
                "max_turn_step": 1,
                "need_reflect": "False"
            }
        ]
    },
    # ... similar for testing phase
]

chat_chain = ChatChain(chat_chain_config)
chat_chain.execute_chain()
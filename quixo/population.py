from dataclasses import dataclass, field


class Population:
    def __init__(self):
        pass


@dataclass
class InitParameters:
    use_grow: bool = field(default=True)
    use_full: bool = field(default=True)
    use_different_depth: bool = field(default=True)


@dataclass
class AgentParameters:
    max_depth: int
    max_branching_factor: int


@dataclass
class PopulationParameters:
    agent_param: AgentParameters
    init_param: InitParameters

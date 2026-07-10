from dataclasses import dataclass


@dataclass(frozen=True)
class RunConfig:
    use_gold_entities: bool = True   # seed anchors from dataset q_entity

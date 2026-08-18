"""W1D4: build two testable prompts for the same product task."""


def build_zero_shot_prompt(requirement: str) -> str:
    """Return a prompt with no worked example.

    The contract must define:
    - the model's role and goal;
    - hard constraints, especially how to handle missing information;
    - the required output sections;
    - observable acceptance criteria.
    """
    # TODO 1: write the zero-shot prompt.
    raise NotImplementedError


def build_few_shot_prompt(requirement: str) -> str:
    """Return the same contract plus one useful input/output example.

    Keep the real requirement visually separate from the example. The example
    should teach a difficult boundary, not merely make the prompt longer.
    """
    # TODO 2: write the few-shot prompt.
    raise NotImplementedError

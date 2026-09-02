"""Pydantic models for the requirement-analysis output.

These models are the single source of truth for today's contract: the prompt,
the parser and the tests all derive from them.

TODO 1: define the three models below.
"""

from pydantic import BaseModel, ConfigDict, Field


class AcceptanceCriterion(BaseModel):
    """One observable condition that proves a task is complete."""

    # TODO 1a: reject unknown fields, and add:
    # - criterion: non-empty string.
    model_config = ConfigDict(extra="forbid")
    criterion: str = Field(..., min_length=1)


class Task(BaseModel):
    """One executable implementation task."""

    # TODO 1b: reject unknown fields, and add:
    # - title: non-empty string;
    # - acceptance_criteria: list[AcceptanceCriterion] with at least one item.
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., min_length=1)
    acceptance_criteria: list[AcceptanceCriterion] = Field(..., min_length=1)


class Requirement(BaseModel):
    """The complete structured response for one user requirement."""

    # TODO 1c: reject unknown fields, and add:
    # - summary: non-empty string;
    # - tasks: list[Task] with at least one item;
    # - open_questions: list[str], optional, defaults to an empty list.
    #
    # open_questions carries the W1D4 rule into the schema: when information is
    # missing the model must ask instead of inventing an API or a threshold.
    model_config = ConfigDict(extra="forbid")
    summary: str = Field(..., min_length=1)
    tasks: list[Task] = Field(..., min_length=1)
    open_questions: list[str] = Field(default_factory=list)

from pydantic import BaseModel, Field


class HtbFeedback(BaseModel):
    """
    Represents the machine rated difficulty.
    """

    counter_bit_hard: int = Field(alias='counterBitHard')
    """A bit hard rate counter."""

    counter_brain_fuck: int = Field(alias='counterBrainFuck')
    """Brainfuck rate counter."""

    counter_cake: int = Field(alias='counterCake')
    """Piece of cake rate counter."""

    counter_easy: int = Field(alias='counterEasy')
    """Easy rate counter."""

    counter_ex_hard: int = Field(alias='counterExHard')
    """Extremely hard rate counter."""

    counter_hard: int = Field(alias='counterHard')
    """Hard rate counter."""

    counter_medium: int = Field(alias='counterMedium')
    """Medium rate counter."""

    counter_too_easy: int = Field(alias='counterTooEasy')
    """Not too easy rate counter."""

    counter_too_hard: int = Field(alias='counterTooHard')
    """Too hard rate counter."""

    counter_very_easy: int = Field(alias='counterVeryEasy')
    """Very easy rate counter."""

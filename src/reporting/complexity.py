from __future__ import annotations

from src.algorithms.backtracking import COMPLEXITY as BACKTRACKING_COMPLEXITY
from src.algorithms.dsatur import COMPLEXITY as DSATUR_COMPLEXITY
from src.algorithms.greedy import COMPLEXITY as GREEDY_COMPLEXITY
from src.algorithms.welsh_powell import COMPLEXITY as WELSH_POWELL_COMPLEXITY


def complexity_map() -> dict[str, str]:
    return {
        "Greedy (First-Fit)": GREEDY_COMPLEXITY,
        "DSATUR": DSATUR_COMPLEXITY,
        "Backtracking": BACKTRACKING_COMPLEXITY,
        "Welsh-Powell": WELSH_POWELL_COMPLEXITY,
    }


from typing import List

from lord.database import Slot


def somente_aliados(slots: List[Slot]) -> List[Slot]:
    return [s for s in slots if s.card.is_ally]
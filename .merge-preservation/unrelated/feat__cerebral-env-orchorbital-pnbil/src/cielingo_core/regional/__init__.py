"""cielingo_core.regional — regional and dialectal language variants.

Handles dialect-specific grammar, vocabulary, and phase offsets for
regional variants of Polish and other CIELingo-supported languages.
Stub namespace — extend with regional modules.
"""

__version__ = "0.1.0"
__description__ = "Regional and dialectal language variants"

import logging as _log
try:
    from cielingo_core.regional import (
        en_solver,
        j_kuramoto_holonomy,
        ja_solver,
        pl_grammar,
        pl_solver,
        surface_solution_validator,
        gap_report,
    )
except Exception as exc:
    _log.getLogger(__name__).debug("regional: optional module import failed: %s", exc)

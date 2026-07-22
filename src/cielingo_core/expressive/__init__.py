"""cielingo_core.expressive — expressive and poetic language layers.

Generative and analytic tools for poetic/symbolic language, metaphor
routing, and affective expression over the CIELingo phase surface.
Stub namespace — extend with expressive modules.
"""

__version__ = "0.1.0"
__description__ = "Expressive and poetic language layers"

import logging as _log
try:
    from cielingo_core.expressive import expressive_codecs, style_renderer
    from cielingo_core.expressive import gap_report
except Exception as exc:
    _log.getLogger(__name__).debug("expressive: optional module import failed: %s", exc)

"""cielingo_core.architecture — system architecture definitions and topologies.

Describes the CIEL/NOEMA/CIELingo component graph, data-flow contracts,
and subsystem wiring.  Stub namespace — extend with architecture
diagrams, dependency specs, and routing tables.
"""

__version__ = "0.1.0"
__description__ = "System architecture definitions and component topologies"

import logging as _log
try:
    from cielingo_core.architecture import gap_report
except Exception as exc:
    _log.getLogger(__name__).debug("architecture: optional module import failed: %s", exc)

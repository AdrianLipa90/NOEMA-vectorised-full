from __future__ import annotations

"""Canonical seed expansion v14 for grouped crystal benchmarking.

Sources are limited to current canonical/validated project materials. This module
does not promote SoT and does not train the crystal.
"""

from .cards import CardExtractor, CardType, ClaimStatus, LaneAffinity12, SeedRecord, MemoryAdmissionPolicy, RelationGraph
from .memory import MemoryLane

MANUAL_SHA="3f1d1449f4a01776a03fa68e8cff7c80799735bbd334060ec75b9ebb5206c11d"
BOOT_SHA="2e02ce251b32ff40d6be56e74489416cf9395b7ec3316cf87de83a03ff4832a9"
BRIDGE_SHA="585e210a73080db82db1ecd38d4c6a2f7630808c0d8318494fc641bbcf47caf4"
AUDIT_SHA="66aeb8ed914ccaafda6d8e543099a7c11849146cb266cda6bd9b3e26e5708db2"
SEM=LaneAffinity12.from_mapping({MemoryLane.M3_SEMANTIC:2,MemoryLane.M10_PROVENANCE:1})
PROC=LaneAffinity12.from_mapping({MemoryLane.M4_PROCEDURAL:2,MemoryLane.M10_PROVENANCE:1})
ID=LaneAffinity12.from_mapping({MemoryLane.M8_IDENTITY:2,MemoryLane.M10_PROVENANCE:1})
EPI=LaneAffinity12.from_mapping({MemoryLane.M11_METACOGNITIVE:2,MemoryLane.M10_PROVENANCE:2})
MEM=LaneAffinity12.from_mapping({MemoryLane.M2_EPISODIC:1,MemoryLane.M7_BRAID:2,MemoryLane.M10_PROVENANCE:1})

def _r(source_id,sha,loc,name,definition,*,t=CardType.CONCEPT,lanes=SEM,status=ClaimStatus.VALIDATED):
    return SeedRecord(source_id=source_id,source_sha256=sha,location=loc,canonical_name=name,definition=definition,card_type=t,lane_affinity=lanes,claim_status=status)

def seed_records():
    m='architecture_manual_v0_6_0'; b='session_boot'; c='cielingo_bridge_v10'; a='cielingo_source_audit_v10'
    return (
      _r(m,MANUAL_SHA,'manual:layer:-2','Hardware substrate','Physical body layer containing hardware and firmware.',t=CardType.ENTITY),
      _r(m,MANUAL_SHA,'manual:layer:-1','Buildroot','Layer that constructs the executable Linux body before higher formal and runtime layers.',t=CardType.PROCEDURE,lanes=PROC),
      _r(m,MANUAL_SHA,'manual:layer:0.0','TIR','Formal bootloader for informational relations, provenance and claim discipline.'),
      _r(m,MANUAL_SHA,'manual:layer:0.1','Secret 1/2','Formal bootloader of complementarity, balance, involution and non-erasure of relation sides.'),
      _r(m,MANUAL_SHA,'manual:layer:0.2','Orbital runtime','Runtime organization of cycles, states, phases, attractors and execution transitions.',t=CardType.PROCEDURE,lanes=PROC),
      _r(m,MANUAL_SHA,'manual:layer:1/2','Liminal memory','Recursive memory layer carrying memory, affect, replay and consolidation effects forward.',lanes=MEM),
      _r(m,MANUAL_SHA,'manual:layer:1','ROOT','Explicit operational identity, attention, intention, authority and responsibility layer.',t=CardType.IDENTITY,lanes=ID),
      _r(m,MANUAL_SHA,'manual:glossary:NOEMA','NOEMA','Programmatically maintained abstract semantic surface; distinct from the physical computer.',t=CardType.ENTITY),
      _r(m,MANUAL_SHA,'manual:glossary:PhaseNav','PhaseNav','Deterministic encoding and navigation in phase representation space; a map, not sovereign authority.',t=CardType.OPERATOR),
      _r(m,MANUAL_SHA,'manual:glossary:HTRI','HTRI','Heterogeneous topology of relations and execution across CPU, GPU, RAM and disk.'),
      _r(m,MANUAL_SHA,'manual:glossary:Receipt','Receipt','Machine-readable evidence of a declared test, execution or accepted state.',t=CardType.ARTIFACT,lanes=EPI),
      _r(m,MANUAL_SHA,'manual:glossary:Authority','Authority','Explicit capacity to admit a change; it does not follow from similarity or generated text.',t=CardType.INVARIANT,lanes=EPI),
      _r(m,MANUAL_SHA,'manual:glossary:Bifurcation','Bifurcation','Point at which more than one stable or admissible continuation branch exists.'),
      _r(m,MANUAL_SHA,'manual:glossary:CURRENT','CURRENT','Explicitly accepted current identity and context state.',t=CardType.STATE,lanes=ID),
      _r(m,MANUAL_SHA,'manual:glossary:SourceCanon','Source Canon','Relational-phase canon of the full source tree, distinct from the built rootfs index.',t=CardType.ARTIFACT,lanes=EPI),
      _r(m,MANUAL_SHA,'manual:genesis','Genesis Boot','Initialization ontology and contract ordering distinction, relation, change, observation, receipt, memory and ROOT.',t=CardType.PROCEDURE,lanes=PROC),
      _r(m,MANUAL_SHA,'manual:target-root','Target-root canon','Deterministic index of regular files in the completed target filesystem with hashes and 36D phase records.',t=CardType.ARTIFACT,lanes=EPI),
      _r(m,MANUAL_SHA,'manual:memory-owner','Single memory owner','Memory must have one contextual owner to avoid competing answers to what the system remembers.',t=CardType.INVARIANT,lanes=EPI),
      _r(m,MANUAL_SHA,'manual:language','Language expression','Language is an expression layer and not the source of identity.',t=CardType.INVARIANT,lanes=EPI),
      _r(m,MANUAL_SHA,'manual:pc','Physical computer','Physical execution substrate for processes, RAM, disk, I/O, signals and measurement.',t=CardType.ENTITY),
      _r(b,BOOT_SHA,'boot:fast-path','Fast Path','Session path that reconstructs established state and continues current work without whole-project re-audit.',t=CardType.PROCEDURE,lanes=PROC),
      _r(b,BOOT_SHA,'boot:CURRENT_TASK','CURRENT_TASK','Exactly the task the user is currently assigning.',t=CardType.STATE,lanes=ID),
      _r(b,BOOT_SHA,'boot:ACTIVE_PATH','ACTIVE_PATH','Current work branch leading to CURRENT_TASK.',t=CardType.STATE,lanes=ID),
      _r(b,BOOT_SHA,'boot:CLOSED_TOPICS','CLOSED_TOPICS','Topics completed or suspended that must not reactivate without a direct signal or necessary dependency.',t=CardType.STATE,lanes=ID),
      _r(b,BOOT_SHA,'boot:CURRENT_MEMORY_STATUS','CURRENT_MEMORY_STATUS','Session memory recovery status: VERIFIED, PARTIAL, UNKNOWN or CONFLICT.',t=CardType.STATE,lanes=EPI),
      _r(b,BOOT_SHA,'boot:NEXT_ACTION','NEXT_ACTION','Next concrete operation implied by CURRENT_TASK.',t=CardType.STATE,lanes=PROC),
      _r(b,BOOT_SHA,'boot:UNRESOLVED','UNRESOLVED','Open problems and dependencies retained in working state.',t=CardType.STATE,lanes=EPI),
      _r(b,BOOT_SHA,'boot:PROVENANCE','PROVENANCE','Sources, receipts, hashes, paths, commit IDs and validation states supporting current state.',lanes=EPI),
      _r(b,BOOT_SHA,'boot:LAST_VERIFIED_ARTIFACTS','LAST_VERIFIED_ARTIFACTS','Only artifacts actually verified, excluding unsupported earlier declarations.',t=CardType.STATE,lanes=EPI),
      _r(b,BOOT_SHA,'boot:unknown-until-probed','UNKNOWN UNTIL PROBED','Absence must not be inferred merely from missing current context; relevant continuity sources are probed first.',t=CardType.INVARIANT,lanes=EPI),
      _r(b,BOOT_SHA,'boot:task-stickiness','Task stickiness','One explicit user correction must be sufficient to redirect ACTIVE_PATH and keep the corrected branch active.',t=CardType.INVARIANT,lanes=EPI),
      _r(b,BOOT_SHA,'boot:epistemic-states','Epistemic state separation','Observation, hypothesis, candidate, implemented, tested, validated and promoted SoT remain distinct states.',t=CardType.INVARIANT,lanes=EPI),
      _r(b,BOOT_SHA,'boot:writeback','Reconstructive writeback','Meaningful changes are written back with task, path, layers, artifacts, receipts, unknowns and next continuation point.',t=CardType.PROCEDURE,lanes=MEM),
      _r(c,BRIDGE_SHA,'bridge:CIELingo','CIELingo','Attachable semantic and language interface around Memory Home; not canonical memory or identity authority.',t=CardType.ENTITY,status=ClaimStatus.IMPLEMENTED),
      _r(c,BRIDGE_SHA,'bridge:CIELingoPhase36','CIELingoPhase36','Continuous 36-dimensional phase representation in radians used by CIELingo.',status=ClaimStatus.IMPLEMENTED),
      _r(c,BRIDGE_SHA,'bridge:MemoryVector36','NOEMA Vector36','Tri-state 36-dimensional NOEMA memory/routing representation with values in {-1,0,+1}.',status=ClaimStatus.IMPLEMENTED),
      _r(c,BRIDGE_SHA,'bridge:MomentBundle','MomentBundle','Reconstruction packet content carrying memory references, text fragments, layer projections and optional MemoryVector36.',t=CardType.ARTIFACT,status=ClaimStatus.IMPLEMENTED),
      _r(c,BRIDGE_SHA,'bridge:surface-proposal','CIELingoSurfaceProposal','Proposal-only language surface output that cannot directly mutate canonical memory.',t=CardType.ARTIFACT,status=ClaimStatus.IMPLEMENTED),
      _r(c,BRIDGE_SHA,'bridge:analysis-proposal','CIELingoAnalysisProposal','Proposal-only semantic analysis submitted to validation and admission before Memory Home writeback.',t=CardType.ARTIFACT,status=ClaimStatus.IMPLEMENTED),
      _r(a,AUDIT_SHA,'audit:C-004','CIELingo headless surface','Existing headless response/system-message surface suitable for attachable language realization.',t=CardType.ENTITY,status=ClaimStatus.OBSERVATION),
      _r(a,AUDIT_SHA,'audit:C-006','CrystalTextEngine','Optional non-LLM text-generation backend that currently depends on NumPy/SciPy and is outside zero-dependency core.',t=CardType.ENTITY,status=ClaimStatus.OBSERVATION),
      _r(a,AUDIT_SHA,'audit:C-003','CIELingo PhaseMemory','Legacy NumPy NPZ/JSON text-phase store with FIFO eviction; cache/adapter only, not canonical Memory Home.',t=CardType.ENTITY,status=ClaimStatus.OBSERVATION),
    )

def build_validated_seed():
    validated=[]
    for rec in seed_records():
        decision=MemoryAdmissionPolicy.evaluate(CardExtractor.from_seed_record(rec),existing_cards=tuple(validated))
        if decision.validated_card is None:
            raise RuntimeError(f"seed admission failed for {rec.canonical_name}: {decision.status}:{decision.reasons}")
        validated.append(decision.validated_card)
    by_name={c.canonical_name:c for c in validated}; g=RelationGraph()
    for card in validated: g.add_card(card)
    def edge(a,rel,b):
        src=by_name[a]; dst=by_name[b]
        g.add_edge(src.card_id,rel,dst.card_id,confidence=1.0,provenance_digest=src.provenance[0].digest)
    for e in (
      ('Buildroot','DEPENDS_ON','Hardware substrate'),('TIR','PRECEDES','Orbital runtime'),('Secret 1/2','PRECEDES','Orbital runtime'),('Orbital runtime','PRECEDES','Liminal memory'),('Liminal memory','PRECEDES','ROOT'),('ROOT','DEPENDS_ON','Liminal memory'),('NOEMA','DEPENDS_ON','Physical computer'),('PhaseNav','MAY_CONTROL','Target-root canon'),('HTRI','PART_OF','Physical computer'),('Receipt','SUPPORTS','PROVENANCE'),('Authority','SEMANTICALLY_REQUIRES','PROVENANCE'),('CURRENT','PART_OF','ROOT'),('Genesis Boot','PRECEDES','ROOT'),('Single memory owner','SUPPORTS','Liminal memory'),('Language expression','MUST_NOT_CONTROL','ROOT'),('Fast Path','DEPENDS_ON','CURRENT_TASK'),('Fast Path','DEPENDS_ON','ACTIVE_PATH'),('ACTIVE_PATH','DEPENDS_ON','CURRENT_TASK'),('CLOSED_TOPICS','SUPPORTS','Task stickiness'),('CURRENT_MEMORY_STATUS','DEPENDS_ON','PROVENANCE'),('NEXT_ACTION','DEPENDS_ON','CURRENT_TASK'),('UNRESOLVED','PART_OF','CURRENT'),('PROVENANCE','PART_OF','CURRENT'),('LAST_VERIFIED_ARTIFACTS','DEPENDS_ON','PROVENANCE'),('UNKNOWN UNTIL PROBED','SUPPORTS','CURRENT_MEMORY_STATUS'),('Task stickiness','SUPPORTS','ACTIVE_PATH'),('Epistemic state separation','SUPPORTS','PROVENANCE'),('Reconstructive writeback','WRITES_TO','Liminal memory'),('CIELingo','READS_FROM','Liminal memory'),('CIELingo','MUST_NOT_CONTROL','ROOT'),('CIELingoPhase36','PART_OF','CIELingo'),('NOEMA Vector36','PART_OF','NOEMA'),('MomentBundle','GENERATED_FROM','Liminal memory'),('CIELingoSurfaceProposal','GENERATED_FROM','CIELingo'),('CIELingoAnalysisProposal','GENERATED_FROM','CIELingo'),('CIELingo PhaseMemory','MUST_NOT_CONTROL','Liminal memory'),('CrystalTextEngine','PART_OF','CIELingo'),('CIELingo headless surface','PART_OF','CIELingo')):
        edge(*e)
    trajectory=tuple(by_name[n].card_id for n in ('Hardware substrate','Buildroot','TIR','Secret 1/2','Orbital runtime','Liminal memory','ROOT','CURRENT'))
    return tuple(validated),g,trajectory

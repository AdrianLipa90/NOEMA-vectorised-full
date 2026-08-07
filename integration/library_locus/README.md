# NOEMA Library Locus

Status: staging / non-canonical until explicit promotion.

This directory establishes the single staging place used before any library cleanup, deduplication, or memory consolidation.

## Invariants

1. No unique source content is deleted.
2. RAW provenance is preserved append-only.
3. Byte-identical duplicates are grouped by SHA-256; SHA equality is the deduplication criterion.
4. One member of each SHA group may be marked `canonical_object`; remaining members are aliases/copies, not discarded evidence.
5. Similar names or semantic similarity are never sufficient for deduplication.
6. Memory consolidation creates derived state above RAW; it never rewrites historical RAW.
7. Promotion out of this staging locus requires an explicit validated manifest/receipt.

## Intended layout

```text
integration/library_locus/
├── README.md
├── raw_refs/
├── duplicates_by_sha/
├── consolidated_memory/
├── manifests/
└── receipts/
```

The subdirectories are logical destinations. They are created only when actual artifacts are written; empty directories are not represented by Git.

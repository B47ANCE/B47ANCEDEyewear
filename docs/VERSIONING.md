# Version inventory

Root VERSION is the only canonical project version. docs/VERSION_POLICY.md is the
authoritative inherited policy; version-inventory.json declares current mirrors,
package selectors, schema/game distinctions and historical evidence.

Current development iteration: 0.11.1-dev.1. Pre-1.0 PATCH corrects the oversized black-cord
ground model to match the crafted retainers' mean width/depth. The three distinct
static ground models were introduced in 0.11.0-dev.1. Existing item IDs, recipes,
loot, durability, save schema, networking and worn appearance remain unchanged.
The prior 0.10.0-dev.1 native head/clothing durability and paid-legacy migration
remain supported; this iteration does not change their untested runtime status.

Source mod.info, README, canonical Workshop texts, current validation/preparation/
API records and RELEASE_STATUS.json are current mirrors. Build reads VERSION and
binds the resulting source/staging/ZIP to its Git commit. Generated output belongs
in dist/current; published0.5 packages and earlier evidence remain historical.
The prepared 0.6.0-dev.1 candidate and provenance are preserved byte-for-byte in
ignored dist/historical/0.6.0-dev.1-prepared with a retention ledger.
No historical proof is relabeled to the current version.

Run python -B scripts/check_versions.py from the project root before/after edits,
and add --release after a current package exists. The check proves only declared
version consistency. All other integrity/authority checks remain separate.
Dedicated G7 PASS is required for stable G8. The labelled MP testing build can be
distributed before G7 only by an explicit publish request after other preflight gates.

The actual published 0.9 ZIP/checksum/provenance moved unchanged to
dist/historical/0.9.0-dev.1-published with verified hashes and a preservation ledger.
The published 0.10 ZIP/checksum/provenance are preserved byte-for-byte in
dist/historical/0.10.0-dev.1-published with a preservation ledger.
No current 0.11.1 package exists; release checks defer packaging until separately requested.

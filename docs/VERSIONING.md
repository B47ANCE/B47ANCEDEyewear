# Version inventory

Root VERSION is the only canonical project version. docs/VERSION_POLICY.md is the
authoritative inherited policy; version-inventory.json declares current mirrors,
package selectors, schema/game distinctions and historical evidence.

Current development iteration: 0.10.0-dev.1. Pre-1.0 MINOR adds native head/clothing
durability for all six improvised ties and both crafted retainers, server wear
configuration and actual condition tooltips. The user approved changing the wear
trigger from hidden native knock-off rolls. Direct ties now create linked physical
items; transferring protection requires both items. This pre-1.0 behavior change
and one-time paid-legacy migration are explicit, not a silent compatibility claim.
Native crafted condition stays on the existing 10-point scale. Item links extend
schema1 additively with wearSchema=1/tieId and a scalar tie-side link. Historical
schema2 records stay inactive; neither schema number is the project version.
The rare item, original eyewear IDs and recipes remain supported. Saved-world
downgrade is not validated; older packages lack the new three tie types.

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
No current 0.10 package exists; release checks defer packaging until separately requested.

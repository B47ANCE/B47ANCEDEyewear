# Cleanup and Workshop preparation

Project Version: 0.15.0-dev.1

## Crafted-retainer tape — 0.15

Crafted cloth/leather retainers now accept ONE tape in their main-inventory
right-click menu, worn or unworn. Default native wear-resistance bonus is +1 for
adhesive/+2 for duct tape. Condition, maximum, identity and worn mapping stay
unchanged; no recraft is required. Server intent validation, observed-payment
rollback boundaries, persistence, settings and runtime gates are detailed in
CRAFTED_RETAINER_TAPE.md. Unbreakable retainers are excluded. This is source-only;
current G7 NOT TESTED / BLOCKED and stable G8 BLOCKED.


## Current 0.14 materials and reinforcement

Fourteen audited materials, same-material strands, adhesive/duct tape, material-
specific installed native condition and zip-tie cutting are implemented in Lua.
See TIE_REINFORCEMENT.md for balance, ownership/payment/replay checks, new item
identity, existing-save policy and current runtime gates. G7 for THIS gameplay
iteration is BLOCKED / NOT TESTED; earlier published acceptance remains historical.
Date: 2026-10-15

Current 0.13.1 fixes native clothing GUID registration and rejects unready tie
visuals before shared publication or equip. See CLOTHING_SYNC_FIX.md for cause,
offline regression and native/MP gates. No artifacts were moved or deleted;
no packaging, deployment, publication or game/server launch was performed.

Earlier 0.11.1 corrects only the black-cord ground mesh size. The authoring
script, derived rare FBX, Blender master/preview/provenance and version records
are updated. Cloth/leather FBX, all textures, original source art, bindings and
gameplay remain unchanged. No artifact move/deletion, package, deployment,
publication or game/server launch is part of this sizing request.

Earlier 0.11.0 adds ground FBX models/textures for the three retainers, native model
bindings, an editable Blender master and an asset integrity validator. Prior
inventory art and gameplay are preserved. The published 0.10 ZIP/checksum/
provenance moved unchanged to dist/historical/0.10.0-dev.1-published; the bounded
preservation ledger verifies all three hashes. Nothing was deleted. This request
does not package, deploy, publish or launch the game/server.

Earlier 0.10 source continuation implements the explicitly approved native head/clothing
wear alternative for all six improvised material ties and both crafted retainers.
Direct ties own native condition through linked clothing items, with paid-legacy
migration and no free reconstruction. Rare-item art/definition remains unchanged.
The published 0.9 ZIP/checksum/provenance were preserved by a bounded move to
dist/historical/0.9.0-dev.1-published, with per-file SHA-256 verification and a
preservation ledger. No deletion, tests/debug grants, Java, game/server launch,
current package, deployment or publication is part of this source request.

Earlier 0.9 source continuation adds a loot-only unbreakable retainer and distinct cloth/
leather inventory art. Generated master images and export hashes are retained;
original black cord artwork/model bytes and prior published packages are unchanged.
No tests, Java, package, deployment or publication are added by this source task.


Earlier 0.8 continuation: add real Lua-only wearable items and ordinary output
recipes by explicit request. No retired tests, Java paths or finite catches are
restored. Item artwork is copied byte-for-byte from the retained original source.
This is source implementation only; packaging/deployment/publication are separate.

Earlier continuation: 0.7.0-dev.1 adds a production crafting recipe by explicit
request. Both inputs are kept during vanilla processing; the existing authoritative
tie transaction validates and consumes one material use. The new recipe replaces
the unsafe retired definition without restoring test/debug code or Java paths.
The cleanup described below remains the historical 0.6.0-dev.1 action record.
Its prepared package, checksum and provenance were preserved with unchanged
hashes and a verified ZIP CRC in ignored dist/historical/0.6.0-dev.1-prepared.
Its retention ledger records the three preserved files; nothing was deleted.

Authorization: remove all testing code, clean repository/code, prepare Workshop.
This authorizes preparation, not publication, live deployment or a game/server launch.

Reversible quarantine removed tests/, native/, obsolete research/audit generation,
the runtime TestKit, finite-retainer action modules and TieGlasses recipe. The
quarantine also preserves 17 older staging snapshots containing TestKit copies.
1678 files were preserved outside the active repository with SHA-256 records;
no permanent artifact deletion was performed. Asset masters, runtime evidence and
immutable published ZIPs were retained. The full ledger and recovery paths are private
local cleanup records, not public repository payload. The previous published 0.5.0
package was reclassified as historical rather than relabeled to this iteration.
Shared .agents/.codex junctions and the pre-existing AGENTS.md change were left intact.

Version decision: pre-1.0 MINOR 0.5.0-dev.1 → 0.6.0-dev.1. Withdraw experimental
finite-retainer action APIs, the unsafe crafting recipe and debugger commands;
retain legacy tie data and explicit Tie/Untie context-menu behavior. Historical
schema-2 data stays read-only and grants no new protection. No synthetic catches,
replacement eyewear, material refunds or Java dependencies are introduced.

Workshop inputs remain WORKSHOP_DESCRIPTION.txt and WORKSHOP_CHANGE_NOTE.txt.
Existing item 3799754736, App ID 108600 and public GitHub identity are preserved.
Build-Workshop.ps1 prepares temporary staging, verifies it before promotion,
archives prior staging outside the active repository, and records version/commit/
source/package provenance. Publish-Workshop.ps1 -PrepareOnly creates a versioned
VDF preserving canonical paragraphs and existing visibility without authentication.
No test suite is required or run by either entry point.

[UNKNOWN / RUNTIME GATE] Functional fixes are source changes, not newly tested
behavior. SP and dedicated MP are NOT TESTED; gameplay G7/G8 remain BLOCKED.
Actual publication requires a separate request and all applicable preflight checks.
Missing dedicated evidence alone permits only labelled MP test distribution, never
G7 PASS or stable G8 approval. Both canonical texts carry the mandatory MP-testing notice.

## Authorized ground-model Workshop distribution

The user subsequently requested 0.11.1-dev.1 publication as a development build
on 2026-10-14. This authorizes packaging and the existing Workshop item upload;
prior source-only statements above describe their original milestones. Run the
production source/version checks, Build-Workshop.ps1, check_versions.py --release
and Publish-Workshop.ps1 preflight against the exact committed source. Generated
publication-0.11.1-dev.1.json records package/text hashes, release commit, exact
commands, SteamCMD/API verification and the Steam desktop restart outcome.
Preserve public visibility, original artwork and prior published provenance.
No game/server launch or local SP deployment is authorized. G7 BLOCKED / NOT
TESTED and stable G8 BLOCKED remain unchanged; distribution is not runtime proof.

## Worn retainer source addition

0.12.0-dev.1 adds original head-attached static clothing meshes through the
existing native worn slot, three new XML definitions and six male/female files.
See WORN_MODELS.md for installed 42.21 source evidence, authoring provenance,
authority/configuration assessment and remaining fit/MP gates. Existing items
resolve current clothing definitions through native ItemVisual.getClothingItem.
No Lua gameplay, persistence, IDs or custom synchronization changed. No package,
deployment, publication or PZ/server launch is part of this source iteration.
Published 0.11.1 ZIP/checksum/provenance were preserved unchanged with hashes,
a preservation ledger and a read-only ZIP CRC check. No artifacts were deleted.

## Authorized worn-model Workshop development distribution

The user subsequently requested 0.12.0-dev.1 publication as a development build
on 2026-10-14. This authorizes packaging and the existing public Workshop item
upload; source-only statements above describe their original milestones. Run
check_versions.py, validate_release.py, Build-Workshop.ps1, check_versions.py
--release and Publish-Workshop.ps1 preflight against the exact committed source.
Generated publication-0.12.0-dev.1.json records source commit, package/text hashes,
exact commands, SteamCMD/API verification and graceful Steam restart outcome.
Preserve prior package/provenance, item identity, visibility and custom artwork.
No game/server launch or local SP deployment. Worn fit/clipping/remote visuals
remain NOT TESTED; G7 BLOCKED / NOT TESTED and stable G8 BLOCKED remain unchanged.

## Improvised-tie worn presentation source addition

0.13.0-dev.1 uses the existing native head-attachment route for the three existing
improvised tie item types. Separate Eyes/Face/Hat XMLs and six original body-
specific meshes share the original cloth atlas for all six materials. Source
inspection confirms the slots, linked-item authority and native SyncClothing
already exist; all gameplay Lua remains unchanged. See IMPROVISED_TIE_MODELS.md
for current installed 42.21 evidence, asset provenance, configuration assessment,
independent import checks and explicit runtime gates. No client-owned gameplay,
new state, item types, schema or networking was introduced. Current iteration is
source only; no packaging, deployment, upload or game/server launch. Published
0.12.0 ZIP/checksum/provenance were preserved with matching hashes, a bounded
preservation ledger and ZIP CRC. No artifact deletion occurred.

## Authorized clothing-sync Workshop MP test distribution

The user requested publication of 0.13.1-dev.1 on 2026-10-15. Canonical inputs
remain WORKSHOP_DESCRIPTION.txt and WORKSHOP_CHANGE_NOTE.txt. Build-Workshop.ps1
and Publish-Workshop.ps1 prepare and validate the existing public item 3799754736
for App ID 108600. The generated publication-0.13.1-dev.1.json binds actual
SteamCMD/API results, source commit, package/text hashes and Steam restart outcome.
Previous source-only statements describe their original milestones. Runtime
acceptance remains NOT TESTED; G7 and stable G8 remain BLOCKED. No local SP
deployment, game/server launch or server modification is authorized.

## Thumbnail source update

0.13.2-dev.1 uses the user-selected PNG as canonical thumbnail source; the previous
artwork and published 0.13.1 package/checksum/provenance are preserved with hashes
and ZIP CRC. No deletion, packaging, staging replacement, deployment, upload or
PZ/server launch is part of this request. See THUMBNAIL.md.

## Authorized 0.14 Workshop test publication

The user requested publication of 0.14.0-dev.1 on 2026-10-16. Reuse canonical
Workshop text, selected thumbnail and existing packaging/uploader scripts.
Workshop item 3799754736, App ID108600, development title and public visibility
remain unchanged. Preserve the 0.13.1 published ZIP/checksum/provenance and archive
prior staging before replacement; do not delete historical evidence. Generated
publication-0.14.0-dev.1.json binds exact release source commit, package/text hashes,
offline checks, SteamCMD/API outcome and Steam client restart. Source preparation
is not a claim of upload success. G7/current dedicated NOT TESTED and stable
G8 BLOCKED; no local mod deployment, server changes or game launch.

## Authorized 0.15 Workshop development publication

The user requested 0.15.0-dev.1 publication on 2026-10-16. Existing canonical
Workshop texts, supplied thumbnail and established builder/uploader target
item 3799754736 / App 108600, preserving development title and public visibility.
Prior 0.14 published ZIP/checksum/provenance are preserved unchanged with hashes,
CRC and ledger; the builder archives prior staging before replacement, without
deletion. Generated publication-0.15.0-dev.1.json records exact commit/package/text
hashes, offline checks, SteamCMD/API/public-page verification and Steam restart.
Preparation is not proof of upload or gameplay. Current SP/dedicated NOT TESTED;
G7 and stable G8 blocked. No game/server launch or live mod deployment.

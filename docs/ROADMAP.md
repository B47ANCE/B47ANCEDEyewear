# Roadmap

Current development source is 0.15.0-dev.1: crafted-retainer tape and fourteen-material improvised ties,
strand/tape reinforcement and zip-tie cutting alongside Lua-only context-menu and crafting
retention, two craftable wearable items, a rare loot-only unbreakable retainer,
distinct inventory icons, native head/clothing durability for all improvised ties
and crafted retainers, live condition inspection, three distinct 3D ground models
and production source preflight. Improvised ties also have a common knotted-cord
worn visual with male/female Eyes, Face and Hat fits; see IMPROVISED_TIE_MODELS.md.
The 0.13.1 patch registers all clothing XMLs in the native GUID table and
rejects unready new tie visuals before publication/equip/payment; see
CLOTHING_SYNC_FIX.md. Native/SP and dedicated acceptance remain pending.

Before stable release, obtain actual SP and dedicated multiplayer evidence for
Tie/Untie and crafting, cancellation, duplicates, one-use consumption, clothing-field sync,
existing saves, item transfers, reconnects, server restarts and UI scales/controllers.
Dedicated G7 must pass before release G8.

Finite-retainer catches require a verified exposed Lua hook with server authority
and the original engine fall decision. No Java extension or replacement RNG is permitted.
Wearable reusable items now keep their actual inventory identity through vanilla
wear/remove and save synchronization. All three retainers have separate male/female
worn meshes; in-game fit is untested. Nested attachment/escrow remains outside
this implementation. See WORN_MODELS.md. Rare-item loot uses a separate authoritative
container-fill callback and current server sandbox settings. The user approved
native head/clothing wear as the Lua-only finite alternative; see DURABILITY.md.
Exact hidden-roll counting remains unsupported and is not the current wear rule.

Earlier validation/publication documents describe their own versions only; they
are not current readiness evidence. Stable tags, live deployment and Steam Workshop
upload require separate authorization and applicable gates.

The preceding 0.13.2 artwork-only patch selected the supplied project thumbnail.
No new gameplay or runtime acceptance is claimed; see THUMBNAIL.md.

## Current 0.14 materials and reinforcement

Fourteen audited materials, same-material strands, adhesive/duct tape, material-
specific installed native condition and zip-tie cutting are implemented in Lua.
See TIE_REINFORCEMENT.md for balance, ownership/payment/replay checks, new item
identity, existing-save policy and current runtime gates. G7 for THIS gameplay
iteration is BLOCKED / NOT TESTED; earlier published acceptance remains historical.

## Crafted-retainer tape — 0.15

Crafted cloth/leather retainers now accept ONE tape in their main-inventory
right-click menu, worn or unworn. Default native wear-resistance bonus is +1 for
adhesive/+2 for duct tape. Condition, maximum, identity and worn mapping stay
unchanged; no recraft is required. Server intent validation, observed-payment
rollback boundaries, persistence, settings and runtime gates are detailed in
CRAFTED_RETAINER_TAPE.md. Unbreakable retainers are excluded. This is source-only;
current G7 NOT TESTED / BLOCKED and stable G8 BLOCKED.

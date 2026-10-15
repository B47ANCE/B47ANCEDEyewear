# Roadmap

Current development source is 0.12.0-dev.1: Lua-only context-menu and crafting
retention, two craftable wearable items, a rare loot-only unbreakable retainer,
distinct inventory icons, native head/clothing durability for all improvised ties
and crafted retainers, live condition inspection, three distinct 3D ground models
and production source preflight.

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

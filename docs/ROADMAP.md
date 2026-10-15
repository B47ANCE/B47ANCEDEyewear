# Roadmap

Current development source is 0.9.0-dev.1: Lua-only context-menu and crafting
retention, two craftable wearable items, a rare loot-only unbreakable retainer,
distinct inventory icons, read-only inspection and production source preflight.

Before stable release, obtain actual SP and dedicated multiplayer evidence for
Tie/Untie and crafting, cancellation, duplicates, one-use consumption, clothing-field sync,
existing saves, item transfers, reconnects, server restarts and UI scales/controllers.
Dedicated G7 must pass before release G8.

Finite-retainer catches require a verified exposed Lua hook with server authority
and the original engine fall decision. No Java extension or replacement RNG is permitted.
Wearable reusable items now keep their actual inventory identity through vanilla
wear/remove and save synchronization. Nested attachment/escrow, fitted 3D visuals
remain outside this implementation. Rare-item loot uses a separate authoritative
container-fill callback and current server sandbox settings. Finite durability stays blocked;
see RETAINER_ITEMS.md for the rechecked engine seam and validation gates.

Earlier validation/publication documents describe their own versions only; they
are not current readiness evidence. Stable tags, live deployment and Steam Workshop
upload require separate authorization and applicable gates.

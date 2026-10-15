# Roadmap

Current development source is 0.8.0-dev.1: Lua-only context-menu and crafting
retention, two real reusable wearable items, read-only inspection and production
source preflight. Items use vanilla equipment and output crafting.

Before stable release, obtain actual SP and dedicated multiplayer evidence for
Tie/Untie and crafting, cancellation, duplicates, one-use consumption, clothing-field sync,
existing saves, item transfers, reconnects, server restarts and UI scales/controllers.
Dedicated G7 must pass before release G8.

Finite-retainer catches require a verified exposed Lua hook with server authority
and the original engine fall decision. No Java extension or replacement RNG is permitted.
Wearable reusable items now keep their actual inventory identity through vanilla
wear/remove and save synchronization. Nested attachment/escrow, fitted 3D visuals
and loot remain outside this implementation. Finite durability stays blocked;
see RETAINER_ITEMS.md for the rechecked engine seam and validation gates.

Earlier validation/publication documents describe their own versions only; they
are not current readiness evidence. Stable tags, live deployment and Steam Workshop
upload require separate authorization and applicable gates.

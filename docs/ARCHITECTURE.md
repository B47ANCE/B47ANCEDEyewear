# Architecture



Original Lua implementation using Build 42 CraftRecipes. The recipe's explicit

inputs enumerate all current vanilla glasses and the six shared Authentic Z

identifiers; this allows the Crafting UI and the item-owned right-click menu to

select an actual item. The menu lists only available tying materials and disables

Tie with a reason when none are present. Eyepatches are deliberately omitted. A small

explicit material allowlist prevents unrelated string-tagged items becoming

consumables. Recipe callbacks validate worn status, ownership, material, and

current tie state again before mutation. Multiplayer context-menu actions send

only inventory IDs; the server resolves and validates both items before mutation.

Persistent item modData records the original fall chance and attached material.

The same clothing instance retains condition, prescription, tint, and identity.

Worn-item events and player updates restore zero chance after load/equip/sync.

No global script-item mutation or zombie hooks. Production Lua has no Java

bridge dependency. A separate development-only native catch spike is documented

in NATIVE_BRIDGE_REPORT.md; its runtime architecture gate remains open.



## Retention framework (0.2.0)



`B47ANCEDEyewear/Retention.lua` is a generic headwear/eyewear retention model that

classifies every worn clothing item into a category and derives its

`ChanceToFall`:



- `loose` (baseball caps, beanies, untied straw/sun hats) — keeps the item's

  vanilla probabilistic fall chance; a previously tied loose item restores its

  recorded chance on untie.

- `fitted` (untied eyewear) — a low fall chance (default 15).

- `strapped` (protective helmets with chin straps) — zero fall chance.

- `tethered` (any tied item) — zero fall chance.



Classification uses a small centralized override table (`Retention.register`)

plus a name heuristic (`helmet`, `hardhat`, `fireman`, and the `hat_army` prefix

for military helmets) so variants and future helmets are covered without

enumerating every identifier. Eyewear detection delegates to Core's

namespace-and-slot predicate via `Retention.isEyewear`, so masks, eyepatches and

other FACE props are never misclassified. Unknown items are left untouched.



`Core.refresh` re-applies the derived chance to every worn item on clothing

updates, player updates, and player creation, which also covers save/load and

equip/sync. The tie/untie timed action and CraftRecipe callbacks are unchanged in

contract; they now accept any tieable item (eyewear plus registered hats) while

the multiplayer serialization fields (character, glasses, material, untie) stay

intact.


Current read-only inventory tooltip implementation and validation: docs/RETAINER_TOOLTIP_INTEGRATION.md (from docs, use RETAINER_TOOLTIP_INTEGRATION.md). Vanilla tooltip remains intact; companion panel displays finite condition and actual reinforcement contributions. Runtime UI and gameplay synchronization remain untested.

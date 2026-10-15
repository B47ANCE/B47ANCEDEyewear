# Reusable retainer items

Project Version: 0.8.0-dev.1
Source review: 2026-10-14; installed Project Zomboid 42.21, Steam build 25485521.

## Items and recipes

The previous expansion reserved EyewearRetainer and prepared artwork, but never
shipped its permanent-item definition. This iteration supplies real clothing
items with ordinary vanilla CraftRecipe outputs, implemented entirely in Lua and
game data. Both are reusable material alternatives with identical protection.

| Recipe in Crafting / Tailoring | Consumed inputs | Kept tools | Output |
| --- | --- | --- | --- |
| Make cloth eyewear retainer | 2 RippedSheets; 2 uses of Twine, Thread, Thread_Sinew or Thread_Aramid | None | 1 B47ANCEDEyewear.MakeshiftRetainer |
| Make eyewear retainer | 2 LeatherStrips; 4 uses of Thread, Thread_Sinew or Thread_Aramid; 2 RubberBand | Sewing needle; usable scissors | 1 B47ANCEDEyewear.EyewearRetainer |

No learning requirement, skill level or workbench is imposed. Vanilla validates
input availability, consumes the specified quantities and produces exactly one
item per completed recipe. No OnCreate payment/output callback duplicates that
work. The OnTest hook is production crafting eligibility, not a testing harness.

Use Wear on a retainer, then wear compatible glasses. The dedicated retainer slot
is independent of glasses and necklaces and accepts one item. One untied,
unbroken, non-monocle pair receives the configured fall value, selected in vanilla
worn-slot order. Hat support remains the existing consumable Tie/Untie route.
Take Off keeps the same retainer and restores the glasses' ordinary profile.

WearableRetainersEnabled (default true) controls crafting and protection;
WearableRetainerFallChance (integer 0–100, default 0) controls the protected pair's
fall value. Disabled retainers remain real items and can always be taken off.
Setting 0 suppresses native knock-off; nonzero values use vanilla impact rules.
The two materials currently have no hidden quality or durability difference.

## Authority and ownership

[VERIFIED: source] Vanilla shared ISWearClothing.complete checks the actual item
and sets its worn mapping. ISUnequipAction.complete removes that same mapping.
The mod chains those completion methods on server/SP and refreshes derived values
without changing their result. A server fallback every 30 ticks handles reconnects,
configuration changes and outside transfers. It checks native worn mappings and
direct main-container ownership and scans only worn slots. No valuable item is
removed, serialized into ModData, reconstructed, refunded or created by retention.
Clients display derived state; they submit only vanilla crafting/equipment intent.
The server determines eligibility and fall values from its sandbox configuration.

Persistence and transfer use vanilla clothing items and worn-item mappings. No
new persistent retainer schema or historical-data migration is introduced. Older
schema 2 records retain their read-only inactive interpretation. Prior schema1
ties and original artwork are preserved. Fitted worn meshes and loot are absent;
the new clothing XML follows the installed emptytexture convention.

## Exact per-catch durability: BLOCKED

Requested rule: spend one durability point only when vanilla's actual hit would
knock the glasses off; preserve the glasses on that catch, including the final
durability point. Counting arbitrary damage events would not implement that rule.

[VERIFIED: installed source] IsoGameCharacter.class is byte-identical to the
previously audited class, SHA-256:
29040e19c3e420499f73bc0ea0d5b86d7f7d38655acdc13d0107df736eb54c0b.
Its private helmetFallFromWornItems performs the native random decision, then
immediately removes the inventory/worn item and creates the falling item. There
is no intervening Lua hook or cancellation result. Public helmetFall emits
OnClothingUpdated afterward only for a local player, so this is not a dedicated
server notification for remote players. OnPlayerGetDamage does not identify the
successful native knock-off decision. A zero fall value skips that roll entirely.

Consequently this iteration does not decrement a fictitious counter, damage
retainers on unrelated hits, introduce another RNG roll, re-equip dropped copies,
or require custom Java. The affected finite-durability implementation remains
stopped. A verified exposed server/SP hook at the actual knock-off decision is
needed to implement the requested rule safely. Inventory condition is not being
advertised as per-catch durability.

## Validation limits

[TESTED: offline] Production preflight compiles Lua 5.1, parses JSON/XML, checks
require paths, item/recipe localization, clothing/icon references and original
icon hashes. Version consistency and whitespace checks are separate.

[RUNTIME GATE] No game/server was launched. Crafting, custom-slot loading and
equipment visibility, authoritative refresh, synchronization, dropping/trading,
existing-save reloads, reconnects and dedicated restarts remain NOT TESTED.
G7 BLOCKED / NOT TESTED; stable G8 BLOCKED. No package, deployment or Workshop
upload is authorized by this implementation request.

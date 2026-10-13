# Retainer source audit — 2026-10-03

Audited Source Version: 0.3.0-dev.1

Installed game root: E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid.
[VERIFIED source] Current Core.class initializes GameVersion(42,21,"").
This is Build 42.21, not the older 42.20.3 baseline in existing project evidence.
Java runtime: installed Azul Zulu 25.0.1. No game/client/server was launched.

The reproducible read-only audit and source hashes are in
research/retainers/vanilla-audit.json. The complete material and compatibility
tables are research/retainers/MATERIAL_AUDIT.md and EYEWEAR_AUDIT.md.
16 exact material/tape FullTypes were verified, and 45 eyewear candidates classified.
No third-party implementation or asset was copied. Vanilla decompiled classes
under research/retainers/native are evidence only and excluded from runtime source.

## Blocking engine seam

[VERIFIED source] research/retainers/native/zombie/characters/IsoGameCharacter.java:
helmetFall at line 7809 returns early on GameClient.client. The private
helmetFallFromWornItems at line 7825 obtains the actual worn Clothing, evaluates
its current ChanceToFall, adds the existing head-hit adjustment and performs the
native random roll. A successful decision is immediately followed by inventory
removal, worn-item removal, model refresh and createFallingItem. Dedicated-server
iteration then breaks after a removal. No Lua call or cancellable event exists
between the successful decision and removal in this method.

The public helmetFall method calls OnClothingUpdated afterward only for a local
player when removal occurred. It provides no per-item pre-removal interception.
Wrapping a Lua-visible method cannot override calls within the native Java class.
The current mod's zero-ChanceToFall protection prevents this roll entirely.
It cannot reveal whether an ordinarily eligible item would have fallen.

[BLOCKED] A supported, build-verified native loader/interception path is not
adopted by this project. An installed FadedJavaLoader directory with an empty
plugins directory does not establish a usable public hook API, registration,
supported-build contract, dedicated deployment, or redistribution decision.
Java policy authorizes a narrow original bridge once this gap is established;
it does not supply a loader or prove a hook works. No upstream/game files were patched.

Required bridge: invoke one server/SP callback after the existing successful
roll and before any removal/drop side effects, with the actual character/item,
trusted event severity and native event identity. On a valid authoritative catch,
persist and synchronize durability once, suppress this item's removal and still
save it on the breaking hit. Preserve vanilla RNG, head-hit adjustment, iteration
and server early-exit semantics. Return normal removal on unavailable capability,
unsupported build, failed preflight, invalid state or refused callback. No client
packet may request a catch or specify damage. A callback must not partially
commit before a failed bridge result; the catch/commit boundary needs an atomic contract.

Forbidden substitutes: independent re-rolls, tick damage, OnPlayerGetDamage as
proof of knock-off, post-drop re-equipping, and ChanceToFall=0 for finite retainers.
These lose the original decision, introduce duplicate drops, or bypass durability.
Gameplay implementation is stopped at this seam under the global authority rule.

## Material and cutting-tool findings

Base.PremiumFishingLine and Base.Zipties are the exact identifiers; spelling and
case must not be guessed. Base.Scotchtape and Base.ElectricWire are normal items.
Base.Wire is drainable. Clean Base.RippedSheets, Base.DenimStrips and
Base.LeatherStrips are the audited strip candidates; bundles/dirty variants need
explicit additional policy, not automatic admission.

ISRepairClothing.complete demonstrates authoritative UseAndSync for thread and
vanilla removal/synchronization for fabric. Fishing/TimedActions/
ISChangeFishingRodEquip.complete uses a specific 0.125 normalized line amount,
which differs from the item's generic UseDelta. The proposed retainer consumes
one script use per strand; that is a declared mod choice, not copied fishing balance.

recipes_fixing.txt defines vanilla tape/zip-tie repairs, but their callbacks repair
item condition rather than retainer state and must not be reused for this feature.
recipes.txt uses base:sharpknife/base:scissors and IsNotDull for cutting inputs.
[VERIFIED] Tag-based candidate tool detection is available. [UNKNOWN] The complete
Lua/server sharpness and condition predicate for a custom cut action still needs
verification; no knife allowlist or zip-tie removal action is implemented.

## Loot findings

[VERIFIED source] ProceduralDistributions.lua defines OptometristGlasses and
SportStoreAccessories with four rolls; Distributions.lua uses both in real rooms.
These are narrow initial candidates. No loot table was modified.
Proposed weights: OptometristGlasses 0.01; SportStoreAccessories 0.005. These are
design values requiring native frequency calibration, not implemented spawn rates.
No broad bedroom/pharmacy/general-container injection or guaranteed world spawn.

Current ItemPickerJava.getActualSpawnChance incorporates vanilla loot modifiers,
the sandbox item-removal list, adjusted zombie density and elapsed-world-time loot
multiplier. Injecting into the regular items array would retain that normal path.
The junk path can replace nonzero loot modifiers with 1, so it is inappropriate
for the required scarcity behavior. Tiny weights alone do not prove rarity:
zombie density can add chance independently, and the integer random roll causes
quantization at very small thresholds. Verify a suitable ignore-density item tag
or equivalent supported option before enabling loot; do not manufacture loot in
OnContainerUpdate. Weeks-to-find behavior remains [RUNTIME GATE].

## Model and reusable-object findings

[VERIFIED source] Vanilla clothing XML for Glasses and audited eyewear sets
m_Static=true and m_AttachBone=Bip01_Head, with separate male/female model paths.
No bone name was invented. This establishes a valid head attachment convention,
not the correct units/origin/axis or fit of a new model. Goggle/novelty-frame
physical temple connections need review; all four monocles are incompatible.

AttachedLocations.lua maps human attachment slots to named model attachments.
IsoGameCharacter.setAttachedItem updates models and can send a client-owned
attached-item packet. It does not establish an authority-safe cosmetic attachment
for a retainer embedded in someone else's eyewear, or automatic eyewear transfer.
Do not use that client packet to own the valuable retainer relationship.

InventoryItem.save/load serialize complete items including inventory ID and item
modData. A raw InventoryItem placed in a Lua item table is not established as a
safe serialized attachment. A string FullType/boolean plus recreation would lose
actual-object state and needs duplication-proof escrow. Reusable permanent-item
storage must therefore establish a native attachment/container capability or an
atomic, versioned full-item escrow bridge before runtime installation/removal.
No permanent item, attachment, loot or visual lifecycle is enabled yet.

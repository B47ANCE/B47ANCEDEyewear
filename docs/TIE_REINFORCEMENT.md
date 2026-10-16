# Improvised materials and reinforcement

Project Version: 0.14.0-dev.1

Implemented 2026-10-16, Lua-only, targeting installed PZ 42.21 / Steam build
25485521. This is a MINOR capability addition, not a tested stable release.
Native head/clothing damage remains the approved wear trigger. No successful
hidden knock-off roll is intercepted or synthesized. The breaking blow can
still dislodge eyewear under native ordering.

## Player actions and balance

Tie worn compatible glasses or the existing straw/summer hats through the
right-click menu or Crafting / Tailoring / Tie worn eyewear. Keep the selected
material in the main inventory. Monocles remain excluded. New direct ties use
actual LayeredTieEyes/Face/Hat items with the existing neutral worn cord visuals.
These are linked to the same original eyewear/hat; no eyewear is reconstructed.

| Verified vanilla material | Default native condition contribution | Strand cap |
| --- | ---: | ---: |
| Base.RubberBand | 2 | 1 |
| Base.Thread | 2 | 3 |
| Base.DentalFloss | 2 | 3 |
| Base.RippedSheets | 4 | 1 |
| Base.DenimStrips | 6 | 1 |
| Base.Twine | 6 | 1 |
| Base.Thread_Sinew | 3 | 3 |
| Base.LeatherStrips | 10 | 1 |
| Base.FishingLine | 4 | 3 |
| Base.ElectricWire | 12 | 1 |
| Base.Wire | 14 | 1 |
| Base.PremiumFishingLine | 5 | 3 |
| Base.Zipties | 16 | 1 |
| Base.Thread_Aramid | 6 | 3 |

Right-click the linked worn glasses/hat to add another use of the SAME thin
material, up to three total strands. No mixed strands, fourth strand, rubber-band
stacking or bulk-material layers. One Base.Scotchtape adds 1 condition/capacity;
one use of Base.DuctTape adds 2. Tape is not a standalone tying material. Only one
tape reinforcement is allowed; neither tape works on zip ties. Tape and strand
reinforcement can be applied in either order, without changing the earned result.

Reinforcement raises current condition and installed capacity by exactly the
same contribution. For example, thread 1/2 becomes 3/4 after a second strand,
then 5/6 after duct tape. Existing wear is never erased. Broken, unworn, orphaned,
foreign or invalid linked ties cannot be reinforced. Crafted reusable cloth and
leather retainers retain their current ten-point wear rules; this feature targets
improvised ties, not those separate wearable items or the unbreakable retainer.

Zip ties require a cutting-capable tool to remove. The server resolves the
selected actual tool in the sender's main inventory, requires base:sharpknife
or base:scissors, positive general condition, no broken state, and the native
IsNotDull equivalent: !hasSharpness() || !isDull(). A tool with head condition
must also have positive head condition. No item-name allowlist. Tools are kept,
without synthetic wear; the zip tie is discarded without a material refund.
The cutting action appears only with a currently usable tool and checks again
at completion. Disabling new tying still permits cutting/removal.

Drainable materials spend exactly one generic native script use, not a fishing-
action-specific fraction. Whole materials spend the entire selected instance via
native inventory removal/synchronization. Clean fabric has ReplaceOnUse dirty
variants, so it MUST NOT use UseAndSync here: tying does not produce dirty fabric.
Dirty, sterile, bundled and boxed material variants are not implicitly admitted.

## Native condition, sandbox and presentation

New LayeredTie definitions have a FIXED ConditionMax=100. Lua never changes a
per-instance condition maximum. Material allocation starts actual native condition
at the installed base contribution; only paid reinforcement raises it. Native
server/SP clothing damage removes real condition and uses vanilla item stats.
The separate installed capacity is a validated scalar, not a second damage counter.
The companion tooltip on both the linked eyewear and tie shows actual condition /
installed capacity, live bar/percentage, material, strands and installed modifiers.
Unused modifier rows are omitted. The preserved vanilla condition bar still uses
its fixed script ceiling of 100; the mod's companion bar uses the earned material
capacity. These denominators differ intentionally; no client item mutation hides it.

Server option ImprovisedTieDurabilityMultiplier is a double, default 1, range
0.25–5, using the vanilla numeric editor. Material/tape contributions round to
nearest integer, minimum 1, and are snapshotted at installation. Changing it never
repairs or rebalances already-installed contributions; future strands and tape
use that tie's original snapshots. At the upper bound, three aramid strands plus
duct tape fit exactly into 100 native condition points. Invalid/non-numeric/NaN/
infinite/out-of-range inputs fall back to 1. ImprovisedTieWearResistance remains
the server one-in-N condition-loss denominator (1–100, default 1), applied to old
and new worn ties without repairing them. Material-specific starting capacities,
rather than fourteen separate resistance sliders, provide the requested balance.
The existing TyingEnabled gates both new ties and new reinforcement; protection
and safe removal remain available when disabled. All names/tooltips are localized
through the existing 29-locale English-fallback policy.

Strand caps and tape exclusions are material design rules. Native ceiling 100,
revision bounds, protocol identifiers and slot names are technical safety limits,
not extra sandbox options. No protocol or UI coordinates are exposed as settings.

## Authority, synchronization and persistence

The client queues Tie, Reinforce, Tape or Untie intent with target/material/tool
native IDs plus the expected tied state, tie ID and revision. It cannot choose
condition, capacity, damage, strand count, contributions or a catch. The server
resolves inventory instances, verifies direct ownership/worn mappings, reciprocal
links, sandbox rules, material/tool availability and that exact state/revision.
All four commands reject stale state, including delayed removal or a request for
a prior tie on the same glasses. SP completes locally; MP timed-action complete
only acknowledges and never also commits a second transaction. Queue cancellation
submits no intent. Action snapshot fields are plain scalars, not saved userdata.

A reinforcement copies scalar link state, increments revision once, adds native
condition/capacity, and attempts one payment. A failed/unconsumed payment restores
the original link and condition. Observed payment survives later notification
exceptions: no refund, replay or second addition. Metadata and native field
notifications are attempted independently via syncItemModData and syncItemFields.
There is no client condition writer, combat polling, world traversal or new damage
packet. As with existing Tie, command validation protects resources/state; the
client animation duration is not claimed as an authoritative anti-cheat timer.

The target's existing version=1/wearSchema=1/tieId link remains compatible. New
actual tie ModData under B47ANCEDEyewearTie retains schema=1 and adds
materialSchema=1, revision, base, strands, adhesive, duct, optional tape and capacity.
Its maximum is validated as base*strands + the installed tape contribution, and
native condition must lie within 0..capacity. Existing reciprocal IDs/material
must match. Invalid new records fail closed for protection and reinforcement.
No link is stored as raw userdata, full-item escrow or a reconstruction recipe.
No native damage counter is mirrored into ModData.

Native item serialization carries actual condition, ID and scalar ModData through
transfers, saves, reloads and reconnects. Native add/remove, SyncClothing and
SyncItemFields carry their established state. Transfer BOTH linked actual items;
a separated item cannot protect. Late-join/reconnect/restart behavior and crash
boundaries still need dedicated evidence; an offline synchronous transaction
harness does not prove disk/crash atomicity or successful network delivery.

## Existing saves and rollback

Original ImprovisedTieEyes/Face/Hat definitions remain at ConditionMax=10. A full
old item may omit condition in its native save; increasing that old script maximum
would load it at the new full maximum. Therefore no old definition was repurposed.
Existing linked ties retain their exact native condition and cannot receive new
reinforcement; their tooltip explains Untie and Tie again to opt in. Old paid
pre-link migrations still create the original ten-point type once, with no second
payment. They do not silently award a new material-specific budget. All existing
original eyewear names, conditions, prescriptions and IDs remain unchanged.
Historical schema-2 catch records remain read-only/inactive. No real saves were
opened. Old versions do not know LayeredTie types; downgrading the mod alone is
unsafe after use. Preserve a world/player backup before upgrading; no automated
downgrade or valuable-item reconstruction is provided.

## Evidence and gates

[VERIFIED: installed source, 2026-10-16] Current vanilla definitions confirm all
14 material and two tape types, script uses and fabric ReplaceOnUse. Native
InventoryItem save/load omits full condition and stores non-full condition as a
byte. Source hashes match the prior 42.21 audit. InventoryItem public methods are
registered through LuaManager.Exposer/public non-HiddenFromLua member traversal.
Native InputScript doesItemPassSharpnessStatusTests supplies the IsNotDull rule;
SyncItemFieldsPacket serializes/applies actual condition. See API_EVIDENCE.md for
fingerprints and synchronization scope. No copied vanilla source is distributed.

[TESTED: offline Windows Python 3.12 / Lupa Lua 5.1] Actual modules pass the
external reinforcement regression audit, covering all materials, payments and
failures, strand/tape limits, deficit conservation, server requests/replays,
ownership, cutting tools, configuration, legacy migration, tooltip, timed actions,
menus and crafting. The harness/doubles stay outside the repository per the user
request to remove test/debug code. Exact commands/counts are in VALIDATION.md.

[RUNTIME GATE] G6 SP NOT TESTED; current G7 dedicated BLOCKED / NOT TESTED; stable
G8 BLOCKED. Prior user-reported 0.13.1 MP acceptance is historical, not proof of
0.14 gameplay. Verify two-client wear/reinforce/cut, native head damage, last-point
breakage, replay/resource totals, canceled actions, full inventory, transfers,
new/old saves, late join/rejoin and restart, tool invalidation, UI/controller/scale
and appearance. No game/server launch, package, deploy or upload was performed.

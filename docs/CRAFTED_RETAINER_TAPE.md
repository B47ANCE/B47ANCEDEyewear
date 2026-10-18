# Tape for crafted cloth and leather retainers

Project Version: 0.15.1-dev.1

MINOR capability addition, implemented 2026-10-16 against the existing installed
PZ 42.21 / Steam build 25485521 evidence. Lua-only; no item definitions, recipes,
meshes or native method hooks change. This source iteration is not deployed or
published. Workshop remains the previously published 0.14.0-dev.1 package.

## Use and effect

Put a crafted Cloth Eyewear Retainer or Eyewear Retainer and usable tape in your
main inventory. Right-click the RETAINER itself, open its item submenu and choose
Reinforce retainer with the available tape. It may be worn or unworn. One whole
Base.Scotchtape adds +1 native wear resistance by default; one generic script use
of Base.DuctTape adds +2. The actual same retainer stays in inventory/equipment.
No replacement item, crafting byproduct, new model or forced equip is created.

Each actual retainer accepts ONE tape, total. No second layer, tape swap/removal
or strand reinforcement. Existing retainer instances work immediately; no recraft
or retie is required. Broken retainers cannot be reinforced. The rare Unbreakable
Eyewear Retainer cannot receive tape. Retainers/tape in nested bags, world
containers or another player's inventory must first be in the acting character's
main inventory. No unavailable-action menu or empty submenu is added.

Crafted tape changes wear resistance, not capacity. Current condition and the
native ten-point maximum NEVER change: a damaged 4/10 item stays 4/10. At default
settings, cloth's one-in-2 condition-loss chance becomes one-in-3 with adhesive or
one-in-4 with duct tape; leather's one-in-4 becomes one-in-5 or one-in-6. These are
eligible native head/clothing damage probabilities, not fixed catches or hits.
Existing native coverage/layering/breaking-blow ordering remains in force.
Improvised-tie reinforcement retains its separate material-capacity arithmetic.
This distinction preserves valuable crafted items' native identity and save
representation without unsafe per-instance maximum changes or reconstruction.

The read-only companion tooltip on the retainer and glasses it protects shows
actual condition/bar plus current wear resistance and the installed tape effect.
It shows the effective bonus after the resistance cap; at zero effective bonus,
it identifies the installed tape without a misleading zero modifier row. Invalid
tape metadata displays unavailable information rather than mutating/repairing it.

## Sandbox behavior

RetainerTapeResistanceMultiplier is server-owned: double, default 1, range 0.25–5,
using the existing vanilla numeric editor. It scales the tape's +1/+2 contribution,
rounds to the nearest integer and has a minimum bonus of 1. The bonus is snapshotted
at application. Invalid, nonnumeric, NaN, infinite or out-of-range values use 1.
The material balance reuses the established adhesive/duct catalogue; no separate
per-item sliders or protocol settings are introduced.

Installed bonuses do not change when the multiplier changes. Current cloth/leather
base wear settings still apply, plus the saved bonus, capped at the existing 100
wear-resistance limit. At base 100 the action is omitted/refused before payment
because it has no effect. Already taped items retain their paid record if later
configuration caps their effective bonus. No setting repairs condition.
WearableRetainersEnabled gates new tape applications along with existing crafting
and protection. Disabling preserves existing tape/items; native worn wear can
still occur with the bonus, as a property of the physical item. TyingEnabled
continues to control improvised ties and does not control crafted tape.
All new UI/sandbox strings use the existing 29-locale English-fallback policy.

## Authority, transactions and persistence

RetainerTape extends the existing timed-action/server-command route. The client
sends target/tape native inventory IDs and expected state/revision only; no chosen
bonus, condition, resistance or output item. Action snapshots are scalar fields.
The server resolves owned direct-inventory items, exact crafted type, positive
native condition, setting, usable tape and absence of ANY prior tape record.
A stale revision or foreign/lost/spent item is rejected. The client only animates
and reads replicated state. MP timed-action complete acknowledges only; validated
server command owns the single mutation. SP completes through the same service.

Authoritative tape state is a plain item ModData record under
B47ANCEDEyewearRetainerTape: schema=1, revision=1, tape=<verified FullType>, bonus=<integer>.
Missing state adds no bonus; malformed state adds no bonus and prevents another
application. Original/native wear and protection remain otherwise valid. Unrelated
item ModData, identity, name, custom-name, condition and worn mapping are preserved.

The server stages this record and derived resistance before one material payment.
A failed/unconsumed payment restores prior metadata and native resistance. Once
payment is observed, later notification errors retain the paid application and
cannot grant a second layer/refund. syncItemModData and syncItemFields are attempted
independently using the existing exposed vanilla APIs. A bounded worn-slot refresh
reapplies the bonus server-side after wear, transfers, configuration and reconnects;
it never polls combat or scans the world. No valuable retainer is reconstructed.
No new API exposure or native serialization claim is needed; existing inspected
native item ModData/ID/condition serialization owns persistence and transfer.

Old items with no tape record need no migration and keep exact condition. Native
ConditionMax remains 10 for these original types, including fully healthy old saves
that omit an explicit condition field. Older mod versions ignore the new bonus
record; reinstalling current source restores interpretation without reconstructing
items. Downgrading the broader mod remains unsupported; preserve world/player
backups. No real player saves or remote server were modified.

## Evidence and limits

[TESTED: offline Windows Python 3.12 / Lupa Lua 5.1] An external audit runs actual
modules against doubles, including all prior improvised-tie checks and new crafted
tape cases: worn/unworn cloth/leather, damaged/full items, ownership and replay,
all payment/notification failures, configuration bounds/snapshots/cap, malformed
records, transfers/scalar reload, live read-only tooltip, menus, canceled actions
and client/server/SP completion routes. Strict fake native setter arity catches
Lua multiple-return mistakes. The harness stays outside source/Git. Commands and
current assertion count are in VALIDATION.md. Offline simulation is not native
save, packet delivery or gameplay proof. Production preflight remains required.

[RUNTIME GATE] Current SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; stable G8
BLOCKED. Test exact installed version on two clients: paid worn/unworn application,
single-use totals, native head/clothing wear, condition sync, transfer, save/load,
join/rejoin, disconnect during action/payment, restart, setting changes and
UI/controller/scaling. Prior 0.13.1 acceptance cannot prove 0.15 behavior. No game,
server, local mod deployment or Workshop publication is authorized by this task.

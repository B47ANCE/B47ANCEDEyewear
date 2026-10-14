# Lua API evidence

Project Version: 0.6.0-dev.1
Source inspection: 2026-10-14. Target Build 42.21.

The installed Steam app108600 build25485521 uses the original JAR Core.class hash
8f5c69740c8bf2181123a831ab68d1dfb047453687cca6dc62c77816d76ab360,
matching the prior42.21 audit. InventoryItem.class hash:
48f01be16d1ef1b76e37638fac6e25ca4eb285ad38ab2f462caa5597318c7f9d.
This is binary/source provenance, not actual game execution.

[VERIFIED: source] Installed shared/TimedActions/ISBaseTimedAction.lua defines
perform() and delegates client queue completion through ISTimedActionQueue.
Installed shared/Entity/TimedActions/ISHandcraftAction.lua calls luaCallOnCreate
then processDestroyAndUsedItems. The former custom recipe has been retired rather
than relying on an unsupported preflight hook or consuming material twice.

[VERIFIED: source] InventoryItem's exposed inventory/container, name/custom-name,
ModData, ID, current-use and UseAndSync interfaces support the retained context-menu
path. UseAndSync may consume before a synchronization exception; consumption must
be observed before retaining a paid tie. Existing syncItemModData/syncItemFields
remain vanilla synchronization, not a replacement networking implementation.

The inventory tooltip delegates to item:DoTooltip. The companion renderer chains
ISToolTipInv.render without replacing its vanilla measurement/drawing logic.

[UNKNOWN / RUNTIME GATE] Actual MP timed-action acknowledgement, command arrival,
derived ChanceToFall ownership/synchronization, save/reconnect behavior, material
consumption recovery and tooltip UI scales/controllers remain untested. G7 remains
BLOCKED / NOT TESTED and stable G8 BLOCKED. No custom Java runtime is used.

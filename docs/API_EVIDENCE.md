# Installed vanilla API evidence

Inspected the installed `projectzomboid.jar` directly with CFR on 2026-09-11;
temporary output is in workspace `.tmp-stayput-api`. No third-party mod inspected.

- Clothing exposes getChanceToFall/setChanceToFall. Its save/load methods do not
  serialize that field, hence persistent modData plus worn-item restoration.
- IsoGameCharacter.helmetFallFromWornItems skips Clothing with chance <= 0,
  including the hitHead path. This is the native retention mechanism used here.
- Vanilla shared ISRepairClothing uses complete for mutation and UseAndSync for
  thread consumption. ISChangeFishingRodEquip demonstrates syncItemModData.
- Generated clothing scripts identify vanilla Glasses and Glasses_* clothing;
  eyepatches are excluded. Generated drainable scripts define Twine, DentalFloss,
  Thread, Thread_Aramid, Thread_Sinew; normal scripts define RubberBand.

These are static observations, not runtime proof. No Java code is shipped.
Protection also covers other callers of the same native fall-off path.
Disabling the mod restores normal fall chance when items reload.

## Optional eyewear compatibility

User requested Authentic Z and Frockin glasses compatibility. Narrow question:
do their glasses expose ordinary clothing identity and the engine eyewear slot?
Read only relevant installed item identifiers/module/body-location metadata.
Authentic Z Current (2335368829) has six glasses in AuthenticZClothing using Eyes;
Lite has four of these. No definitions, assets, balance, or Lua implementation
were imported. Installed Frockin packs did not identify the requested glasses.

Independent vanilla evidence: shared NPCs/BodyLocations.lua registers
ItemBodyLocation.EYES; shared TimedActions/ISWearClothing.lua uses that native
location. General capability: third-party clothing can use vanilla wear slots.
Design consequence: original slot-and-name predicate, no external mod dependency.
SOURCE CODE COPIED: NO
IMPLEMENTATION DERIVED FROM REFERENCE: NO
Remaining verification: identify exact Frockin glasses pack and test actual
instances, tying, combat, save/reload, and multiplayer in the game.

### Frockin family follow-up (2026-09-11)

User identified the full family. Installed current Build 42 script metadata was
checked for item names containing glasses/goggles/spectacles or eye body slots:

| Pack | Workshop ID | Current script files | Eyewear candidates |
| --- | --- | --- | --- |
| Volume 1 | 3307376332 | 5 | 0 |
| Volume 2 | 3411888105 | 7 | 0 |
| Volume 3 | 3431256608 | 4 | 0 |
| Volume 4 | 3475347500 | 10 | 0 |
| Volume 5 | 3635394848 | 8 | 0 |
| Shirts & Ties | 3453676250 | 5 | 0 |
| Wiseguys | 3538760023 | 2 | 0 |
| Stompers | 3736813592 | 6 | 0 |

These counts describe installed copies, not every online revision or dynamically
created item. No new runtime change is justified from these copies.
Volume 6 (3798149669) and Backstage (3798146388) are absent locally; their titles
were verified against their Steam Workshop pages. Inspect their eyewear metadata
after the user subscribes and Steam completes downloading. The earlier pack
identification question is resolved; missing current files are the remaining gap.

### Faded's Authentic Z (2026-09-11)

User explicitly requested support. The local Workshop and live-mod metadata
search found original Authentic Z only, with no Faded edition or downloaded
archive in Downloads. Faded's catalog identifies Authentic Z - Current version
42.20.2.1 at https://fadedmods.com/?mod=Authentic+Z+-+Current&page_id=12 .
The download requires accepting an access agreement. No agreement was accepted,
and no protected download or third-party implementation was accessed.

Compatibility remains unverified pending locally supplied item metadata.
Existing recognition is namespace-independent for named glasses in the native
EYES slot, so no guessed Faded-specific identifiers or dependencies were added.
Next step: inspect module/item/body-location metadata from the user's installed
edition, exercise the existing predicate, and add regression cases or an original
narrow adapter if the evidence establishes a different eyewear convention.

### Downloaded editions checked (2026-09-11; supersedes missing-file notes)

Read only module/item/body-location metadata inside the user-downloaded
`C:/Users/willi/Downloads/Authentic-Z-Current-v42.20.2.1.zip`, without extracting
or installing it. Faded's edition uses the same six AuthenticZClothing glasses
identifiers already covered by the regression suite, all using Eyes. The existing
namespace-independent recognition therefore needs no runtime modification.
ClownNose and ClownNoseTINT also use Eyes but are correctly excluded by name;
mask accessories are excluded. Additional host regression covers these negatives.

Newly installed Volume 6 (3798149669): 11 item-script files, no glasses/goggles/
spectacles name or eye-slot candidates. Backstage (3798146388): one component
script, no such candidates. These are checks of installed item definitions,
not a claim about every possible dynamically created or future item.

SOURCE CODE COPIED: NO
IMPLEMENTATION DERIVED FROM REFERENCE: NO
Only compatibility metadata was used; no assets, balance, definitions, or
third-party algorithms were imported. Native combat/persistence/multiplayer
acceptance remains UNVERIFIED. No external mods were modified or deployed.

### Eyewear reference recheck

Broader filename and text-metadata search clarified the earlier item-script audit:
Frockin Volume 5 and Volume 6 outfit XML DOES reference glasses, including vanilla
aviators and prescription sunglasses. These are existing game eyewear references,
not new item definitions. Compared glasses asset GUIDs in Frockin fileGuidTable.xml
against installed vanilla media/fileGuidTable.xml: Volume 5 has 1 unique glasses
asset path, Volume 6 has 25, and Stompers has 45 across non-LEGACY copies; all their
GUIDs exist in vanilla. A GUID-table entry alone does not prove an outfit uses it.
Thus Frockin outfits can include glasses, and those vanilla glasses already qualify
for this mod. No distinct Frockin glasses item definition was found. Only reference
metadata was compared; no outfit structure or assets were copied.

### Multiplayer action audit

Installed jar NetTimedAction serializes constructor-named fields and reconstructs
the shared action on the server; the constructor fields character, glasses,
material, and untie match this contract. LuaTimedActionNew.complete invokes Lua
complete only when not GameClient.client. SyncItemModDataPacket synchronizes the
item modData and does not restore the transient clothing chance itself; existing
worn-player refresh derives that value from synchronized persistent state.
Vanilla ISRepairClothing permits a started client presentation to survive early
server consumption. The glasses action now handles this race while retaining
strict authoritative completion checks, explicit client write rejection, and
missing-item startup guards. No vanilla or third-party functions are replaced.
Native timing, remote players, reconnect, and actual dedicated-server authority
still require runtime observations; this static audit cannot certify them.

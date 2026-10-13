# Eyewear retention profiles

B47ANCE'd Eyewear applies these `ChanceToFall` values to worn, untied vanilla eyewear. Tied supported eyewear uses `0`; this changes item instances, not vanilla item definitions.

| Value | Vanilla item IDs |
| ---: | --- |
| 2 | `Glasses_SkiGoggles`, `Glasses_SwimmingGoggles` |
| 5 | `Glasses_SafetyGoggles` |
| 8 | `Glasses_Shooting`, `Glasses_Prescription_Shooting`, `Glasses_OldWeldingGoggles` |
| 10 | `Glasses`, `Glasses_Prescription` |
| 15 | `Glasses_Aviators`, `Glasses_Prescription_Aviators`, `Glasses_Normal_HornRimmed`, `Glasses_Cosmetic_Normal_HornRimmed` |
| 18 | `Glasses_CatsEye`, `Glasses_CatsEye_Sun`, `Glasses_Cosmetic_CatsEye`, `Glasses_Prescription_CatsEye_Sun` |
| 20 | `Glasses_Normal`, `Glasses_Cosmetic_Normal`, `Glasses_Sun`, `Glasses_Prescription_Sun`, `Glasses_Round_Normal`, `Glasses_Round_Shades`, `Glasses_Cosmetic_Round_Normal`, `Glasses_Prescription_Round_Shades`, `Glasses_70s_Gold`, `Glasses_Cosmetic_70s_Gold`, `Glasses_Macho` |
| 25 | `Glasses_Reading`, `Glasses_JackieO`, `Glasses_Prescription_JackieO` |
| 30 | `Glasses_HalfMoon`, `Glasses_Cosmetic_HalfMoon`, `Glasses_SunCheap`, `Glasses_NewWave`, `Glasses_Round_HoloSkulls` |
| 35 | `Glasses_3dGlasses`, `Glasses_Groucho`, `Glasses_Venetian`, `Glasses_Novelty_Xray` |
| 70 | `Glasses_MonocleLeft`, `Glasses_MonocleRight`, `Glasses_Cosmetic_MonocleLeft`, `Glasses_Cosmetic_MonocleRight` |

The four monocles cannot be tied and never enter a tied state. A worn monocle from an older release has obsolete B47ANCE'd Eyewear tie state cleared server-side, then receives its 70-value profile. The prior retainer material is not refunded: it was consumed in the earlier completed action, and creating an inventory mutation during save migration would be less safe than preserving the item and correcting its state.

Build 42's four vanilla monocle item definitions omit `ChanceToFall`; B47ANCE'd Eyewear therefore supplies the explicit 70-value profile rather than relying on an unverified engine default.

Unknown/modded eyewear keeps the previous fitted fallback unless a compatibility patch calls `B47ANCEDEyewear.Retention.registerEyewearProfile(itemType, chance)`.

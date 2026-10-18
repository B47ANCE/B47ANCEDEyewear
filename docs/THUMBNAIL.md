# Project thumbnail artwork

Project Version: 0.15.1-dev.1

Original selection milestone (0.13.2-dev.1); statements below describe that original request.
The 0.15.1 icon update preserves this thumbnail exactly; see MOD_ICON.md.

The user explicitly selected the supplied Eyewear/glasses-and-cord PNG on
2026-10-15. Canonical source: root thumbnail.png, 1254x1254 RGB PNG, exact bytes.
SHA-256: 10ac7ba24b2b0f784a3a0eb294b915088311d8a3924d7aad4af3de2cf9d86758.
No redraw, cropping, resampling or fallback substitution was performed.
assets/branding/thumbnail.json records portable source identity and provenance.

The previous custom 1024x1024 thumbnail is preserved byte-for-byte as
assets/branding/Eyewear_Thumbnail_Previous.png (and in Git history). Existing
Build-Workshop.ps1 reads root thumbnail.png and derives a 256x256 preview.png
when packaging is authorized. The current request changes the source only;
Workshop/staging previews and published archives were not rewritten.

Mod icon, poster, item icons, ground/worn meshes, textures, Lua, crafting, loot,
durability, clothing registrations, network authority and save schema are
unchanged. The only runtime metadata difference is modversion. Artwork size
is presentation data, not configurable gameplay. No API or runtime logic changes
require new API, compatibility, configuration or architecture claims.

[TESTED: offline, 2026-10-15] Pillow decoded/verified the selected and preserved
PNGs; dimensions, mode, integrity and SHA-256 match their recorded originals.
Production source/version checks pass. No gameplay test was run. Historical
runtime reports retain their exact old version/package and acceptance limits.
Stable G8 remains blocked; no stable release is approved by an artwork update.

No package, deployment, Steam Workshop upload, Steam restart or game/server
launch occurred in this iteration. A future publish request will use this art.

0.14.0-dev.1 adds gameplay independently of this artwork. The selected original
thumbnail and preserved prior artwork remain byte-identical; no preview was built.

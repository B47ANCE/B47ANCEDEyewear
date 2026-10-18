# Transparent mod-list icon

Project Version: 0.15.1-dev.1

On 2026-10-18 the user selected the generated glasses-and-cord cutout as the mod
icon, with no text or background fill. The original thumbnail is the reference;
built-in image generation produced the selected transparent master. Its original
prompt is retained at assets/branding/Eyewear_Icon_Prompt.txt. The selected master
is assets/branding/Eyewear_Icon_Transparent.png, 1254x1254 RGBA, SHA-256
4734edc206992b892bd6d428eaeed2e8b880056e6ca83bf807d17d5aab3f65ea.

`python -B scripts/build_mod_icon.py` exports that master to the established
64x64 RGBA mod-list icon with Pillow LANCZOS, retaining alpha without a fill,
crop or redraw. The existing mod.info icon binding remains
media/ui/B47ANCEDEyewear_icon.png. Export/source hashes and dimensions are in
assets/branding/mod-icon.json; production preflight validates them, compares
export pixels with the master-derived image and checks transparent corners.
The prior fallback icon remains preserved in assets/branding/B47_ICON_SMALL.png
and Git history. No retainer inventory icon or poster is replaced.

The canonical thumbnail.png remains byte-identical:
10ac7ba24b2b0f784a3a0eb294b915088311d8a3924d7aad4af3de2cf9d86758.
The existing builder still derives its Workshop preview from that original;
the selected icon never becomes the Workshop preview. The poster is unchanged.

[VERIFIED: source] This local presentation update changes no Lua, native gameplay
definition, recipe, translation, configuration, authority, synchronization or save
format. A fixed artwork choice needs no sandbox setting. [TESTED: offline] PNG
decode, alpha, export parity, metadata path/case and source/package checks are
recorded in VALIDATION.md and generated publication provenance. [RUNTIME GATE]
Native mod-list appearance is NOT TESTED; no game/server is launched. Inherited
0.15 gameplay still lacks current SP/dedicated acceptance, so G7 remains BLOCKED /
NOT TESTED and stable G8 BLOCKED. Authorized development distribution to existing
item 3799754736 is separate from runtime proof. Steam restart requires explicit
approval for that specific restart after verified publication.

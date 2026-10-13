# Art provenance

Mode: built-in imagegen, generated then edited for readability; no CLI fallback.
Only the original mod-owned generated image was supplied as an edit reference.
Original retained imagegen outputs remain in the Codex generated-images directory;
the selected source and runtime-sized icon are copied into this project.
Pillow only performs normal alpha-preserving inventory resize/padding, not artwork editing.
Model geometry and technical texture atlas are original deterministic source assets
created by scripts/build_retainer_assets.py; no reference mesh, asset or texture copied.

## Initial prompt

Use case: stylized-concept. Asset type: original Project Zomboid inventory item sprite,
one commercial eyewear retainer. Create a single isolated dark charcoal flexible sports
eyewear retaining cord, arranged in a shallow curved U loop, with two clearly visible
small rubber/silicone sleeves at its ends that grip the temples of glasses and one
compact adjustable slider behind the loop. No glasses or person. It must read as a
purpose-built glasses retainer, not necklace, shoelace, rope, wire, or lanyard.
Restrained painted game-inventory style, bold readable silhouette, subtle highlights
for dark cord, modest thickness, centered with tight reasonable padding. Clean true
transparent RGBA background. No text, logo, watermark, baked background, or checkerboard.
Designed to remain recognizable when reduced to 64x64 pixels.

## Selected edit prompt

Edit this original eyewear-retainer inventory asset for actual 64x64 pixel readability.
Preserve the commercial sports glasses-retainer identity: one U-shaped curved dark
flexible cord, TWO rubber silicone temple sleeves with conspicuous small circular
openings, and ONE compact adjustment slider. Make the cord substantially thicker in
the illustration (but not rope-like), use medium charcoal with clear light gray edge
highlights, and enlarge the temple sleeves and slider slightly. Simple bold painted
inventory-game silhouette with very restrained detail, no complex braid texture.
The object should nearly fill a square canvas with just a small transparent margin.
Remove ALL outer glow, cast shadows, background shading, or backdrop: only object
pixels, true clean transparent alpha surrounding it. No person or glasses, no text,
logo, watermark, necklace clasp or unrelated objects. Readable dark retainer object
against both light and dark inventory UIs.

Reference: EyewearRetainer_Inventory_Source.png (the initial original generated source,
before it was replaced with the selected edit). Transparent background was requested
for both calls. Generated images are original source assets; model fit and inventory
appearance in PZ are not validated by generation or visual inspection here.

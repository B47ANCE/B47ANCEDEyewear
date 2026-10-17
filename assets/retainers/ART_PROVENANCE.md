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

## Crafted retainer icons — 0.9.0-dev.1, 2026-10-14

Mode: built-in image_gen, one call per asset, transparent_background=true.
No CLI/API-key fallback or third-party image/mesh reference was used. Both
selected outputs are retained as unchanged project masters. Pillow 12.3.0 only
performs a normal premultiplied-alpha resize to 60x60 plus 2px transparent padding
inside 64x64; it does not redraw or remove a background. crafted-icons.json binds
source/export/runtime hashes. The original black icon and model files retain
all prior hashes and are reserved for the rare unbreakable item.

### Cloth prompt (verbatim)

Use case: stylized-concept. Create one finished Project Zomboid inventory item sprite, centered on a truly transparent square canvas. Subject: a homemade CLOTH EYEWEAR RETAINER, not glasses: a narrow off-white/ecru fabric cord bent into a relaxed upside-down U, with simple small tied cloth loops at both tips to slide over eyeglass temples. Show soft cloth weave and two modest knots; clearly handmade from ripped sheets and twine. Muted slightly weathered survival-game painted item art, crisp dark edging and restrained shading, readable as a small 64x64 inventory icon. Orthographic three-quarter/top-down catalog view, silhouette occupies about 85 percent of square, generous clear transparent margins, no drop shadow outside the item. Keep shape simple and strong enough to survive reduction to 64 pixels. No text, letters, logos, glasses, person, borders, tile, checkerboard, background, or extra objects. This will become an in-game icon; produce actual alpha transparency.

### Leather prompt (verbatim)

Use case: stylized-concept. Create one finished Project Zomboid inventory item sprite, centered on a truly transparent square canvas. Subject: a handmade LEATHER EYEWEAR RETAINER, not glasses: a slim medium-brown leather strap bent into a relaxed upside-down U, with modest beige stitched edges and a small dark rubber loop at each tip to slide over eyeglass temples. Clearly a practical small leather eyeglasses retaining strap, not a belt, bracelet, lanyard clip or spectacle frame. Muted slightly weathered survival-game painted item art, crisp dark edging and restrained shading, readable as a small 64x64 inventory icon. Orthographic three-quarter/top-down catalog view, silhouette occupies about 85 percent of square, generous clear transparent margins, no drop shadow outside the item. Keep stitching broad and silhouette simple enough to survive reduction to 64 pixels. No text, letters, logos, glasses, person, borders, tile, checkerboard, background, metal buckle or extra objects. This will become an in-game icon; produce actual alpha transparency.

Selected masters: ClothRetainer_Inventory_Source.png and
LeatherRetainer_Inventory_Source.png (both 1254x1254 RGBA with real alpha).
Runtime exports: Item_B47ANCEDEyewearClothRetainer.png and
Item_B47ANCEDEyewearLeatherRetainer.png (both 64x64 RGBA).
These are inventory assets, not fitted on-character meshes.

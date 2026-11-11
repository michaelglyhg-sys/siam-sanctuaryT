# Refined visitor assets

Original visitor-male.glb and visitor-female.glb preserved. New outputs visitor-male-refined.glb (31,290 triangles, 710,776 bytes) and visitor-female-refined.glb (34,498 triangles, 813,248 bytes). Each retains 31 merged mesh/material groups. No extra textures or compression dependencies.

Added eyelid rims, lip planes, ear helix/antihelix, nose wings, swept hair ridges, female bun strands, collar piping and chased motifs, silk pleats, buckle filigree, hem lattice and finger creases/nails. All 13 animation nodes have identical local translation/rotation/scale to the original exports, verified by parsed GLB comparison. Shoulder/elbow/wrist pivots unchanged.

Editable source: reference-visitors-refined.blend. Generator: generate_refined_visitors.py. Front closeup: reference-visitors-refined-closeup.png. Round-trip validation imports both GLBs into a fresh background Blender process and renders reference-visitors-refined-glb-verified.png. This render and the closeup were visually inspected. Actual browser animation integration is handled separately.

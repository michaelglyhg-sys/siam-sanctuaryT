# Additional original Buddha poses

Generated from this project's original sculpture source; no legacy game assets used.

| File | Height (m) | Triangles | Bytes |
| --- | ---: | ---: | ---: |
| buddha-reassurance.glb | 4.053002 | 3724 | 96652 |
| buddha-standing.glb | 4.053002 | 3692 | 95688 |
| buddha-teaching.glb | 4.711819 | 24632 | 636628 |

All assets: glTF 2.0 binary, Y-up, +Z forward, base at Y=0, 2 standard PBR materials, no textures or compression decoder dependency. Standing variants have aligned feet; reassurance has raised right palm, standing has both arms down. Teaching has right hand before chest with thumb/index circle and left palm in lap.

Source: generate_pose_variants.py and buddha-pose-variants.blend. Source preview: buddha-pose-variants-preview.png. Export round-trip check: verify_pose_variants.py imported all three GLBs into an empty Blender background scene and rendered buddha-pose-variants-glb-verified.png; inspected visually. GLB JSON bounds, index counts, material counts and transform-free nodes checked. No live Blender scene or website code modified. These are stylized original sculptures, not claims of historically exact replicas.

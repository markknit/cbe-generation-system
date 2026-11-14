# GS1.2 The Cell — licensed microscopy asset suitability review

Review-only investigation, 2026-11-14 UTC. No canonical content, authored assets, outputs or acceptance records changed. **Scoped PASS: suitable licensed light and TEM plant/animal examples are available, with the specimen and observation limits below.** This is an asset suitability decision, not content acceptance or a claim that all source outcomes can now be delivered.

## Method and evidence

Inspected primary repository descriptions, explicit image licences, and downloaded ordinary publicly offered JPEGs; visually inspected actual pixels. No restricted download bypass and no AI illustrations. Evidence and exact URLs/SHA256 are in `evidence/cell_assets/download_manifest.json`; primary HTML snapshots and unchanged image downloads sit beside it. Source metadata establishes organism/tissue/mode; visual notes distinguish structures actually readable from things that cannot be identified in these images.

## Verified light microscopy

**CIL12594: suitable animal light example.** [Primary record](https://www.cellimagelibrary.org/images/12594), [JPEG](https://www.cellimagelibrary.org/download/web_jpeg/image/12594). Human (*Homo sapiens*) cheek squamous epithelial cell; brightfield, phase contrast and DIC views of the same cell, composite1397×3125. Public Domain; credit Graham Wright(2011), CIL12594, DOI10.7295/W9CIL12594. Zeiss Axiovert200M with100×1.4NA objectives; these are objective specifications, not a total magnification claim. Actual pixels show cell outline, cytoplasm, nucleus and contrast-dependent granularity. A15µm bar is embedded in the bottom panel. Do not assign individual granules to mitochondria, ER or ribosomes, or claim to resolve a membrane bilayer. Panel modes are named in metadata but not labelled on the displayed composite; retain the composite unless mapping is separately established. This supports comparison of observable detail across light-contrast techniques, not resolution of every organelle.

**CIL43552: suitable plant light example with root/mitosis qualification.** [Primary record](https://www.cellimagelibrary.org/images/43552), [JPEG](https://www.cellimagelibrary.org/download/web_jpeg/image/43552). Onion (*Allium cepa*) root tip, acetocarmine-stained chemically fixed whole mount, brightfield;40×0.65NA objective,1280×1024. Public Domain; credit Shoba Shanti(2013), CIL43552, DOI10.7295/W9CIL43552. Actual pixels show cell boundaries and stained nuclei/condensed mitotic chromosomes; multiple division stages are present. Pale boundaries can support recognising plant cell walls; a separate plasma membrane is not resolved. No scale bar/calibration was found, so no size measurement or invented total magnification. This is dividing, nonphotosynthetic root tissue; do not label it leaf tissue or infer that plant cells lack chloroplasts because this sample does not show them. ER, ribosomes and mitochondrial cristae cannot be identified here.

## Verified animal TEM

**CIL39755: suitable animal ultrastructure example, explicitly a partial cardiac muscle section.** [Primary record](https://www.cellimagelibrary.org/images/39755), [JPEG](https://www.cellimagelibrary.org/download/web_jpeg/image/39755). Mouse (*Mus musculus*) cardiac muscle, TEM of70nm section, PhilipsCM100 at80kV; chemical fixation, osmium and uranyl/lead contrasting. Public Domain; credit Dee Lauzon, Sue Lancelle, Marian Rice, Mount Holyoke College(2012), CIL39755, DOI10.7295/W9CIL39755. Actual1805×1711 pixels show a large nucleus crossing the frame, nucleolus/chromatin contrast, nuclear boundary, many mitochondria with cristae, and specialised muscle fibrils. The2µm scale bar is clear. It is sufficiently broad for nucleus-versus-cytoplasm/mitochondria comparisons, but neither the full cell outline nor the complete nucleus is contained in frame. Do not call it a complete generic animal cell, identify every pale vesicle as a vacuole/lysosome, or equate absence from this section with absence from animal cells. No disease is specified by the record.

## Normal land-plant TEM — suitable

[Hsu, Chou, Yen and Jane(2026), Botanical Studies67:13](https://doi.org/10.1186/s40529-026-00499-x), published15October2026, supplies the preferred plant TEM: [Figure3](https://link.springer.com/article/10.1186/s40529-026-00499-x/figures/3), *Brachypodium distachyon* leaf mesophyll. Preparation: high-pressure freezing/freeze substitution;70–90nm sections, FEI TecnaiG2SpiritTWIN at80kV. Explicit [CC BY4.0](https://creativecommons.org/licenses/by/4.0/); no exception credit found. Credit all four authors, article/DOI and Figure3; declare crops/annotations.

Viewed actual1985×1736 composite:3B shows cell wall/enclosed section, large vacuole, nucleus and chloroplasts,2µm bar;3C shows nucleus/chloroplast/mitochondrion detail,1µm bar.3D–F provide thylakoid/cristae/roughER detail at smaller scales. Use3B for broad comparison,3C/F only for detail. Plasma membrane bilayer and ribosomes cannot be reliably distinguished at3B scale. This is normal prepared leaf tissue, not infected maize or an isolated chloroplast.

Optional [Figure1](https://link.springer.com/article/10.1186/s40529-026-00499-x/figures/1),1985×2540: *Arabidopsis thaliana* root meristem1B–C shows nucleus, small vacuoles and cytoplasmic organelles, with1µm/0.3µm bars; chloroplasts must not be expected.1A is light microscopy; remaining panels are TEM. Prefer3B over the less elementary root-cell detail. All original composites are preserved unchanged in evidence; no publishing crop made here.

## Exclusions and limits

CIL9526 is a green alga,10431 specialised frog barrier tissue, and12587 infected maize; none is selected as a generic normal land-plant/animal comparison. Other infected maize/virus records, isolated plastids and disease-only samples do not fill the target gap. Wisconsin Eldon Newcomb images are promising teaching references, but the [collection terms](https://botit.botany.wisc.edu/about.html) allow classroom use and restrict web/published redistribution without permission; they are not selected for a portable lesson package. No permission request was sent.

## Practical selection and comparison limits

Use CIL12594 (human cheek/light), CIL43552 (onion root/light), Hsu2026Figure3B (grass leaf/TEM), and CIL39755 (mouse cardiac muscle/TEM). This is a defensible four-example set when every caption names the actual organism, tissue, method and preparation. It compares observed structures across different biological samples; it is not a controlled same-cell light-versus-TEM experiment. Tissue specialisation, staining, plane of section, and contrast also affect visibility. State “not resolved/not in this section” rather than “absent”. Cardiac mitochondria density and onion mitosis are tissue-specific features. No single micrograph shows every textbook organelle; avoid marking pupils wrong for declining an unsupported label.

Keep each original scale bar attached to its own panel, preserve aspect ratio, and resize the bar with the image. Figure3A is light microscopy and3B–F TEM; do not call the full mixed-method composite one TEM image. Source letter abbreviations make some answers explicit; an assessment may need a separately declared, licensed adaptation, with panel/bar preserved and attribution retained. Before release, check legibility at actual document size. This asset review does not certify any future crop, label arrows, printed layout, practical availability, or final lesson content.

## Evidence integrity

The JSON manifest binds every candidate image to its exact observed public download URL and source-page SHA256. All five candidate image files were visually inspected. HTML snapshots support licence and identity checks. SHA256 below is for unchanged downloaded image bytes.

| File | SHA256 |
|---|---|
| CIL12594.jpg | `8cec9a5649ddff6bd2ea1ae207f076e9c54c1784f720e2063ad1f6a304d874bc` |
| CIL43552.jpg | `453f2c454f4cc303423c50468ea2ba2d44922f6bfb8f79e313ece84785ead486` |
| CIL39755.jpg | `9c879cf7402de95e51a4a9286f0447d06e6287e724de7b6bfb1aa17798d2a784` |
| Hsu2026_Fig3.png | `1001ef35df120d781231777b2e51ec7228e9f0583b970fba313287d41b536b98` |
| Hsu2026_Fig1.png | `2e4c296ff8532e42bb1cc6959f5cf55bcd6024ee0029da4a47fbb3a927efc2dc` |

Article HTML snapshot SHA256: `ddd0b3e32c10226cf49bc3f374691aee6d07b0973dc6cb879090c0cf9ef4f8ca`.

Primary image URLs for the plant TEM downloads:

- Figure3: https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs40529-026-00499-x/MediaObjects/40529_2026_499_Fig3_HTML.png
- Figure1: https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs40529-026-00499-x/MediaObjects/40529_2026_499_Fig1_HTML.png

**Final scoped disposition: PASS for licensed candidate suitability with stated caption/visibility limits. No content acceptance verdict.** The earlier microscopy-image blocker has a credible licensed route; author must implement the selected materials and undergo normal content/artifact review.

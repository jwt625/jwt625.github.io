# RFD-009: Infinera 1.6T PIC Interactive Component Map

## Status
**COMPLETE** - 2026-10-20

## Goal
An interactive page that pairs a generated schematic of the Infinera 1.6 Tb/s PIC with the full-resolution die micrograph. Hovering or selecting a component, a category (e.g. all SOAs, all monitor PDs), or a subsystem highlights it in both views. The page is embedded as an iframe in `_posts/2026-05-15-infinera-DP-64QAM.md`.

## Decisions (2026-10-20, from Wentao)
- Placement: standalone static page at `/infinera-pic-map/`, embedded in the post with an inserted iframe. The post is hand-edited: insert only, never regenerate.
- Image: full resolution (20000 x 19091 source), served as a WebP tile pyramid; only visible tiles load. Credit siliconpr0n as in the post.
- Granularity: every instance is traced individually (all TX and RX chains), and categories highlight all copies.
- Schematic: a generated SVG inside the interactive page only; no separate export.
- Mapping confidence: solid outline = labeled on the die or in the post; dashed = inferred from layout.

## Plan
- [x] Tile pyramid generator `infinera-pic-map/tools/make_tiles.py` (uv + Pillow), 512 px WebP q72, 7 levels (L6 = native), 16.1 MB total; `tiles/manifest.json`.
- [x] Layout analysis: 5 parallel tracing agents (TX unit 1, TX unit 2, RX signal, RX LO/WLL, test/die), then merged.
- [x] Component registry `infinera-pic-map/data.js` (window.PIC_DATA): 463 components, 303 optical connections. This file is the source of truth; edit it directly.
- [x] Schematic generated from the registry in `schematic.js` (role templates per TX chain / RX unit; wires linked to traced routes via the connection graph).
- [x] Viewer `index.html`: tile deep zoom + overlay SVG, modes component / category / subsystem, linked hover with dashed cross-pane links, pin + fly-to, tour (x2 per notch speed), foldable tree with tier buttons, narrow layout for the iframe.
- [x] Iframe inserted in the post below the image credits (insert only).
- [x] Fresh-context audit of identifications and topology; fixes applied.

## DevLog
### 2026-10-20
- Read the post and its annotated crops; plan written.
- The source JPEG carries EXIF orientation (LeftBottom). All coordinates and tiles use the displayed orientation (19091 x 20000).
- Viewer bugs found in headless verification and fixed: tiles stacked above the overlay (z-index), async image decoding dropped tiles in headless Chrome, page `buildSchematic` shadowed the global.
- Tracing fix: TX1 TM-chain I/Q combiner, tap and route shapes had been mirror-copied from TE1 onto the wrong side, and arm names disagreed with the die labels. Ids, labels and connections were right; shapes were swapped and names corrected.

#### Findings vs the post (from tracing; see component descs for evidence)
- TX light order: 1x2 then 2x 1x2 split in the centre channel, then the 4 arms go through the fast traveling-wave section at the top (next to the RF pads), then amplitude (xxA) and thermal phase (xxP) tuners, then I/Q combiners with TEIM/TEQM taps, IQ combiner, CPD tap, SOA, facet.
- Each TX laser: the top end feeds TE, the bottom end feeds TM (via a long loop). The phase section sits between the gain section and the bottom DBR.
- The TE and TM blocks of each TX unit are near mirror images about the laser axis. Arm order (west to east) is TE: I1 I2 Q2 Q1 and TM: I2 I1 Q1 Q2.
- RX: signal ports TE3 to TE1, TM3 to TM1, TE4 to TE2, TM4 to TM2. All signal paths are passive. Each hybrid is a two-section MMI with 3 dummy ports. RX PDs have no curled terminations (only the dummy ports do).
- RX LO lasers also have phase sections (PHASE/PHG pads). There is no common LO splitter: LO1 top end feeds TE1 and the WLL branch, bottom end feeds TM1 and a monitor PD; LO2 top end feeds TM2 and the WLL branch, bottom end feeds TE2 and a monitor PD.
- WLL: one facet port, a Y junction, then two InP sections (pads SH1/SH2) to each LO's top-end splitter. Light direction cannot be read from the layout. The post's injection-locking reading and an alternative (LO output tap to an off-chip wavelength locker, SH as per-laser gates) both fit.
- Die name reads TR6A_301. The middle-column 12-pad array relays TX DC lines to the package on the right. Isolation trenches are mostly not distinguishable optically (only two traced, inferred).
- Audit (fresh context): topology (a)-(d) confirmed, including fast section before the xxA/xxP tuners; ~110 shapes sampled, none off by more than ~50 px. Fixed: TM1 Q-combiner desc and I-arm route names, TESOA attribution (TX2 die label, not the post), "widely tunable" wording dropped, splitter category covers Y-junctions, TE2 I2P pad label, I1R pad-pair assignment marked inferred, WLL right-edge crossing caveat.

### 2026-10-21
- Feedback: schematic too colorful. Schematic devices now draw in neutral near-white (`SCH_NEUTRAL`, #c3c8cf); each device also has a category-colored copy that is shown only while it is highlighted (hover/pin/tour). Micrograph outlines, tree swatches and highlight overlays are unchanged.
- Follow-up: muted color is now a blend, 30% category color + 70% neutral (`SCH_TINT`), instead of plain near-white.
- Overlay fixes (TX unit 2): each TE2/TM2 arm route was one polyline from the 2nd-level splitter over the modulator and both tuners to the combiner, so it covered those devices in the micrograph hit layer and left the schematic wires unlinked. Split to match TX1: `wg_<arm>_up` (splitter -> RF section, cut at the modulator rect edge), `wg_<arm>_ret` (RF section -> amplitude tuner), `wg_<arm>_m` (phase tuner -> combiner); phase tuners got the TX1-style line from the amplitude-tuner end. Added `wg_mmi_i/q` (1st splitter -> 2nd-level splitters, the untraced gap under the die's TE2/TM2 text). Split `wg_i/q` at the monitor taps (+ `wg_i2iq/q2iq`) and `wg_out1` at the CPD tap (+ `wg_soa`). Modulator rects checked against the electrodes (TE2 x 6440-7420, TM2 8400-9350 on the die). Registry now 489 components, 329 connections; TX2 has 25 routes per chain like TX1. Schematic unlinked wires 67 -> 41 (remaining are device-to-device joins with no route, same as TX1).
- Micrograph hit order is now background (pads, trenches, test, marks) < routes < devices, so splitters, taps, combiners and ports that a route runs through stay hoverable. Headless check: 183/191 device shapes are hit at their center; the 8 others are RX hybrid outer rects whose main/secondary sections sit on top (intended). Trade-off: `tx1_wg_cavity` is now mostly under the TX1 laser sections (select it from the tree).

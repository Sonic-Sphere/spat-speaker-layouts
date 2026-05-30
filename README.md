# Sonic Sphere SPAT Speaker Layouts

Reference SpatGRIS speaker setup XML files for common multichannel, Dolby
Atmos-style, and Auro-3D layouts.

These files are intended as geometry/reference assets. They are speaker setup
XMLs, not `.spatgris` projects, audio files, render kernels, Dolby Atmos, or Auro-3D
master files.

## What Is Here

- `dolby-multichannel-and-other-speaker-layouts/`: SpatGRIS speaker setup XML files.
- `sonic-sphere-speaker-layouts/`: imported Fey/Fëy and Loveburn source XML speaker setups.
- `layout_geometry.csv`: the same layout data as a flat table.
- `scripts/generate_reference_spatgris_layouts.py`: the generator used to build
  the XML and CSV files.

The files use the legacy SpatGRIS `SPEAKER_N` XML shape (`VERSION="3.3.7"`)
because the bundled SpatGRIS templates use that format and SpatGRIS 4.0.3 still
loads it. LFE entries are marked `DIRECT_OUT_ONLY="1"` so the dome spatializer
ignores them.

## What Is SPAT?

SPAT is short for spatialization: placing and rendering sound in a physical or
virtual space instead of treating audio as only left/right stereo. In this repo,
SPAT refers to the speaker-geometry side of that work.

[SpatGRIS](https://github.com/GRIS-UdeM/SpatGRIS) is an open-source spatial audio
tool from GRIS/SAT. It can render sources to arbitrary 2D and 3D speaker layouts
using spatialization algorithms such as VBAP/MBAP, and it stores speaker layouts
as XML files like the ones in this repo.

## How To Use These Layouts

1. Open SpatGRIS.
2. Open the speaker setup editor or speaker setup load dialog.
3. Load one of the XML files from `dolby-multichannel-and-other-speaker-layouts/`.
4. Use the file as a reference layout, visualization target, or geometry source
   for downstream renderers such as Sonic Sphere/Orbisonic tooling.

The `sonic-sphere-speaker-layouts/` files are preserved source assets rather than generated
Dolby-reference layouts. Use them when you need the original Fey/Fëy or Loveburn
speaker geometry.

For programmatic use, prefer `layout_geometry.csv`. It includes the layout name,
patch number, channel label, azimuth, elevation, Cartesian position, and LFE
direct-out flag for every speaker.

LFE handling: generated layouts with `.1` channels include an LFE entry at patch
4, marked direct-out-only.

## Coordinate Convention

- `+x` is listener-right.
- `+y` is front/screen.
- `+z` is up.
- Negative azimuth is listener-left, positive azimuth is listener-right.
- Non-LFE dome speakers are normalized to radius 1.0.

## Source Data And Standards Links

- Dolby Atmos speaker setup guide:
  https://www.dolby.com/about/support/guide/dolby-atmos-speaker-setup/
- Dolby 5.1.2 overhead setup:
  https://www.dolby.com/en-in/about/support/guide/setup-guides/5.1.2-overhead-speaker-placement
- Dolby 7.1.2 overhead setup:
  https://www.dolby.com/en-in/about/support/guide/setup-guides/7.1.2-overhead-speaker-placement
- Dolby 9.1.6 overhead setup:
  https://www.dolby.com/en-in/about/support/guide/setup-guides/9.1.6-overhead-speaker-placement
- Dolby Atmos Home Theater Installation Guidelines:
  https://professional.dolby.com/siteassets/tv/home/dolby-atmos/atmos-installation-guidelines-121318_r3.1.pdf
- Dolby mix-room guidance:
  https://professionalsupport.dolby.com/s/article/How-to-Design-a-Dolby-Atmos-Mix-Room
- Auro-3D Home Theater Setup Guidelines, Rev. 12, 2024 May 16:
  https://www.auro-3d.com/wp-content/uploads/2024/05/Auro-3D-Home-Theater-Setup-Guidelines-v12-20240516.pdf
- SpatGRIS source project:
  https://github.com/GRIS-UdeM/SpatGRIS

Existing SpatGRIS ITU/BS templates were used as a local sanity check for channel
families, LFE direct-out handling, Auro-3D layout geometry, and the `SPEAKER_N`
XML format.

## Files

| Layout | XML Speakers | File | Basis |
| --- | ---: | --- | --- |
| Mono 1.0 | 1 | `dolby-multichannel-and-other-speaker-layouts/mono_1_0_spatgris_speaker_setup.xml` | Center-front mono reference. |
| Stereo 2.0 | 2 | `dolby-multichannel-and-other-speaker-layouts/stereo_2_0_spatgris_speaker_setup.xml` | Dolby/ITU front stereo pair nominally at +/-30 degrees from center. |
| Binaural 2.0 Narrow | 2 | `dolby-multichannel-and-other-speaker-layouts/binaural_2_0_narrow_spatgris_speaker_setup.xml` | Utility narrow stereo reference from the local workplan; not a Dolby room-speaker standard. |
| Quad 4.0 | 4 | `dolby-multichannel-and-other-speaker-layouts/quad_4_0_spatgris_speaker_setup.xml` | Symmetric quad reference layout. |
| 5.1 | 6 | `dolby-multichannel-and-other-speaker-layouts/5_1_spatgris_speaker_setup.xml` | Dolby/ITU 5.1 basis: L/R +/-30 degrees, surround pair about +/-110 degrees, LFE direct. |
| 5.1.2 | 8 | `dolby-multichannel-and-other-speaker-layouts/5_1_2_spatgris_speaker_setup.xml` | Dolby 5.1.2 overhead basis: 5.1 bed plus left/right top-middle overhead pair. |
| 5.1.4 | 10 | `dolby-multichannel-and-other-speaker-layouts/5_1_4_spatgris_speaker_setup.xml` | Dolby 5.1.4 overhead basis: 5.1 bed plus top-front and top-rear pairs. |
| 7.1 | 8 | `dolby-multichannel-and-other-speaker-layouts/7_1_spatgris_speaker_setup.xml` | Dolby/ITU 7.1 basis: side surrounds at +/-90 degrees and rear surrounds at +/-135 degrees. |
| 7.1.2 | 10 | `dolby-multichannel-and-other-speaker-layouts/7_1_2_spatgris_speaker_setup.xml` | Dolby 7.1.2 overhead basis: 7.1 bed plus left/right top-middle overhead pair. |
| 7.1.4 | 12 | `dolby-multichannel-and-other-speaker-layouts/7_1_4_spatgris_speaker_setup.xml` | Dolby 7.1.4 reference basis: 7.1 bed plus top-front and top-rear overhead pairs. |
| 9.1.4 | 14 | `dolby-multichannel-and-other-speaker-layouts/9_1_4_spatgris_speaker_setup.xml` | Dolby 9.1.4 basis: 7.1.4 plus left/right wide speakers. |
| 9.1.6 | 16 | `dolby-multichannel-and-other-speaker-layouts/9_1_6_spatgris_speaker_setup.xml` | Dolby 9.1.6 basis: 9.1.4 plus left/right top-middle overhead pair. |
| Harmony Bloom 8ch | 8 | `dolby-multichannel-and-other-speaker-layouts/harmony_bloom_8ch_spatgris_speaker_setup.xml` | Music-production circular utility layout from the local workplan; not a Dolby room-speaker standard. |
| Auro-3D 8.0 | 8 | `dolby-multichannel-and-other-speaker-layouts/auro_8_0_spatgris_speaker_setup.xml` | Auro-3D 8.0 (4.0+4H): two quadraphonic layers, lower layer at 0 degrees and height layer at +30 degrees. |
| Auro-3D 9.1 | 10 | `dolby-multichannel-and-other-speaker-layouts/auro_9_1_spatgris_speaker_setup.xml` | Auro-3D 9.1 (5.1+4H): 5.1 lower layer plus height front and height surround pairs at +30 degrees. |
| Auro-3D 10.1 | 11 | `dolby-multichannel-and-other-speaker-layouts/auro_10_1_spatgris_speaker_setup.xml` | Auro-3D 10.1 (5.1+4H+T): Auro 9.1 plus top Voice of God channel at +90 degrees. |
| Auro-3D 11.1 (5.1+5H+T) | 12 | `dolby-multichannel-and-other-speaker-layouts/auro_11_1_5_1_5h_t_spatgris_speaker_setup.xml` | Auro-3D 11.1 (5.1+5H+T): Auro 10.1 plus height center at 0 degrees azimuth and +30 degrees elevation. |
| Auro-3D 11.1 (7.1+4H) | 12 | `dolby-multichannel-and-other-speaker-layouts/auro_11_1_7_1_4h_spatgris_speaker_setup.xml` | Auro-3D 11.1 (7.1+4H): 7.1 lower layer with surrounds at +/-110 degrees, backs at +/-150 degrees, and four height speakers. |
| Auro-3D 13.1 | 14 | `dolby-multichannel-and-other-speaker-layouts/auro_13_1_spatgris_speaker_setup.xml` | Auro-3D 13.1 (7.1+5H+T): 7.1 lower layer, height front/surround/center layer at +30 degrees, and top at +90 degrees. |

## Imported Source Layouts

These were imported from the local `All projects assets` folder and preserved
with the revised titles already used there.

| Layout | XML Speakers | Direct-Out Channels | File |
| --- | ---: | ---: | --- |
| Fey/Fëy without LFE | 30 | 0 | `sonic-sphere-speaker-layouts/fey/SPAT Fey speaker setup - without LFE.xml` |
| Fey/Fëy with LFE channel | 31 | 1 | `sonic-sphere-speaker-layouts/fey/SPAT Fey speaker setup - with LFE channel.xml` |
| Loveburn speaker setup | 54 | 2 | `sonic-sphere-speaker-layouts/loveburn/Loveburn speaker setup.xml` |

See `sonic-sphere-speaker-layouts/README.md` for the import notes.

## Notes

- `Binaural 2.0 Narrow` and `Harmony Bloom 8ch` are utility/music-production
  layouts, not Dolby or Auro room-speaker standards.
- Auro-3D layouts use the nominal positions from the Auro-3D Home Theater Setup
  Guidelines: lower-layer fronts at +/-30 degrees, surrounds at +/-110 degrees,
  backs at +/-150 degrees, height layer at +30 degrees, and top at +90 degrees.
- The generated XML files include comments naming the logical channel at each
  patch number.

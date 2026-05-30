# Sonic Sphere SPAT Speaker Layouts

Reference SpatGRIS speaker setup XML files for common multichannel and Dolby
Atmos-style layouts, plus the Sonic Sphere 30.1 physical target layout.

These files are intended as geometry/reference assets. They are speaker setup
XMLs, not `.spatgris` projects, audio files, render kernels, or Dolby Atmos
master files.

## What Is Here

- `speaker_setups/`: SpatGRIS speaker setup XML files.
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
3. Load one of the XML files from `speaker_setups/`.
4. Use the file as a reference layout, visualization target, or geometry source
   for downstream renderers such as Sonic Sphere/Orbisonic tooling.

For programmatic use, prefer `layout_geometry.csv`. It includes the layout name,
patch number, channel label, azimuth, elevation, Cartesian position, and LFE
direct-out flag for every speaker.

LFE handling: layouts with `.1` channels include an LFE entry at patch 4, marked
direct-out-only. The Sonic Sphere 30.1 physical target uses patch 31 for LFE.

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
- SpatGRIS source project:
  https://github.com/GRIS-UdeM/SpatGRIS

Existing SpatGRIS ITU/BS templates were used as a local sanity check for channel
families, LFE direct-out handling, and the `SPEAKER_N` XML format.

## Files

| Layout | XML Speakers | File | Basis |
| --- | ---: | --- | --- |
| Sonic Sphere 30.1 | 31 | `speaker_setups/sonic_sphere_30_1_spatgris_speaker_setup.xml` | Project-specific Sonic Sphere geometry from spatgris_layout_workplan.md; LFE is direct-out-only. |
| Mono 1.0 | 1 | `speaker_setups/mono_1_0_spatgris_speaker_setup.xml` | Center-front mono reference. |
| Stereo 2.0 | 2 | `speaker_setups/stereo_2_0_spatgris_speaker_setup.xml` | Dolby/ITU front stereo pair nominally at +/-30 degrees from center. |
| Binaural 2.0 Narrow | 2 | `speaker_setups/binaural_2_0_narrow_spatgris_speaker_setup.xml` | Utility narrow stereo reference from the local workplan; not a Dolby room-speaker standard. |
| Quad 4.0 | 4 | `speaker_setups/quad_4_0_spatgris_speaker_setup.xml` | Symmetric quad reference layout. |
| 5.1 | 6 | `speaker_setups/5_1_spatgris_speaker_setup.xml` | Dolby/ITU 5.1 basis: L/R +/-30 degrees, surround pair about +/-110 degrees, LFE direct. |
| 5.1.2 | 8 | `speaker_setups/5_1_2_spatgris_speaker_setup.xml` | Dolby 5.1.2 overhead basis: 5.1 bed plus left/right top-middle overhead pair. |
| 5.1.4 | 10 | `speaker_setups/5_1_4_spatgris_speaker_setup.xml` | Dolby 5.1.4 overhead basis: 5.1 bed plus top-front and top-rear pairs. |
| 7.1 | 8 | `speaker_setups/7_1_spatgris_speaker_setup.xml` | Dolby/ITU 7.1 basis: side surrounds at +/-90 degrees and rear surrounds at +/-135 degrees. |
| 7.1.2 | 10 | `speaker_setups/7_1_2_spatgris_speaker_setup.xml` | Dolby 7.1.2 overhead basis: 7.1 bed plus left/right top-middle overhead pair. |
| 7.1.4 | 12 | `speaker_setups/7_1_4_spatgris_speaker_setup.xml` | Dolby 7.1.4 reference basis: 7.1 bed plus top-front and top-rear overhead pairs. |
| 9.1.4 | 14 | `speaker_setups/9_1_4_spatgris_speaker_setup.xml` | Dolby 9.1.4 basis: 7.1.4 plus left/right wide speakers. |
| 9.1.6 | 16 | `speaker_setups/9_1_6_spatgris_speaker_setup.xml` | Dolby 9.1.6 basis: 9.1.4 plus left/right top-middle overhead pair. |
| Harmony Bloom 8ch | 8 | `speaker_setups/harmony_bloom_8ch_spatgris_speaker_setup.xml` | Music-production circular utility layout from the local workplan; not a Dolby room-speaker standard. |

## Notes

- `Binaural 2.0 Narrow` and `Harmony Bloom 8ch` are utility/music-production
  layouts, not Dolby room-speaker standards.
- `Sonic Sphere 30.1` is the physical target sphere layout, not a consumer
  Dolby playback room layout.
- The generated XML files include comments naming the logical channel at each
  patch number.

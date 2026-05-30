#!/usr/bin/env python3
"""Generate SpatGRIS speaker setup XMLs for reference multichannel layouts."""

from __future__ import annotations

import csv
import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


# When this script lives in the SpatGRIS checkout, write the pack under
# presets/dolby_reference_layouts. When it lives inside the standalone published
# repo, write the pack at the repo root.
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "presets" / "dolby_reference_layouts" if (ROOT / "presets").exists() else ROOT
SPEAKER_SETUP_DIR = OUTPUT_DIR / "dolby-multichannel-and-other-speaker-layouts"
GEOMETRY_CSV = OUTPUT_DIR / "layout_geometry.csv"
README = OUTPUT_DIR / "README.md"
GENERATOR_COPY = OUTPUT_DIR / "scripts" / Path(__file__).name


@dataclass(frozen=True)
class Speaker:
    patch: int
    label: str
    azimuth: float
    elevation: float
    direct_out_only: bool = False
    note: str = ""


@dataclass(frozen=True)
class Layout:
    slug: str
    display_name: str
    speakers: tuple[Speaker, ...]
    standard_basis: str
    notes: str = ""


def sph_to_cart(azimuth: float, elevation: float) -> tuple[float, float, float]:
    """Convert SpatGRIS-style azimuth/elevation to Cartesian.

    Coordinates match the local SpatGRIS guide:
    +x is right, +y is front, +z is up. Negative azimuth is listener-left.
    """
    az = math.radians(azimuth)
    el = math.radians(elevation)
    horizontal = math.cos(el)
    return (
        math.sin(az) * horizontal,
        math.cos(az) * horizontal,
        math.sin(el),
    )


def fmt_float(value: float) -> str:
    if abs(value) < 5e-12:
        value = 0.0
    return f"{value:.10f}"


def lfe(patch: int = 4) -> Speaker:
    # Direct-out LFE is exempt from dome radius checks in SpatGRIS. Position is visual only.
    return Speaker(patch, "LFE", -45.0, 0.0, True, "direct out only")


def front_lrc() -> tuple[Speaker, Speaker, Speaker, Speaker]:
    return (
        Speaker(1, "L", -30.0, 0.0),
        Speaker(2, "R", 30.0, 0.0),
        Speaker(3, "C", 0.0, 0.0),
        lfe(4),
    )


def surround_5_1(start_patch: int = 5) -> tuple[Speaker, Speaker]:
    return (
        Speaker(start_patch, "Ls", -110.0, 0.0),
        Speaker(start_patch + 1, "Rs", 110.0, 0.0),
    )


def surround_7_1(start_patch: int = 5) -> tuple[Speaker, Speaker, Speaker, Speaker]:
    return (
        Speaker(start_patch, "Lss", -90.0, 0.0),
        Speaker(start_patch + 1, "Rss", 90.0, 0.0),
        Speaker(start_patch + 2, "Lrs", -135.0, 0.0),
        Speaker(start_patch + 3, "Rrs", 135.0, 0.0),
    )


def top_front(start_patch: int) -> tuple[Speaker, Speaker]:
    return (
        Speaker(start_patch, "Ltf", -45.0, 45.0),
        Speaker(start_patch + 1, "Rtf", 45.0, 45.0),
    )


def top_middle(start_patch: int) -> tuple[Speaker, Speaker]:
    return (
        Speaker(start_patch, "Ltm", -90.0, 45.0),
        Speaker(start_patch + 1, "Rtm", 90.0, 45.0),
    )


def top_rear(start_patch: int) -> tuple[Speaker, Speaker]:
    return (
        Speaker(start_patch, "Ltr", -135.0, 45.0),
        Speaker(start_patch + 1, "Rtr", 135.0, 45.0),
    )


def front_wide(start_patch: int) -> tuple[Speaker, Speaker]:
    return (
        Speaker(start_patch, "Lw", -60.0, 0.0),
        Speaker(start_patch + 1, "Rw", 60.0, 0.0),
    )


def auro_surround_7_1(start_patch: int = 5) -> tuple[Speaker, Speaker, Speaker, Speaker]:
    return (
        Speaker(start_patch, "Ls", -110.0, 0.0),
        Speaker(start_patch + 1, "Rs", 110.0, 0.0),
        Speaker(start_patch + 2, "Lb", -150.0, 0.0),
        Speaker(start_patch + 3, "Rb", 150.0, 0.0),
    )


def auro_height_quad(start_patch: int) -> tuple[Speaker, Speaker, Speaker, Speaker]:
    return (
        Speaker(start_patch, "HL", -30.0, 30.0),
        Speaker(start_patch + 1, "HR", 30.0, 30.0),
        Speaker(start_patch + 2, "HLs", -110.0, 30.0),
        Speaker(start_patch + 3, "HRs", 110.0, 30.0),
    )


def auro_top(start_patch: int) -> tuple[Speaker]:
    return (Speaker(start_patch, "T", 0.0, 90.0, False, "Voice of God top channel"),)


def auro_height_center(start_patch: int) -> tuple[Speaker]:
    return (Speaker(start_patch, "HC", 0.0, 30.0),)


LAYOUTS: tuple[Layout, ...] = (
    Layout(
        "mono_1_0",
        "Mono 1.0",
        (Speaker(1, "C", 0.0, 0.0),),
        "Center-front mono reference.",
    ),
    Layout(
        "stereo_2_0",
        "Stereo 2.0",
        (Speaker(1, "L", -30.0, 0.0), Speaker(2, "R", 30.0, 0.0)),
        "Dolby/ITU front stereo pair nominally at +/-30 degrees from center.",
    ),
    Layout(
        "binaural_2_0_narrow",
        "Binaural 2.0 Narrow",
        (Speaker(1, "LeftEar", -15.0, 0.0), Speaker(2, "RightEar", 15.0, 0.0)),
        "Utility narrow stereo reference from the local workplan; not a Dolby room-speaker standard.",
    ),
    Layout(
        "quad_4_0",
        "Quad 4.0",
        (
            Speaker(1, "FL", -45.0, 0.0),
            Speaker(2, "FR", 45.0, 0.0),
            Speaker(3, "RL", -135.0, 0.0),
            Speaker(4, "RR", 135.0, 0.0),
        ),
        "Symmetric quad reference layout.",
    ),
    Layout(
        "5_1",
        "5.1",
        front_lrc() + surround_5_1(),
        "Dolby/ITU 5.1 basis: L/R +/-30 degrees, surround pair about +/-110 degrees, LFE direct.",
    ),
    Layout(
        "5_1_2",
        "5.1.2",
        front_lrc() + surround_5_1() + top_middle(7),
        "Dolby 5.1.2 overhead basis: 5.1 bed plus left/right top-middle overhead pair.",
    ),
    Layout(
        "5_1_4",
        "5.1.4",
        front_lrc() + surround_5_1() + top_front(7) + top_rear(9),
        "Dolby 5.1.4 overhead basis: 5.1 bed plus top-front and top-rear pairs.",
    ),
    Layout(
        "7_1",
        "7.1",
        front_lrc() + surround_7_1(),
        "Dolby/ITU 7.1 basis: side surrounds at +/-90 degrees and rear surrounds at +/-135 degrees.",
    ),
    Layout(
        "7_1_2",
        "7.1.2",
        front_lrc() + surround_7_1() + top_middle(9),
        "Dolby 7.1.2 overhead basis: 7.1 bed plus left/right top-middle overhead pair.",
    ),
    Layout(
        "7_1_4",
        "7.1.4",
        front_lrc() + surround_7_1() + top_front(9) + top_rear(11),
        "Dolby 7.1.4 reference basis: 7.1 bed plus top-front and top-rear overhead pairs.",
    ),
    Layout(
        "9_1_4",
        "9.1.4",
        front_lrc() + front_wide(5) + surround_7_1(7) + top_front(11) + top_rear(13),
        "Dolby 9.1.4 basis: 7.1.4 plus left/right wide speakers.",
    ),
    Layout(
        "9_1_6",
        "9.1.6",
        front_lrc() + front_wide(5) + surround_7_1(7) + top_front(11) + top_rear(13) + top_middle(15),
        "Dolby 9.1.6 basis: 9.1.4 plus left/right top-middle overhead pair.",
        "Channel order preserves the local workplan: top-middle is appended after top-rear.",
    ),
    Layout(
        "harmony_bloom_8ch",
        "Harmony Bloom 8ch",
        tuple(Speaker(i + 1, f"HB{i + 1}", az, 0.0) for i, az in enumerate((0, 45, 90, 135, 180, -135, -90, -45))),
        "Music-production circular utility layout from the local workplan; not a Dolby room-speaker standard.",
    ),
    Layout(
        "auro_8_0",
        "Auro-3D 8.0",
        (
            Speaker(1, "L", -30.0, 0.0),
            Speaker(2, "R", 30.0, 0.0),
            Speaker(3, "Ls", -110.0, 0.0),
            Speaker(4, "Rs", 110.0, 0.0),
        )
        + auro_height_quad(5),
        "Auro-3D 8.0 (4.0+4H): two quadraphonic layers, lower layer at 0 degrees and height layer at +30 degrees.",
    ),
    Layout(
        "auro_9_1",
        "Auro-3D 9.1",
        front_lrc() + surround_5_1() + auro_height_quad(7),
        "Auro-3D 9.1 (5.1+4H): 5.1 lower layer plus height front and height surround pairs at +30 degrees.",
    ),
    Layout(
        "auro_10_1",
        "Auro-3D 10.1",
        front_lrc() + surround_5_1() + auro_height_quad(7) + auro_top(11),
        "Auro-3D 10.1 (5.1+4H+T): Auro 9.1 plus top Voice of God channel at +90 degrees.",
    ),
    Layout(
        "auro_11_1_5_1_5h_t",
        "Auro-3D 11.1 (5.1+5H+T)",
        front_lrc() + surround_5_1() + auro_height_quad(7) + auro_top(11) + auro_height_center(12),
        "Auro-3D 11.1 (5.1+5H+T): Auro 10.1 plus height center at 0 degrees azimuth and +30 degrees elevation.",
    ),
    Layout(
        "auro_11_1_7_1_4h",
        "Auro-3D 11.1 (7.1+4H)",
        front_lrc() + auro_surround_7_1(5) + auro_height_quad(9),
        "Auro-3D 11.1 (7.1+4H): 7.1 lower layer with surrounds at +/-110 degrees, backs at +/-150 degrees, and four height speakers.",
    ),
    Layout(
        "auro_13_1",
        "Auro-3D 13.1",
        front_lrc() + auro_surround_7_1(5) + auro_height_quad(9) + auro_top(13) + auro_height_center(14),
        "Auro-3D 13.1 (7.1+5H+T): 7.1 lower layer, height front/surround/center layer at +30 degrees, and top at +90 degrees.",
    ),
)


def build_xml(layout: Layout) -> ET.ElementTree:
    root = ET.Element(
        "SPEAKER_SETUP",
        {
            "VERSION": "3.3.7",
            "SPAT_MODE": "Dome",
            "DIFFUSION": "0.0",
            "GENERAL_MUTE": "0",
        },
    )
    root.append(ET.Comment(f" {layout.display_name} "))
    root.append(ET.Comment(" Coordinates: +x right, +y front, +z up; negative azimuth is listener-left. "))
    root.append(ET.Comment(f" Basis: {layout.standard_basis} "))
    if layout.notes:
        root.append(ET.Comment(f" Note: {layout.notes} "))

    for speaker in layout.speakers:
        elem = ET.SubElement(
            root,
            f"SPEAKER_{speaker.patch}",
            {
                "STATE": "normal",
                "GAIN": "0.0",
                "DIRECT_OUT_ONLY": "1" if speaker.direct_out_only else "0",
            },
        )
        elem.append(ET.Comment(f" {speaker.label}: az={speaker.azimuth:g}, el={speaker.elevation:g}{', ' + speaker.note if speaker.note else ''} "))
        if speaker.direct_out_only:
            # Match bundled SpatGRIS direct-out templates: visual point only, outside unit dome.
            x, y, z = (-1.0, 1.0, 0.0)
        else:
            x, y, z = sph_to_cart(speaker.azimuth, speaker.elevation)
        ET.SubElement(
            elem,
            "POSITION",
            {
                "X": fmt_float(x),
                "Y": fmt_float(y),
                "Z": fmt_float(z),
            },
        )
    return ET.ElementTree(root)


def indent(element: ET.Element, level: int = 0) -> None:
    space = "\n" + level * "  "
    child_space = "\n" + (level + 1) * "  "
    children = list(element)
    if children:
        if not element.text or not element.text.strip():
            element.text = child_space
        for child in children:
            indent(child, level + 1)
        if not children[-1].tail or not children[-1].tail.strip():
            children[-1].tail = space
    if level and (not element.tail or not element.tail.strip()):
        element.tail = space


def write_xml(layout: Layout) -> Path:
    tree = build_xml(layout)
    indent(tree.getroot())
    path = SPEAKER_SETUP_DIR / f"{layout.slug}_spatgris_speaker_setup.xml"
    tree.write(path, encoding="UTF-8", xml_declaration=True)
    path.write_text(path.read_text(encoding="UTF-8").replace("<?xml version='1.0' encoding='UTF-8'?>", '<?xml version="1.0" encoding="UTF-8"?>'), encoding="UTF-8")
    return path


def write_geometry_csv() -> None:
    with GEOMETRY_CSV.open("w", newline="", encoding="UTF-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "layout",
                "patch",
                "label",
                "azimuth_degrees",
                "elevation_degrees",
                "x",
                "y",
                "z",
                "direct_out_only",
                "note",
            ]
        )
        for layout in LAYOUTS:
            for speaker in layout.speakers:
                if speaker.direct_out_only:
                    x, y, z = (-1.0, 1.0, 0.0)
                else:
                    x, y, z = sph_to_cart(speaker.azimuth, speaker.elevation)
                writer.writerow(
                    [
                        layout.slug,
                        speaker.patch,
                        speaker.label,
                        speaker.azimuth,
                        speaker.elevation,
                        fmt_float(x),
                        fmt_float(y),
                        fmt_float(z),
                        int(speaker.direct_out_only),
                        speaker.note,
                    ]
                )


def write_readme(paths: list[Path]) -> None:
    table_rows = []
    for layout, path in zip(LAYOUTS, paths, strict=True):
        table_rows.append(
            f"| {layout.display_name} | {len(layout.speakers)} | `{path.relative_to(OUTPUT_DIR)}` | {layout.standard_basis} |"
        )

    content = f"""# Sonic Sphere SPAT Speaker Layouts

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
{chr(10).join(table_rows)}

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
"""
    README.write_text(content, encoding="UTF-8")


def write_generator_copy() -> None:
    source = Path(__file__).resolve()
    target = GENERATOR_COPY.resolve()
    if source == target:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="UTF-8"), encoding="UTF-8")


def main() -> None:
    SPEAKER_SETUP_DIR.mkdir(parents=True, exist_ok=True)
    paths = [write_xml(layout) for layout in LAYOUTS]
    write_geometry_csv()
    write_readme(paths)
    write_generator_copy()
    print(f"Generated {len(paths)} XML speaker setup files in {SPEAKER_SETUP_DIR}")


if __name__ == "__main__":
    main()

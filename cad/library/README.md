# Persistent hardware CAD library

This directory is the reproducible hardware-reference boundary for the PCB
CNC. The authoritative registry is
[`hardware-model-manifest.json`](hardware-model-manifest.json). Its stable
`HW-*` IDs are used by the master assembly and identify the model source,
critical dimensions, verification state, and publication treatment.

The current library contains project-generated build123d reference/interface
models under [`parametric_models.py`](parametric_models.py). No downloaded
third-party CAD file is currently vendored. This is deliberate: HIWIN,
SycoTec, Omron, and MISUMI CAD offerings were found, but their public
redistribution terms are not sufficiently clear for this repository. Arduino
open-hardware references are attributed, while the committed mechanical model
is still project-generated.

## Category layout

| Directory | Contents |
| --- | --- |
| `linear_motion/` | MGN12/MGN12H and MGN9/MGN9H guide interfaces |
| `leadscrews/` | T8x4 and T8x2 non-helical screw envelopes |
| `leadnuts/` | T8 anti-backlash nut envelope |
| `bearings/` | 608-class bearing reference |
| `couplers/` | 5-to-8 mm flexible coupling envelope |
| `motors/` | Generic owner-stock NEMA17 interface |
| `spindle/` | SycoTec 5045 AC-ER11 candidate envelope |
| `electronics/` | Arduino Mega and provisional CNC Shield |
| `switches/` | Omron D2F family reference |
| `fasteners/` | Representative M4 envelope |

Category directories contain provenance/readme boundaries; the parametric
builders remain centralized so dimensions are not duplicated. The master
assembly imports the stable wrappers from this library rather than selecting
generic hardware builders directly.

Validate the manifest with:

```text
python -B tools/validate_hardware_library.py
```

External CAD may be added only after its license, attribution, deterministic
filename, checksum, and verification record are added to the manifest and the
third-party notice. A source file's presence in a vendor download page is not
by itself permission to redistribute it.

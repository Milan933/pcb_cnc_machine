# Precision CAD examples and methodology exercises

These are reasoning examples, not production designs. They demonstrate how to move from visual modeling to engineering CAD without embedding project-specific dimensions.

## Good versus bad examples

### 1. NEMA17 motor bracket

- **Bad:** A rectangular block with a guessed four-hole pattern and an oversized shaft opening.
- **Good:** A documented motor interface frame controls mounting pitch, shaft axis, body envelope, connector clearance, reaction moment, boss/load path, fastener access, manufacturing process, and service removal. Actual motor dimensions are classified by source confidence.

### 2. Bearing housing

- **Bad:** A cylinder is subtracted from a block because it resembles a bearing seat.
- **Good:** Bore/OD/width and fit are sourced, the housing datum and shoulder are defined, axial retention is explicit, runout/coaxiality and inspection are specified, and replacement access is preserved.

### 3. Linear-rail mounting structure

- **Bad:** A rail is placed at a visually convenient height on a thin plate.
- **Good:** A continuous datum seat, carriage spacing, moment reaction, preload, parallelism, fastener sequence, lubrication, travel limits, and replacement path are defined and reviewed in section.

### 4. Shaft supported by two bearings

- **Bad:** Both bearing outer rings are clamped axially and a flexible coupler is expected to absorb all alignment error.
- **Good:** One support locates axial load, the other permits the required movement, shaft shoulders/retention are explicit, thermal and assembly variation are accommodated, and the coupler is sized only for torque/misalignment.

### 5. Two-part structural assembly

- **Bad:** A long beam is split at its midpoint with flat faces and screws expected to carry all shear.
- **Good:** Split location follows moment, shear, datum continuity, process orientation, and inspection. Keys/shoulders carry location and shear; fasteners clamp; the assembly can be tightened and inspected.

### 6. CNC-machined aluminum plate

- **Bad:** A deep square pocket, tight universal tolerances, and hidden holes are modeled without a stock/setup/tool plan.
- **Good:** Stock and datums, setups, workholding, cutter diameter, internal radii, tool reach, hole process, tolerances, surface requirements, and inspection method are defined before detailed features.

### 7. FDM structural bracket

- **Bad:** Weak layer orientation is retained and infill is increased to compensate.
- **Good:** Load direction drives print orientation, perimeters and walls carry the load, bosses connect to ribs, overhang/support/warping risks are controlled, and fit/insert dimensions are coupon-validated.

### 8. Electronics enclosure

- **Bad:** A box with a board-sized cavity and decorative vents.
- **Good:** Board datum, connector/cable envelopes, thermal path, fastener/insertion method, cover retention, gasket or clearance, assembly order, inspection, and service removal are defined.

## Required methodology exercises

For each exercise record requirements, datums, interfaces, critical dimensions, manufacturing process, tolerances, assembly, and validation. Do not produce CNC geometry as part of these exercises.

### A. Precision NEMA17 mounting plate

Use a generic motor interface envelope. Define the shaft axis and mounting datum, classify all dimensions, check connector/fastener access and moment load, choose material/process, assign only functional tolerances, and specify a hole-pattern/shaft-axis inspection method.

### B. Shaft supported by two bearings with axial location

Define radial and axial load cases, shaft datum, bearing spacing, locating/floating roles, shoulders, retention, thermal movement, coupler load, assembly sequence, and dial-indicator or gauge checks.

### C. Linear rail mounted to a structural beam

Define rail datum and beam reference, carriage spacing and moment loads, seat continuity, parallelism, preload, fastener tightening order, lubrication/service access, end stops, and a straightness/parallelism inspection plan.

### D. CNC-machined bearing block

Define stock, machining datums, setup count, workholding, cutter access, pocket/bore tools, internal radii, bearing fit, perpendicularity/coaxiality intent, deburring, and a bore/face inspection method.

### E. FDM structural bracket with heat-set inserts

Define force entry/reaction, layer orientation, perimeter/wall strategy, boss/rib geometry, insert supplier-dependent dimensions, pilot/depth/edge assumptions, insertion-tool access, print compensation, coupon tests, and post-print fit inspection.

## Exercise conclusion

The methodology test is successful only when the design can explain its dimensions, interfaces, load path, process, tolerance, assembly, and inspection evidence. A plausible picture or valid export is not the completion condition.

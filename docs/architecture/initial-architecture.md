# Initial architecture

This document defines boundaries and priorities before selecting detailed
components. It is not a mechanical layout.

## Functional chain

The intended engineering chain is:

requirements -> centralized parameters -> individual parametric parts ->
deterministic assembly -> validation -> manufacturing exports.

Purchased hardware is represented by controlled envelopes and interfaces. It
must not force the frame to use unsuitable geometry merely because it is
already owned.

## Mechanical priority

The primary force loop is the tool point -> spindle mount -> Z carriage ->
gantry or supported moving structure -> base -> workholding -> PCB. The
architecture should shorten and stiffen this loop, especially in Z, and should
avoid relying on a tall compliant stack of adapters.

The printed frame is expected to use closed sections, monocoque skins, ribs,
gussets, triangulation, and distributed metal interfaces where needed. Rails,
screws, bearings, spindle hardware, fasteners, inserts, and couplers may be
metal when their function requires it.

## Process interfaces

### Workholding and spoilboard

The workholding concept must hold thin PCB stock without bending it, permit
repeatable registration, expose a probe datum, and allow a worn spoilboard to
be replaced or resurfaced. The final method is unresolved.

### Probing and height mapping

The architecture must provide a probe input and a mechanically stable probing
datum. Height mapping must be treated as a measured coordinate transform:

1. establish the machine and PCB datums;
2. probe a documented grid or adaptive set;
3. record the map with machine and job metadata;
4. verify the map is valid for the clamped board;
5. apply compensation only within the measured region and toolpath policy.

Probe hardware, map density, interpolation, and firmware/toolpath ownership
are unresolved.

### PCB processes

- Isolation routing needs low runout, a stiff short tool path, shallow and
  repeatable depth, and a stable board surface.
- Drilling needs axial alignment, controlled retracts, adequate spindle speed,
  and a hole-size/runout acceptance test.
- Outline cutting needs predictable depth, board support, chip clearance, and
  a workholding strategy that remains secure through the final pass.

## Control boundary

The controller, firmware, stepper drivers, spindle control, limit switches,
and probing signal are interfaces to be validated. This foundation does not
assume that an Arduino CNC Shield has enough current, axes, or probe/spindle
features until the exact hardware is identified.

## Coordinate convention

X is left/right, positive to the right when facing the machine. Y is
front/back, positive toward the rear. Z is up/down, positive upward from the
workholding reference plane. The final physical origin and bed datum are
controlled decisions, not yet selected.

## Architecture risks

- PETG creep may relax rail and bearing preload or alter a long-term datum.
- Layer orientation may place weak inter-layer tension or shear in a primary
  load path.
- A large nominal envelope can increase gantry span and reduce tool-point
  stiffness.
- The spindle, cable routing, and dust/chip environment may impose thermal or
  contamination loads not captured by the first layout.
- Height mapping can compensate board flatness but cannot rescue a moving or
  poorly clamped machine datum.

# Generic mechanical CAD framework validation exercises

These exercises validate reasoning changes without redesigning or regenerating any CNC geometry. Each starts from a deliberately weak conceptual baseline and applies the generic skills.

## 1. NEMA17 motor bracket

- **Weak baseline:** A box with a four-hole pattern and a circular shaft opening is centered by eye.
- **Framework reasoning:** `mechanical-cad-design` establishes a motor-interface frame and shaft axis. `cad-hardware-integration` classifies the motor as an interface/envelope model until the body, shaft, connector, and mounting data are verified. `mechanical-joints-fasteners` separates clamp preload from locating shoulders and checks boss bearing, moment, edge distance, and tool access. `design-for-3d-printing` chooses an orientation with continuous perimeter paths through the motor reaction and gussets tied into the support.
- **Evidence:** Interface record, torque/moment load case, boss and wall checks, connector keep-out, print dossier, and service-removal view.
- **Lesson:** The mount is defined by shaft/load/service interfaces, not by the visual size of a box.

## 2. Supported linear rail

- **Weak baseline:** A rail is placed at a convenient height on a thin plate because the carriage reaches the desired location.
- **Framework reasoning:** `mechanical-cad-design` defines rail and carriage datums. `motion-mechanism-design` calculates span, carriage spacing, pitch/yaw/roll moment reactions, preload, travel, and alignment. `mechanical-assembly-design` provides continuous support, accessible tightening, shim/alignment strategy, and replacement access. `cad-design-review` inspects the seat in section and at motion extremes.
- **Evidence:** Rail-seat section, supported length, guide-load/moment screen, fastening sequence, alignment datum, and hardware/service view.
- **Lesson:** Rail length and carriage travel do not prove a structurally adequate guide installation.

## 3. Leadscrew bearing arrangement

- **Weak baseline:** Two bearing blocks are clamped equally at both ends and connected to a motor by a flexible coupler.
- **Framework reasoning:** `motion-mechanism-design` assigns one locating support for axial reaction and one non-locating support for displacement/assembly tolerance. It separates radial and axial load paths and checks screw whip, end margins, shaft engagement, coupler misalignment, and motor service. `mechanical-joints-fasteners` checks housing retention and preload.
- **Evidence:** Bearing-role diagram, axial/radial reaction path, tolerance/thermal displacement allowance, coupler load screen, and service sequence.
- **Lesson:** A plausible line of components can still be overconstrained and mechanically wrong.

## 4. Two-piece printable structural beam

- **Weak baseline:** A beam longer than the printer is split exactly at its midpoint with flat ends and four screws.
- **Framework reasoning:** `design-for-3d-printing` maps layer orientation, section stiffness, warping, and print supports. `mechanical-cad-design` traces bending and shear. `mechanical-joints-fasteners` adds a keyed or stepped shear interface while screws provide clamp. `mechanical-assembly-design` checks registration, tightening access, inspection, and replacement. The split is moved out of a high-moment or poorly inspectable region if the load path requires it.
- **Evidence:** Moment/shear sketch, split-location rationale, key/shoulder geometry, preload and bearing checks, print orientations, and assembled inspection view.
- **Lesson:** Printer size creates a design constraint, not permission for an arbitrary split.

## 5. Electronics mounting plate

- **Weak baseline:** A plate has a grid of holes and a cable opening; the board is assumed to fit.
- **Framework reasoning:** `cad-hardware-integration` records the board drawing and connector confidence. `mechanical-cad-design` defines the mounting datum and keep-outs. `mechanical-assembly-design` checks installation direction and captive hardware. `mechanical-joints-fasteners` chooses standoffs/inserts and checks clamp and board bearing. `cad-rendering-visualization` produces a hardware-only and cable-access view. `cad-design-review` checks service removal and cable bend radius.
- **Evidence:** Interface manifest, connector/cable envelope, standoff and fastener record, tool-access view, removal sequence, and inspection dimensions.
- **Lesson:** A plate is an interface and service part, not merely a perforated rectangle.

## Cross-exercise findings

The framework consistently changes the starting question from “does the solid fit?” to “what function, datum, interface, load path, constraint, manufacturing process, service action, and evidence make this part credible?” The exercises also expose why human review and physical validation remain necessary after automated CAD checks pass.

# Precision Mechanical CAD Research / Development

This repository is a clean baseline for investigating how an AI engineering
agent can produce useful, inspectable, precision mechanical CAD. It is not a
machine design repository and it does not yet contain a replacement CAD
framework.

The intentionally preserved engineering method is the
[precision-mechanical-cad skill](.agents/skills/precision-mechanical-cad/SKILL.md),
including its references and generic exercises. It defines reasoning and
review expectations without prescribing a particular CAD engine or repository
architecture.

The reset is recorded in [CLEANUP-AUDIT.md](CLEANUP-AUDIT.md). Historical
commits remain available through Git; the current tree is the starting point
for first-principles research, small generic experiments, and an architecture
proposal.

## Current boundary

- No PCB-CNC design, hardware selection, machine-specific dimensions, or
  product-specific workflow remains in the working tree.
- No general-purpose replacement framework has been implemented.
- Future additions must earn their place through a documented capability need,
  a reproducible experiment, or a clearly justified engineering workflow.

## Working principle

Use a real geometry kernel and existing CAD tooling wherever they already
provide the needed capability. Add repository infrastructure only when a
small, explicit experiment shows that it improves engineering correctness,
reproducibility, inspectability, or review.

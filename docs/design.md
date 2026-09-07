# OpenTorque rigid simulation design

## Purpose

This simulation lets a maker inspect the released OpenTorque geometry as one
rigid actuator, command its motor angle, and observe the uniquely derived
planetary and output motion. It is an additive interpretation of the published
mechanical sources, not a revision of them.

## Source and frame

`STEP/opentorque.step` is the assembly and placement authority. Named
`StepNode` leaves select the printed products in place. The origin and +Z
actuator axis remain those of the STEP; the gear group retains its 40 mm Z
translation and its planet centers remain at 27 mm radius and 120° spacing.
The print-oriented STLs supply independent bounds, connectivity, volume, and
tooth-frequency evidence but not assembly placement.

Simple connected CadQuery envelopes replace compound bearing products and
represent the motor and encoder board omitted from the STEP. Catalogue values
define only their outside dimensions. Named 0.05 mm increments establish
otherwise coincident axial/radial fit witnesses; they are recorded in code and
do not alter any upstream geometry.

## Motion architecture

The top-level `input_angle` driver rotates the motor can and 18-tooth sun. A
fixed 126-tooth housing ring and three 54-tooth planets produce:

```text
output/carrier = input / 8
planet relative spin = -7 input / 24
planet absolute spin = -input / 6
```

The housing, retainer, backplate, encoder cover, motor stator, encoder board,
and cross-roller outer race are fixed. Each planet gear spins inside a unit
which orbits with the carrier; its pin and bearing share that orbit. All three
carrier pieces, the encoder magnet holder, and the cross-roller inner race turn
with the output. Ports bind those groups at the root so internal sliders cannot
create incoherent states.

## Integrity contracts

The model requires connected rigid leaves, preserved source fingerprints,
source axial order and centers, exact reducer relations, one builder driver,
three finite instructions, and a sampled instruction path. Because source gear
engagement and bought-hardware capture envelopes have positive volume, the
interference contract names all 16 accepted pairs and bounds each volume across
the exact and faceted kernels. There is no global ignored-volume epsilon: any
new or removed pair fails, as does an existing pair outside its reviewed range.

## Findings and limits

- At home, exact planet/housing overlaps are 23.6147 mm³ each and exact
  planet/sun overlaps are 10.2284–10.2409 mm³. Faceted tooth volumes are lower,
  so their reviewed ranges deliberately cover both kernels.
- The retainer/outer-race and carrier/planet-bearing interfaces are represented
  as accepted capture seats. The connected envelopes cannot establish real
  bearing internal clearances, fits, or load paths.
- A 22 × 28 × 1.6 mm encoder-board envelope fits the source cover at Y=6 mm,
  with its front face 0.05 mm behind the source magnet-holder bound. Centering
  it at Y=0 creates a measured cover collision.
- The BOM motor alternatives differ dimensionally. The model uses the primary
  Multistar can dimensions and the X8318 stator diameter only as visibly
  distinct envelopes.
- The model is rigid and geometric. It does not establish torque, compliance,
  loaded backlash, efficiency, life, thermal/electromagnetic response,
  firmware behaviour, manufacturability, material strength, or safety.

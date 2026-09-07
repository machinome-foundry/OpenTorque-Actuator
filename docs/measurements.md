# Simulation source measurements

Measured 2026-09-07 from commit `412762e` with:

```sh
/home/asa/devel/libresolid-studio/.venv/bin/python simulation/tools/probe.py
```

The probe merges coincident STL vertices before asking about watertightness or connected bodies. The raw exports duplicate vertices at triangle boundaries, so an unprocessed split gives a false disconnected-body count.

## Assembly frame

`STEP/opentorque.step` is the placement authority. `solid import-step` reports the gear group translated by `(0, 0, 40)` mm. Inside it, the three planet gears are placed at:

| Planet | Rotation about +Z | Translation (mm) |
| --- | ---: | --- |
| 1 | 0° | `(0, 27, 1)` |
| 2 | +120° | `(-23.382685902, -13.5, 1)` |
| 3 | -120° | `(23.382685902, -13.5, 1)` |

Their 625 bearings use the same XY centers at local Z = 10 mm. Pins 2 and 3 inherit ±120° rotations; the pin product itself carries its source-modelled radial offset. Every other top-level product occurrence is at the identity, so its product frame is already the main assembly frame.

The complete imported STEP compound contains 66 solids, spans approximately 110 × 110 × 95 mm, and has volume 427969.944 mm³. That compound count includes bought bearing internals and is not a printed-part connectivity failure.

## Printable STL readings

Every listed STL is watertight and one connected body after vertex merging.

| Source | Bounds min (mm) | Bounds max (mm) | Volume (mm³) |
| --- | --- | --- | ---: |
| Actuator Housing | `(-54.997883, -55, -3.5)` | `(54.997883, 55, 62.5)` | 157345.105 |
| Backplate | `(-54.992332, -54.998058, -11)` | `(55, 54.998058, -3.5)` | 27491.109 |
| Bearing Retainer | `(-55, -54.998058, 62.5)` | `(54.992237, 54.998058, 73)` | 24476.122 |
| Encoder Cover | `(-24.999559, -25, -21)` | `(24.999559, 22.197973, -11)` | 11600.539 |
| Encoder Magnet Holder | `(-12.5, -12.498217, -14)` | `(12.5, 12.498217, -9)` | 1823.400 |
| Planet Carrier A | `(-42.743969, -42.748493, 62.5)` | `(42.75, 42.748493, 74)` | 59010.771 |
| Planet Carrier B | `(-42.748581, -42.748459, 40)` | `(42.75, 42.75, 62.5)` | 37496.469 |
| Planet Carrier C | `(-44.743687, -44.748421, 36)` | `(44.75, 44.748421, 47.5)` | 20843.855 |
| Planet Gear | `(-21.249887, -21.249996, 0)` | `(21.249943, 21.249973, 18)` | 19202.888 |
| Planet Gear low backlash | `(-21.750036, -21.750067, 0)` | `(21.749994, 21.749958, 18)` | 19627.319 |
| Sun Gear | `(-19.999229, -19.99692, -5)` | `(19.999229, 20, 20)` | 8724.093 |
| Sun Gear low backlash | `(-19.999229, -19.99692, -5)` | `(19.999229, 20, 20)` | 8582.864 |

The gear STL frames are print-local rather than assembly-global: the planet is centred around XY zero in its STL but is placed at 27 mm radius by the STEP occurrence.

## Gear evidence and kinematics

At each herringbone centre seam, the polar radial envelope has a dominant half-count harmonic and a smaller full tooth-count harmonic:

| Gear | Midplane Z | Radial range | Half-count amplitude | Full-count amplitude |
| --- | ---: | --- | ---: | ---: |
| Sun | 7.5 mm | 5.499967–8.249927 mm | 9: 1245.067 | 18: 217.718 |
| Planet | 9 mm | 18.374999–21.250001 mm | 27: 1557.406 | 54: 126.220 |
| Low-backlash sun | 7.5 mm | 4.874995–8.249927 mm | 9: 1273.371 | 18: 193.390 |
| Low-backlash planet | 9 mm | 18.374999–21.750001 mm | 27: 1673.715 | 54: 85.030 |

The assembled standard set therefore uses sun `Ns = 18`, planet `Np = 54`, and fixed ring `Nr = Ns + 2Np = 126`. Willis' relation gives carrier angle `input / 8`; external sun/planet mesh gives planet spin relative to the carrier `-7 input / 24`, or absolute planet orientation `-input / 6`.

## Catalogue dimensions used for envelopes

- The BOM's primary [Turnigy Multistar 9235-100KV listing](https://hobbyking.com/9235-100kv-turnigy-multistar-brushless-multi-rotor-motor.html) gives a 92 mm can diameter, 38 mm body length, 22 mm can length, and 43 mm total length. The item is discontinued; the simulation makes no availability claim.
- The BOM's alternate [SunnySky X8318S](https://sunnyskyusa.com/products/x8318s) gives a 91.6 mm rotor diameter, 41 mm body length without shaft, 46.5 mm total body length, and 15 mm shaft. Those values do not exactly match the Multistar listing, so interchangeability is not assumed.
- The official [THK RA8008 specification](https://tech.thk.com/en/products/get_all_attributes.php?id=2843) identifies the bearing; THK's dimensional table gives 80 mm bore, 96 mm outside diameter, and 8 mm width.
- The official [JTEKT 625 ZZ specification](https://koyo.jtekt.co.jp/en/products/detail/?pno=625+ZZ) gives 5 mm bore, 16 mm outside diameter, and 5 mm width.
- The [ams OSRAM AS5048 adapter-board manual](https://look.ams-osram.com/m/d6b55afbdfe4b3d0/original/AS5048_UG000223_1-00.pdf) gives a 22 × 28 mm board and 2.6 mm mounting holes.

Only simple clearance envelopes use these dimensions. The simulation does not redistribute vendor CAD or claim electrical, load, speed, or fit performance.

## Assembly-seat inventory

The full assembly was measured at home on both kernels with a global volume
epsilon of exactly 0 mm³. Per-pair bounds in `simulation/seats.py` span these
reviewed readings; the pair set itself must remain exactly 16.

| Pair group (three symmetric pairs where stated) | Faceted volume (mm³) | Exact volume (mm³) |
| --- | ---: | ---: |
| Housing / each planet gear | 22.439–22.917 | 23.6147 |
| Bearing retainer / cross-roller outer race | 38.3984 | 38.7747 |
| Carrier B / each planet bearing | 197.652–197.830 | 199.4453 |
| Carrier C / each planet bearing | 193.139–193.309 | 194.8935 |
| Sun / each planet gear | 2.0878–2.0893 | 10.2284–10.2409 |
| Each planet bearing / its planet gear | 230.5390 | 223.8385 |

The large kernel difference at tooth engagement is a tessellation effect, not
a clearance claim. The contract therefore uses explicit reviewed ranges for
each named pair rather than a global epsilon. A centered encoder-board mutant
added 59.739 mm³ against the cover and failed as a new pair; shifting the
cross-roller outer race by another 0.05 mm grew its retained overlap to
76.797 mm³ and failed its pair-specific range.

The connected bearing envelopes include deliberate fit clearance: the RA8008
outer envelope is 95.8 mm across inside the nominal 96 mm seat, its inner race
envelope is 86.8 mm across with an 80.2 mm bore, and each 625 envelope uses a
5.1 mm bore around the source 5 mm pin. The PCB envelope is placed at Y=6 mm
inside the source cover after a direct fit search; its Z span is
-15.65 through -14.05 mm.

## Accepted source fingerprints

| Source | SHA-256 |
| --- | --- |
| `STEP/opentorque.step` | `715965dc130555453d7d76d7ab51beeb8a5566a35cc37aae25cbb81151c879a3` |
| `STEP/low_backlash_gears.step` | `e42087627ee49bbe70a7d5259ede9f61386a24b58baccef7d7f00b92ffdfcce9` |
| `STL/Actuator Housing.stl` | `82685e3fb69f138f3ed10d0397c2fcff811a69f2fd28228a7e3b5e48d93fd28f` |
| `STL/Backplate.stl` | `b40a27d1e12d064efd924f86ae94bae99e6842807dcaa32c4332358bb914a87b` |
| `STL/Bearing Retainer.stl` | `2436ab847e4c324eb3d45ba8d16c1759268afb75822e598ab5b25dee474b260b` |
| `STL/Encoder Cover.stl` | `64f86f93e73a0f4f9cff8767ebd11355c416543e57cfe7f0ef9fefc72315c6e8` |
| `STL/Encoder Magnet Holder.stl` | `fc8fc7ee141c5ffe3179313b405d88294c33794fe8d00ad97425bd188be74942` |
| `STL/Planet Carrier A.stl` | `acad9410458907d6d01a0ae769e9d9cdfb7776a5182a5ecabbb374795e9422b7` |
| `STL/Planet Carrier B.stl` | `5851e2b6e5a2c6404b485223b0961eb626815932ff4d11c9fa7477eb98ee87ea` |
| `STL/Planet Carrier C.stl` | `ab97f7d79fef1652b9739287d7dffe526eedc0ed83202bc06ea4dda63a48557c` |
| `STL/Planet Gear.stl` | `45ac97ec746b598675a839abe673980edf23f09e2e50affebd089219da7db769` |
| `STL/Planet Gear low backlash.stl` | `e8364a823c63b74eb6cd00f427a12cfa1d4d79f22eb6983d23f16c5168e4c6db` |
| `STL/Sun Gear.stl` | `15740f6ad3d74bca58fecc99b26c4b5a97333d8145e3f4f58b2ba19bcb9ec930` |
| `STL/Sun Gear low backlash.stl` | `123732b287f47a8635b80406d30b94bf9655d39f47b0c5c88676a874e7bbfd80` |

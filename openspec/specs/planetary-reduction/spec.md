# Planetary Reduction Specification

## Purpose

Represent the source planetary layout and its fixed-ring 8:1 kinematics with mechanically coherent, testable motion.

## Requirements

### Requirement: Source-defined planetary layout

The simulation SHALL preserve the assembled STEP's coaxial 18-tooth sun, three 54-tooth planets at 27 mm centers and 120-degree spacing, and fixed 126-tooth internal ring at the home pose.

#### Scenario: Reducer at home

- **WHEN** `input_angle` is 0 degrees
- **THEN** the sun and carrier retain their source orientations, each planet axis is 27 mm from the actuator axis within 0.01 mm, and adjacent planet axes are separated by 120 degrees within 0.01 degree

### Requirement: Eight-to-one carrier reduction

The simulation SHALL derive every reducer angle from the input so that the fixed-ring carrier turns once in the input direction for every eight input revolutions and each planet preserves the corresponding external-mesh spin.

#### Scenario: One motor revolution

- **WHEN** `input_angle` advances from 0 to 360 degrees
- **THEN** the output carrier advances 45 degrees and every planet's absolute orientation changes by -60 degrees

#### Scenario: One output revolution

- **WHEN** `input_angle` advances from 0 to 2880 degrees
- **THEN** the output carrier advances exactly 360 degrees, every planet center completes exactly one orbit, and every planet's absolute orientation changes by -480 degrees

### Requirement: Meshing geometry remains physically coherent

The reducer SHALL keep the sun, planets, and fixed ring in their source-defined engagement without positive-volume rigid interference beyond the documented source-seat inventory throughout a complete output revolution.

#### Scenario: Driven reduction sweep

- **WHEN** the input is sampled from 0 through 2880 degrees at intervals sufficient to include every tooth phase
- **THEN** the rigid reducer parts exhibit only the documented source-seat intersection inventory and no new or changed overlap

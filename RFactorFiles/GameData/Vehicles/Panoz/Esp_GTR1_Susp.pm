// Panoz Esperante GTR-1 1997 Suspension Geometry File
//////////////////////////////////////////////////////////////////////////
//
// Conventions:
//
// +x = left
// +z = rear
// +y = up
// +pitch = nose up
// +yaw = nose right
// +roll = right
//
// [BODY]  - a rigid mass with mass and inertial properties
// [JOINT] - a ball joint constraining an offset of one body to an
//           offset of another body (eliminates 3 DOF)
// [HINGE] - a constraint restricting the relative rotations of two
//           bodies to be around a single axis (eliminates 2 DOF).
// [BAR]   - a constraint holding an offset of one body from an offset of
//           another body at a fixed distance (eliminates 1 DOF).
// [JOINT&HINGE] - both the joint and hinge constraints, forming the
//           conventional definition of a hinge (eliminates 5 DOF).
//
//////////////////////////////////////////////////////////////////////////

// Body including all rigidly attached parts (wings, barge boards, etc.)
[BODY]
Name=body Mass=(0) Inertia=(0,0,0)
Pos=(0,0,0) Ori=(0,0,0)

// Front spindles
[BODY]
Name=fl_spindle Mass=(12.0) Inertia=(0.025,0.024,0.0225)
Pos=( 0.820,0.0,-1.30) Ori=(0,0,0)

[BODY]
Name=fr_spindle Mass=(12.0) Inertia=(0.025,0.024,0.0225)
Pos=(-0.820,0.0,-1.30) Ori=(0,0,0)

// Front wheels
[BODY]
Name=fl_wheel Mass=(22.0) Inertia=(1.33,0.74,0.74)
Pos=( 0.850,0.0,-1.30) Ori=(0,0,0)

[BODY]
Name=fr_wheel Mass=(22.0) Inertia=(1.33,0.74,0.74)
Pos=(-0.850,0.0,-1.30) Ori=(0,0,0)

// Rear spindles
[BODY]
Name=rl_spindle Mass=(13.0) inertia=(0.0275,0.0260,0.0245)
Pos=( 0.800,0.0, 1.39) Ori=(0,0,0)

[BODY]
Name=rr_spindle Mass=(13.0) inertia=(0.0275,0.0260,0.0245)
Pos=(-0.800,0.0, 1.39) Ori=(0,0,0)

// Rear wheels (includes half of rear-axle)
[BODY]
Name=rl_wheel Mass=(26.0) Inertia=(1.480,0.880,0.880)
Pos=(0.82,0.0, 1.39) Ori=(0.0,0.0,0.0)

[BODY]
Name=rr_wheel Mass=(26.0) Inertia=(1.480,0.880,0.880)
Pos=(-0.82,0.0, 1.39) Ori=(0.0,0.0,0.0)

// Fuel in tank is not rigidly attached - it is attached with springs and
// dampers to simulate movement.  Properties are defined in the HDV file.

[BODY]
Name=fuel_tank Mass=(1.5) Inertia=(1,1,1)
Pos=(0,0,0) Ori=(0,0,0)

// Driver's head is not rigidly attached, and it does NOT affect the vehicle
// physics.  Position is from the eyepoint defined in the VEH file, while
// other properties are defined in the head physics file.

[BODY]
Name=driver_head Mass=(6.1) Inertia=(0.035,0.026,0.030)
Pos=(0,0,0) Ori=(0,0,0)


//////////////////////////////////////////////////////////////////////////
//
// Constraints
//
//////////////////////////////////////////////////////////////////////////

// Front wheel and spindle connections
[JOINT&HINGE]
Posbody=fl_wheel Negbody=fl_spindle Pos=fl_wheel Axis=(-0.85,0,0)

[JOINT&HINGE]
Posbody=fr_wheel Negbody=fr_spindle Pos=fr_wheel Axis=( 0.85,0,0)

// Front left suspension (2 A-arms + 1 steering arm = 5 links)
[BAR] // forward upper arm
Name=fl_fore_upper Posbody=body Negbody=fl_spindle Pos=(0.344,0.078,-1.39) Neg=(0.682,0.090,-1.295)

[BAR] // rearward upper arm
Posbody=body Negbody=fl_spindle Pos=(0.339,0.077,-1.12) Neg=(0.682,0.090,-1.295)

[BAR] // forward lower arm
Posbody=body Negbody=fl_spindle Pos=(0.265,-0.142,-1.385) Neg=(0.730,-0.145,-1.305)

[BAR] // rearward lower arm
Name=fl_fore_lower Posbody=body Negbody=fl_spindle Pos=(0.265,-0.142,-1.080) Neg=(0.730,-0.145,-1.305)

[BAR] // steering arm (must be named for identification)
Name=fl_steering Posbody=body Negbody=fl_spindle Pos=(0.285,0.079,-1.425) Neg=(0.704,0.089,-1.400)

// Front right suspension (2 A-arms + 1 steering arm = 5 links)
[BAR] // forward upper arm (used in steering lock calculation)
Name=fr_fore_upper Posbody=body Negbody=fr_spindle Pos=(-0.344,0.078,-1.39) Neg=(-0.682,0.09,-1.295)

[BAR] // rearward upper arm
Posbody=body Negbody=fr_spindle Pos=(-0.339,0.077,-1.12) Neg=(-0.682,0.09,-1.295)

[BAR] // forward lower arm
Name=fr_fore_lower Posbody=body Negbody=fr_spindle Pos=(-0.265,-0.142,-1.385) Neg=(-0.730,-0.145,-1.305)

[BAR] // rearward lower arm
Posbody=body Negbody=fr_spindle Pos=(-0.265,-0.142,-1.080) Neg=(-0.730,-0.145,-1.305)

[BAR] // steering arm (must be named for identification)
Name=fr_steering Posbody=body Negbody=fr_spindle Pos=(-0.285,0.079,-1.425) Neg=(-0.704,0.089,-1.400)



///////////// TEMP rear suspension.

// Rear left suspension (2 A-arms + 1 straight link = 5 links)
[BAR] // forward upper arm
posbody=body negbody=rl_spindle pos=(0.420,0.160,1.086) neg=(0.672,0.190,1.39)

[BAR] // rearward upper arm
posbody=body negbody=rl_spindle pos=(0.420,0.160,1.441) neg=(0.672,0.190,1.39)

[BAR] // forward lower arm
posbody=body negbody=rl_spindle pos=(0.340,-0.152,1.086) neg=(0.700,-0.166,1.39)

[BAR] // rearward lower arm
posbody=body negbody=rl_spindle pos=(0.340,-0.152,1.441) neg=(0.700,-0.166,1.39)

[BAR] // straight link
posbody=body negbody=rl_spindle pos=(0.355,-0.04,1.56) neg=(0.696,-0.040,1.56)

// Rear right suspension (2 A-arms + 1 straight link = 5 links)
[BAR] // forward upper arm
posbody=body negbody=rr_spindle pos=(-0.420,0.160,1.086) neg=(-0.672,0.190,1.39)

[BAR] // rearward upper arm
posbody=body negbody=rr_spindle pos=(-0.420,0.160,1.441) neg=(-0.672,0.190,1.39)

[BAR] // forward lower arm
posbody=body negbody=rr_spindle pos=(-0.340,-0.152,1.086) neg=(-0.700,-0.166,1.39)

[BAR] // rearward lower arm
posbody=body negbody=rr_spindle pos=(-0.340,-0.152,1.441) neg=(-0.700,-0.166,1.39)

[BAR] // straight link
posbody=body negbody=rr_spindle pos=(-0.355,-0.040,1.56) neg=(-0.696,-0.040,1.56)

// Rear spindle and wheel connections
[JOINT&HINGE]
posbody=rl_wheel negbody=rl_spindle pos=rl_wheel axis=(-0.82,0.0,0.0)

[JOINT&HINGE]
posbody=rr_wheel negbody=rr_spindle pos=rr_wheel axis=(0.82,0.0,0.0)











//// 1.590538336052202283849918433931484502446982055464926590538336052
//// Rear left suspension (2 A-arms + 1 straight link = 5 links)
//[BAR] // forward upper arm
//Posbody=body Negbody=rl_spindle Pos=( 0.230, 0.162,1.13) Neg=(0.660,0.2,1.39) // X.162?, .611.. Y .. Z
//
//[BAR] // rearward upper arm
//Posbody=body Negbody=rl_spindle Pos=( 0.230, 0.168,1.47) Neg=(0.660,0.2,1.39) // X.188, .611.. Y .. Z
//
//[BAR] // forward lower arm
//Posbody=body Negbody=rl_spindle Pos=( 0.205,-0.135,1.13) Neg=(0.690,-0.145,1.39)
//
//[BAR] // rearward lower arm
//Posbody=body Negbody=rl_spindle Pos=( 0.205,-0.135,1.47) Neg=(0.690,-0.145,1.39)
//
//[BAR] // straight link
//Posbody=body Negbody=rl_spindle Pos=( 0.210,-0.12,1.48) Neg=(0.710,-0.125,1.48)
//
//// Rear right suspension (2 A-arms + 1 straight link = 5 links)
//[BAR] // forward upper arm
//Posbody=body Negbody=rr_spindle Pos=(-0.230, 0.162,1.13) Neg=(-0.660,0.2,1.39)
//
//[BAR] // rearward upper arm
//Posbody=body Negbody=rr_spindle Pos=(-0.230, 0.168,1.47) Neg=(-0.660,0.2,1.39)
//
//[BAR] // forward lower arm
//Posbody=body Negbody=rr_spindle Pos=(-0.205,-0.135,1.13) Neg=(-0.690,-0.145,1.39)
//
//[BAR] // rearward lower arm
//Posbody=body Negbody=rr_spindle Pos=(-0.205,-0.135,1.47) Neg=(-0.690,-0.145,1.39)
//
//[BAR] // straight link
//Posbody=body Negbody=rr_spindle Pos=(-0.210,-0.12,1.48) Neg=(-0.710,-0.125,1.48)
//
//// Rear spindle and wheel connections
//[JOINT&HINGE]
//Posbody=rl_wheel Negbody=rl_spindle Pos=rl_wheel Axis=(-0.82,0,0)
//
//[JOINT&HINGE]
//Posbody=rr_wheel Negbody=rr_spindle Pos=rr_wheel Axis=( 0.82,0,0)

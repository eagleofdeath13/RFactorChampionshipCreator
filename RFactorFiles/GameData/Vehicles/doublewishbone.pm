
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
name=body mass=(900.0) inertia=(388.0,423.0,25.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

// Front spindles
[BODY]
name=fl_spindle mass=(8.0) inertia=(0.0175,0.0160,0.0145)
pos=(0.67,0.0,-1.65) ori=(0.0,0.0,0.0)

[BODY]
name=fr_spindle mass=(8.0) inertia=(0.0175,0.0160,0.0145)
pos=(-0.67,0.0,-1.65) ori=(0.0,0.0,0.0)

// Front wheels
[BODY]
name=fl_wheel mass=(20.0) inertia=(0.913,0.594,0.594)
pos=(0.7177,0.0,-1.65) ori=(0.0,0.0,0.0)

[BODY]
name=fr_wheel mass=(20.0) inertia=(0.913,0.594,0.594)
pos=(-0.7177,0.0,-1.65) ori=(0.0,0.0,0.0)

// Rear spindles
[BODY]
name=rl_spindle mass=(8.5) inertia=(0.0175,0.0160,0.0145)
pos=(0.64,0.0,1.35) ori=(0.0,0.0,0.0)

[BODY]
name=rr_spindle mass=(8.5) inertia=(0.0175,0.0160,0.0145)
pos=(-0.64,0.0,1.35) ori=(0.0,0.0,0.0)

// Rear wheels (includes half of rear-axle)
[BODY]
name=rl_wheel mass=(22.0) inertia=(0.996,0.655,0.655)
pos=(0.7025,0.0,1.35) ori=(0.0,0.0,0.0)

[BODY]
name=rr_wheel mass=(22.0) inertia=(0.996,0.655,0.655)
pos=(-0.7025,0.0,1.35) ori=(0.0,0.0,0.0)

// Fuel in tank is not rigidly attached - it is attached with springs and
// dampers to simulate movement.  Properties are defined in the HDV file.
[BODY]
name=fuel_tank mass=(1.0) inertia=(1.0,1.0,1.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

// Driver's head is not rigidly attached, and it does NOT affect the vehicle
// physics.  Position is from the eyepoint defined in the VEH file, while
// other properties are defined in the head physics file.
[BODY]
name=driver_head mass=(5.0) inertia=(0.02,0.02,0.02)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

//////////////////////////////////////////////////////////////////////////
//
// Constraints
//
//////////////////////////////////////////////////////////////////////////

// Front wheel and spindle connections
[JOINT&HINGE]
posbody=fl_wheel negbody=fl_spindle pos=fl_wheel axis=(-1.0,0.0,0.0)

[JOINT&HINGE]
posbody=fr_wheel negbody=fr_spindle pos=fr_wheel axis=(1.0,0.0,0.0)

// Front left suspension (2 A-arms + 1 steering arm = 5 links)
[BAR] // forward upper arm
name=fl_fore_upper posbody=body negbody=fl_spindle pos=(0.157,0.103,-1.65) neg=(0.657,0.113,-1.635)

[BAR] // rearward upper arm
posbody=body negbody=fl_spindle pos=(0.157,0.103,-1.45) neg=(0.6575,0.113,-1.635)

[BAR] // forward lower arm
posbody=body negbody=fl_spindle pos=(0.00,-0.113,-1.65) neg=(0.667,-0.113,-1.65)

[BAR] // rearward lower arm
name=fl_fore_lower posbody=body negbody=fl_spindle pos=(0.00,-0.113,-1.425) neg=(0.667,-0.113,-1.65)

[BAR] // steering arm (must be named for identification)
name=fl_steering posbody=body negbody=fl_spindle pos=(0.155,0.113,-1.725) neg=(0.667,0.113,-1.735)

// Front right suspension (2 A-arms + 1 steering arm = 5 links)
[BAR] // forward upper arm (used in steering lock calculation)
name=fr_fore_upper posbody=body negbody=fr_spindle pos=(-0.157,0.103,-1.65) neg=(-0.657,0.113,-1.635)

[BAR] // rearward upper arm
posbody=body negbody=fr_spindle pos=(-0.157,0.103,-1.45) neg=(-0.6575,0.113,-1.635)

[BAR] // forward lower arm
name=fr_fore_lower posbody=body negbody=fr_spindle pos=(-0.00,-0.113,-1.65) neg=(-0.667,-0.113,-1.65)

[BAR] // rearward lower arm
posbody=body negbody=fr_spindle pos=(-0.00,-0.113,-1.425) neg=(-0.667,-0.113,-1.65)

[BAR] // steering arm (must be named for identification)
name=fr_steering posbody=body negbody=fr_spindle pos=(-0.155,0.113,-1.725) neg=(-0.667,0.113,-1.735)

// Rear left suspension (2 A-arms + 1 straight link = 5 links)
[BAR] // forward upper arm
posbody=body negbody=rl_spindle pos=(0.109,0.11,1.05) neg=(0.615,0.12,1.35)

[BAR] // rearward upper arm
posbody=body negbody=rl_spindle pos=(0.109,0.11,1.40) neg=(0.615,0.12,1.35)

[BAR] // forward lower arm
posbody=body negbody=rl_spindle pos=(0.079,-0.06,1.05) neg=(0.615,-0.08,1.35)

[BAR] // rearward lower arm
posbody=body negbody=rl_spindle pos=(0.079,-0.08,1.40) neg=(0.615,-0.08,1.35)

[BAR] // straight link
posbody=body negbody=rl_spindle pos=(0.089,0.02,1.52) neg=(0.615,0.02,1.52)

// Rear right suspension (2 A-arms + 1 straight link = 5 links)
[BAR] // forward upper arm
posbody=body negbody=rr_spindle pos=(-0.109,0.11,1.05) neg=(-0.615,0.12,1.35)

[BAR] // rearward upper arm
posbody=body negbody=rr_spindle pos=(-0.109,0.11,1.40) neg=(-0.615,0.12,1.35)

[BAR] // forward lower arm
posbody=body negbody=rr_spindle pos=(-0.079,-0.06,1.05) neg=(-0.615,-0.08,1.35)

[BAR] // rearward lower arm
posbody=body negbody=rr_spindle pos=(-0.079,-0.08,1.40) neg=(-0.615,-0.08,1.35)

[BAR] // straight link
posbody=body negbody=rr_spindle pos=(-0.089,0.02,1.52) neg=(-0.615,0.02,1.52)

// Rear spindle and wheel connections
[JOINT&HINGE]
posbody=rl_wheel negbody=rl_spindle pos=rl_wheel axis=(-1.0,0.0,0.0)

[JOINT&HINGE]
posbody=rr_wheel negbody=rr_spindle pos=rr_wheel axis=(1.0,0.0,0.0)

// Special Thanks to Doug Arnao for this vastly improved and more realistic geometry!!!


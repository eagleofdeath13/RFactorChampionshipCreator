
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
// NOTE: the mass and inertia for the main vehicle "body" is not used
// because it is derived from the HDV file by subtracting out all the
// wheels, etc.  For all other bodies (wheels, spindles), they are important!
[BODY]
name=body mass=(1.0) inertia=(1.0,1.0,1.0)
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
name=fl_wheel mass=(22.0) inertia=(0.900,0.600,0.600)
pos=(0.7177,0.0,-1.65) ori=(0.0,0.0,0.0)

[BODY]
name=fr_wheel mass=(22.0) inertia=(0.900,0.600,0.600)
pos=(-0.7177,0.0,-1.65) ori=(0.0,0.0,0.0)

// Solid rear axle
[BODY]
name=rear_axle mass=(30.0) inertia=(1.0, 3.0, 3.0)
pos=(0.0,0.0,1.35) ori=(0.0,0.0,0.0)

// Rear wheels
[BODY]
name=rl_wheel mass=(22.0) inertia=(0.900,0.600,0.600)
pos=(0.7025,0.0,1.35) ori=(0.0,0.0,0.0)

[BODY]
name=rr_wheel mass=(22.0) inertia=(0.900,0.600,0.600)
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
name=fl_fore_upper posbody=body negbody=fl_spindle pos=(0.207,0.103,-1.65) neg=(0.637,0.113,-1.635)

[BAR] // rearward upper arm
posbody=body negbody=fl_spindle pos=(0.207,0.103,-1.45) neg=(0.637,0.113,-1.635)

[BAR] // forward lower arm
posbody=body negbody=fl_spindle pos=(0.10,-0.113,-1.65) neg=(0.647,-0.113,-1.65)

[BAR] // rearward lower arm
name=fl_fore_lower posbody=body negbody=fl_spindle pos=(0.10,-0.113,-1.425) neg=(0.647,-0.113,-1.65)

[BAR] // steering arm (must be named for identification)
name=fl_steering posbody=body negbody=fl_spindle pos=(0.205,0.113,-1.725) neg=(0.637,0.113,-1.735)

// Front right suspension (2 A-arms + 1 steering arm = 5 links)
[BAR] // forward upper arm (used in steering lock calculation)
name=fr_fore_upper posbody=body negbody=fr_spindle pos=(-0.207,0.103,-1.65) neg=(-0.637,0.113,-1.635)

[BAR] // rearward upper arm
posbody=body negbody=fr_spindle pos=(-0.207,0.103,-1.45) neg=(-0.637,0.113,-1.635)

[BAR] // forward lower arm
name=fr_fore_lower posbody=body negbody=fr_spindle pos=(-0.10,-0.113,-1.65) neg=(-0.647,-0.113,-1.65)

[BAR] // rearward lower arm
posbody=body negbody=fr_spindle pos=(-0.10,-0.113,-1.425) neg=(-0.647,-0.113,-1.65)

[BAR] // steering arm (must be named for identification)
name=fr_steering posbody=body negbody=fr_spindle pos=(-0.205,0.113,-1.725) neg=(-0.637,0.113,-1.735)

// Rear axle is connected to the body with a ball joint approximately 45 inches
// in front of the rear axle.
[JOINT]
posbody=body negbody=rear_axle pos=(0.0, 0.0, 0.200)

// Fourth link to provide enough constraints on the rear axle
[BAR]
posbody=body negbody=rear_axle pos=(-0.45, 0.0, 1.65) neg=(0.45, 0.0, 1.65)

// Rear wheel connections
[JOINT&HINGE]
posbody=rl_wheel negbody=rear_axle pos=rl_wheel axis=(-1.0,0.0,0.0)

[JOINT&HINGE]
posbody=rr_wheel negbody=rear_axle pos=rr_wheel axis=(1.0,0.0,0.0)


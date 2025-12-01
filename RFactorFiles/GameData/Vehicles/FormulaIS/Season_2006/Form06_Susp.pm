// F1 Type Suspension
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
name=body mass=(0.0) inertia=(0.0,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

// Front spindles
[BODY]
name=fl_spindle mass=(6.0) inertia=(0.0200,0.0185,0.0170)
pos=(0.63,0.0,-1.65) ori=(0.0,0.0,0.0)

[BODY]
name=fr_spindle mass=(6.0) inertia=(0.0200,0.0185,0.0170)
pos=(-0.63,0.0,-1.65) ori=(0.0,0.0,0.0)

// Front wheels
[BODY]
name=fl_wheel mass=(17.1) inertia=(0.9270,0.6529,0.6529)
pos=(0.707,0.0,-1.65) ori=(0.0,0.0,0.0)

[BODY]
name=fr_wheel mass=(17.1) inertia=(0.9270,0.6529,0.6529)
pos=(-0.707,0.0,-1.65) ori=(0.0,0.0,0.0)

// Rear spindles
[BODY]
name=rl_spindle mass=(6.5) inertia=(0.0205,0.0190,0.0175)
pos=(0.635,0.0,1.35) ori=(0.0,0.0,0.0)

[BODY]
name=rr_spindle mass=(6.5) inertia=(0.0205,0.0190,0.0175)
pos=(-0.635,0.0,1.35) ori=(0.0,0.0,0.0)

// Rear wheels (includes half of rear-axle)
[BODY]
name=rl_wheel mass=(19.8) inertia=(1.1083,0.8029,0.8029)
pos=(0.685,0.0,1.35) ori=(0.0,0.0,0.0)

[BODY]
name=rr_wheel mass=(19.8) inertia=(1.1083,0.8029,0.8029)
pos=(-0.685,0.0,1.35) ori=(0.0,0.0,0.0)

// Fuel in tank is not rigidly attached - it is attached with springs and
// dampers to simulate movement.  Properties are defined in the HDV file.
[BODY]
name=fuel_tank mass=(1.0) inertia=(1.0,1.0,1.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

// Driver's head is not rigidly attached, and it does NOT affect the vehicle
// physics.  Position is from the eyepoint defined in the VEH file, while
// other properties are defined in the head physics file.
[BODY]
name=driver_head mass=(5.85) inertia=(0.032,0.024,0.028)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

//////////////////////////////////////////////////////////////////////////
//
// Constraints
//
//////////////////////////////////////////////////////////////////////////

// Front wheel and spindle connections
[JOINT&HINGE]
posbody=fl_wheel negbody=fl_spindle pos=fl_wheel axis=(-0.78,0.0,0.0)

[JOINT&HINGE]
posbody=fr_wheel negbody=fr_spindle pos=fr_wheel axis=( 0.78,0.0,0.0)

// Front left suspension (2 A-arms + 1 steering arm = 5 links)
[BAR] // forward upper arm
name=fl_fore_upper posbody=body negbody=fl_spindle pos=(0.155,0.175,-1.66) neg=(0.602,0.113,-1.65)

[BAR] // rearward upper arm
posbody=body negbody=fl_spindle pos=(0.157,0.165,-1.365) neg=(0.602,0.113,-1.65)

[BAR] // forward lower arm
posbody=body negbody=fl_spindle pos=(0.03,-0.051,-1.66) neg=(0.616,-0.113,-1.65)

[BAR] // rearward lower arm
name=fl_fore_lower posbody=body negbody=fl_spindle pos=(0.03,-0.051,-1.340) neg=(0.616,-0.113,-1.65)

[BAR] // steering arm (must be named for identification)
name=fl_steering posbody=body negbody=fl_spindle pos=(0.152,0.176,-1.705) neg=(0.616,0.113,-1.700)

// Front right suspension (2 A-arms + 1 steering arm = 5 links)
[BAR] // forward upper arm (used in steering lock calculation)
name=fr_fore_upper posbody=body negbody=fr_spindle pos=(-0.155,0.175,-1.66) neg=(-0.602,0.113,-1.65)

[BAR] // rearward upper arm
posbody=body negbody=fr_spindle pos=(-0.157,0.165,-1.365) neg=(-0.602,0.113,-1.65)

[BAR] // forward lower arm
name=fr_fore_lower posbody=body negbody=fr_spindle pos=(-0.03,-0.051,-1.66) neg=(-0.616,-0.113,-1.65)

[BAR] // rearward lower arm
posbody=body negbody=fr_spindle pos=(-0.03,-0.051,-1.340) neg=(-0.616,-0.113,-1.65)

[BAR] // steering arm (must be named for identification)
name=fr_steering posbody=body negbody=fr_spindle pos=(-0.152,0.176,-1.705) neg=(-0.616,0.113,-1.700)

// Rear left suspension (2 A-arms + 1 straight link = 5 links)
[BAR] // forward upper arm
posbody=body negbody=rl_spindle pos=(0.109,0.11,1.05) neg=(0.600,0.12,1.35)

[BAR] // rearward upper arm
posbody=body negbody=rl_spindle pos=(0.109,0.11,1.40) neg=(0.600,0.12,1.35)

[BAR] // forward lower arm
posbody=body negbody=rl_spindle pos=(0.079,-0.06,1.05) neg=(0.600,-0.08,1.35)

[BAR] // rearward lower arm
posbody=body negbody=rl_spindle pos=(0.079,-0.08,1.40) neg=(0.600,-0.08,1.35)

[BAR] // straight link
posbody=body negbody=rl_spindle pos=(0.089,0.02,1.52) neg=(0.600,0.02,1.52)

// Rear right suspension (2 A-arms + 1 straight link = 5 links)
[BAR] // forward upper arm
posbody=body negbody=rr_spindle pos=(-0.109,0.11,1.05) neg=(-0.600,0.12,1.35)

[BAR] // rearward upper arm
posbody=body negbody=rr_spindle pos=(-0.109,0.11,1.40) neg=(-0.600,0.12,1.35)

[BAR] // forward lower arm
posbody=body negbody=rr_spindle pos=(-0.079,-0.06,1.05) neg=(-0.600,-0.08,1.35)

[BAR] // rearward lower arm
posbody=body negbody=rr_spindle pos=(-0.079,-0.08,1.40) neg=(-0.600,-0.08,1.35)

[BAR] // straight link
posbody=body negbody=rr_spindle pos=(-0.089,0.02,1.52) neg=(-0.600,0.02,1.52)

// Rear spindle and wheel connections
[JOINT&HINGE]
posbody=rl_wheel negbody=rl_spindle pos=rl_wheel axis=(-0.77,0.0,0.0)

[JOINT&HINGE]
posbody=rr_wheel negbody=rr_spindle pos=rr_wheel axis=( 0.77,0.0,0.0)

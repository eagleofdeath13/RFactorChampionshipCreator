// Stock Car Suspension Geometry file. © 2006 Image Space Inc. 
/////////////////////////////////////////////////////////////////////////////
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
/////////////////////////////////////////////////////////////////////////////

// Body including all rigidly attached parts (wings, barge boards, etc.)
[BODY]
name=body mass=(0.0) inertia=(0.0,0.0,0.0)
pos=(0.0,0.00,0.0) ori=(0.0,0.0,0.0)

// Front spindles
[BODY]
name=fl_spindle mass=(22.0) inertia=(0.0325,0.0305,0.0285)
pos=(0.70,0.0,-1.34) ori=(0.0,0.0,0.0)

[BODY]
name=fr_spindle mass=(22.0) inertia=(0.0325,0.0305,0.0285)
pos=(-0.70,0.0,-1.34) ori=(0.0,0.0,0.0)

// Front wheels
[BODY]
name=fl_wheel mass=(26.0) inertia=(2.100,1.220,1.220)
pos=(0.764,0.0,-1.34) ori=(0.0,0.0,0.0)

[BODY]
name=fr_wheel mass=(26.0) inertia=(2.100,1.220,1.220)
pos=(-0.764,0.0,-1.34) ori=(0.0,0.0,0.0)

// Live rear axle
[BODY]
name=rear_axle mass=(120.00) inertia=(10.70,10.70,5.20)
pos=(0.0,-0.07,1.30) ori=(0.0,0.0,0.0)

// Rear wheels 
[BODY]
name=rl_wheel mass=(30.0) inertia=(2.110,1.225,1.225)
pos=(0.715,0.0,1.35) ori=(0.0,0.0,0.0)

[BODY]
name=rr_wheel mass=(30.0) inertia=(2.110,1.225,1.225)
pos=(-0.715,0.0,1.35) ori=(0.0,0.0,0.0)

// Fuel in tank is not rigidly attached - it is attached with springs and
// dampers to simulate movement.  Properties are defined in the HDV file.

[BODY]
name=fuel_tank mass=(1.5) inertia=(1.0,1.0,1.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

// Driver's head is not rigidly attached, and it does NOT affect the vehicle
// physics.  Position is from the eyepoint defined in the VEH file, while
// other properties are defined in the head physics file.

[BODY]
name=driver_head mass=(6.0) inertia=(0.035,0.025,0.030)
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
posbody=fr_wheel negbody=fr_spindle pos=fr_wheel axis=(0.78,0.0,0.0)

// Front left suspension (2 A-arms + 1 steering arm = 5 links)
[BAR] // forward upper arm
name=fl_fore_upper posbody=body negbody=fl_spindle pos=(0.409,0.178,-1.38) neg=(0.589,0.195,-1.34)

[BAR] // rearward upper arm
posbody=body negbody=fl_spindle pos=(0.409,0.161,-1.140) neg=(0.589,0.195,-1.34)

[BAR] // forward lower arm
name=fl_fore_lower posbody=body negbody=fl_spindle pos=(0.193,-0.148,-1.320) neg=(0.612,-0.147,-1.34)

[BAR] // rearward lower arm
posbody=body negbody=fl_spindle pos=(0.349,-0.137,-0.990) neg=(0.612,-0.147,-1.34)

[BAR] // steering arm (must be named for identification)
name=fl_steering posbody=body negbody=fl_spindle pos=(0.235,-0.095,-1.476) neg=(0.606,-0.097,-1.516)

// Front right suspension (2 A-arms + 1 steering arm = 5 links)
[BAR] // forward upper arm (used in steering lock calculation)
name=fr_fore_upper posbody=body negbody=fr_spindle pos=(-0.409,0.178,-1.38) neg=(-0.589,0.195,-1.34)

[BAR] // rearward upper arm
posbody=body negbody=fr_spindle pos=(-0.409,0.161,-1.140) neg=(-0.589,0.195,-1.34)

[BAR] // forward lower arm
name=fr_fore_lower posbody=body negbody=fr_spindle pos=(-0.193,-0.148,-1.320) neg=(-0.612,-0.147,-1.34)

[BAR] // rearward lower arm
posbody=body negbody=fr_spindle pos=(-0.349,-0.137,-0.990) neg=(-0.612,-0.147,-1.34)

[BAR] // steering arm (must be named for identification)
name=fr_steering posbody=body negbody=fr_spindle pos=(-0.235,-0.095,-1.476) neg=(-0.606,-0.097,-1.516)

// Live Axle rear suspension geometry:
// 3 links + Trackbar
[BAR]
posbody=body negbody=rear_axle pos=( 0.00,-0.070,0.000) neg=( 0.00, 0.000,1.345)

[BAR]
posbody=body negbody=rear_axle pos=( 0.40,-0.110,0.710) neg=( 0.50,-0.100,1.365)

[BAR]
posbody=body negbody=rear_axle pos=(-0.40,-0.110,0.710) neg=(-0.50,-0.100,1.365)

// Track bar (heights will be changed with track bar adjustments)
[BAR]
name=track_bar posbody=body negbody=rear_axle pos=(0.55,-0.00, 1.47) neg=(-0.55,-0.00, 1.45)

// Rear spindle and wheel connections (axis will be changed with rear camber adjustments)
[JOINT&HINGE]
posbody=rl_wheel negbody=rear_axle pos=rl_wheel axis=(-0.8,0.0,0.0)

[JOINT&HINGE]
posbody=rr_wheel negbody=rear_axle pos=rr_wheel axis=(0.8,0.0,0.0)

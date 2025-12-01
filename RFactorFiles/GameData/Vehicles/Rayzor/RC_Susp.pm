// Generated 06.03.2004 01:30:05
// Roll Center Height Front: 0.033 (relative to ground level)
// Roll Center Height Rear : 1.079 (relative to ground level)
// Front Kingpin Inclination : 12.849

[BODY]
name=body mass=(0.0) inertia=(0.0,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

[BODY]
name=fl_spindle mass=(8.50) inertia=(0.0175,0.0160,0.0145)
pos=(0.765205,0.0,-1.332500) ori=(0.0,0.0,0.0)

[BODY]
name=fr_spindle mass=(8.50) inertia=(0.0175,0.0160,0.0145)
pos=(-0.765205,0.0,-1.332500) ori=(0.0,0.0,0.0)

[BODY]
name=fl_wheel mass=(22.50) inertia=(0.900,0.600,0.600)
pos=(0.808000,0.0,-1.332500) ori=(0.0,0.0,0.0)

[BODY]
name=fr_wheel mass=(22.50) inertia=(0.900,0.600,0.600)
pos=(-0.808000,0.0,-1.332500) ori=(0.0,0.0,0.0)

[BODY]
name=rl_spindle mass=(8.50) inertia=(0.0175,0.0160,0.0145)
pos=(0.634844,0.0,1.332500) ori=(0.0,0.0,0.0)

[BODY]
name=rr_spindle mass=(8.50) inertia=(0.0175,0.0160,0.0145)
pos=(-0.634844,0.0,1.332500) ori=(0.0,0.0,0.0)

[BODY]
name=rl_wheel mass=(22.50) inertia=(0.900,0.600,0.600)
pos=(0.803500,0.0,1.332500) ori=(0.0,0.0,0.0)

[BODY]
name=rr_wheel mass=(22.50) inertia=(0.900,0.600,0.600)
pos=(-0.803500,0.0,1.332500) ori=(0.0,0.0,0.0)

[BODY]
name=fuel_tank mass=(1.0) inertia=(1.0,1.0,1.0)
pos=(0.0,0.15,1.00) ori=(0.0,0.0,0.0)

[BODY]
name=driver_head mass=(5.8) inertia=(0.033,0.024,0.029)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

[JOINT&HINGE]
posbody=fl_wheel negbody=fl_spindle pos=fl_wheel axis=(-0.808,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

[JOINT&HINGE]
posbody=fr_wheel negbody=fr_spindle pos=fr_wheel axis=(0.808,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

// Front left suspension [double wishbone]
[BAR] // forward upper arm
name=fl_fore_upper posbody=body negbody=fl_spindle pos=(0.294919,0.08803,-1.4087) neg=(0.737036,0.12573,-1.30710)

[BAR] // rearward upper arm
name=fl_rear_upper posbody=body negbody=fl_spindle pos=(0.294919,0.078617,-1.2563) neg=(0.737036,0.12573,-1.307100)

[BAR] // forward lower arm
name=fl_fore_lower posbody=body negbody=fl_spindle pos=(0.211099,-0.159288,-1.4087) neg=(0.793373,-0.139701,-1.3325)

[BAR] // rearward lower arm
name=fl_rear_lower posbody=body negbody=fl_spindle pos=(0.211099,-0.155926,-1.2563) neg=(0.793373,-0.139701,-1.332500)

[BAR] // steering arm (must be named for identification)
name=fl_steering posbody=body negbody=fl_spindle pos=(0.255099,0.139701,-1.586501) neg=(0.7556,0.139701,-1.586501)

// Front right suspension [double wishbone]
[BAR] // forward upper arm
name=fr_fore_upper posbody=body negbody=fr_spindle pos=(-0.294919,0.08803,-1.4087) neg=(-0.737036,0.125730,-1.3071)

[BAR] // rearward upper arm
name=fr_rear_upper posbody=body negbody=fr_spindle pos=(-0.294919,0.078617,-1.2563) neg=(-0.737036,0.125730,-1.3071)

[BAR] // forward lower arm
name=fr_fore_lower posbody=body negbody=fr_spindle pos=(-0.211099,-0.159288,-1.4087) neg=(-0.793373,-0.139701,-1.3325)

[BAR] // rearward lower arm
name=fr_rear_lower posbody=body negbody=fr_spindle pos=(-0.211099,-0.155926,-1.2563) neg=(-0.793373,-0.139701,-1.332500)

[BAR] // steering arm (must be named for identification)
name=fr_steering posbody=body negbody=fr_spindle pos=(-0.255099,0.139701,-1.586501) neg=(-0.7556,0.139701,-1.586501)

// Rear left suspension [double wishbone]
[BAR] // forward upper arm
name=rl_fore_upper posbody=body negbody=rl_spindle pos=(0.31911,0.098405,1.265194) neg=(0.618587,0.125730,1.3579)

[BAR] // rearward upper arm
name=rl_rear_upper posbody=body negbody=rl_spindle pos=(0.31911,0.096442,1.404252) neg=(0.618587,0.125730,1.357900)

[BAR] // forward lower arm
name=rl_fore_lower posbody=body negbody=rl_spindle pos=(0.310598,-0.135434,1.274128) neg=(0.6511,-0.139701,1.3325)

[BAR] // rearward lower arm
name=rl_rear_lower posbody=body negbody=rl_spindle pos=(0.310598,-0.145746,1.390872) neg=(0.6511,-0.139701,1.3325)

[BAR] // straight link
posbody=body negbody=rl_spindle pos=(0.206599,-0.139701,1.586501) neg=(0.6511,-0.139701,1.586501)

// Rear right suspension [double wishbone]
[BAR] // forward upper arm
name=rr_fore_upper posbody=body negbody=rr_spindle pos=(-0.31911,0.098405,1.265194) neg=(-0.618587,0.12573,1.3579)

[BAR] // rearward upper arm
name=rr_rear_upper posbody=body negbody=rr_spindle pos=(-0.319110,0.096442,1.404252) neg=(-0.618587,0.12573,1.3579)

[BAR] // forward lower arm
name=rr_fore_lower posbody=body negbody=rr_spindle pos=(-0.310598,-0.135434,1.274128) neg=(-0.6511,-0.139701,1.3325)

[BAR] // rearward lower arm
name=rr_rear_lower posbody=body negbody=rr_spindle pos=(-0.310598,-0.145746,1.390872) neg=(-0.6511,-0.139701,1.3325)

[BAR] // straight link
posbody=body negbody=rr_spindle pos=(-0.206599,-0.139701,1.586501) neg=(-0.6511,-0.139701,1.586501)

[JOINT&HINGE]
posbody=rl_wheel negbody=rl_spindle pos=rl_wheel axis=(-0.804,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

[JOINT&HINGE]
posbody=rr_wheel negbody=rr_spindle pos=rr_wheel axis=(0.804,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)


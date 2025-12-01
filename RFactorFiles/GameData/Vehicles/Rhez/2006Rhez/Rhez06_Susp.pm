// Generated 06.03.2004 01:30:05
// Roll Center Height Front: 0.033 (relative to ground level)
// Roll Center Height Rear : 1.079 (relative to ground level)
// Front Kingpin Inclination : 12.849

[BODY]
name=body mass=(0.0) inertia=(0.0,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

[BODY]
name=fl_spindle mass=(14.00) inertia=(0.0350,0.0320,0.0290)
pos=( 0.7650,0.0,-1.3325) ori=(0.0,0.0,0.0)

[BODY]
name=fr_spindle mass=(14.00) inertia=(0.0350,0.0320,0.0290)
pos=(-0.7650,0.0,-1.3325) ori=(0.0,0.0,0.0)

[BODY]
name=fl_wheel mass=(22.50) inertia=(1.200,0.750,0.750)
pos=( 0.8080,0.0,-1.3325) ori=(0.0,0.0,0.0)

[BODY]
name=fr_wheel mass=(22.50) inertia=(1.200,0.750,0.750)
pos=(-0.8080,0.0,-1.3325) ori=(0.0,0.0,0.0)

[BODY]
name=rl_spindle mass=(14.00) inertia=(0.0350,0.0320,0.0290)
pos=( 0.6350,0.0,1.3325) ori=(0.0,0.0,0.0)

[BODY]
name=rr_spindle mass=(14.00) inertia=(0.0350,0.0320,0.0290)
pos=(-0.6350,0.0,1.3325) ori=(0.0,0.0,0.0)

[BODY]
name=rl_wheel mass=(22.50) inertia=(1.200,0.750,0.750)
pos=( 0.8035,0.0,1.3325) ori=(0.0,0.0,0.0)

[BODY]
name=rr_wheel mass=(22.50) inertia=(1.200,0.750,0.750)
pos=(-0.8035,0.0,1.3325) ori=(0.0,0.0,0.0)

[BODY]
name=fuel_tank mass=(1.5) inertia=(1.0,1.0,1.0)
pos=(0.0,0.15,1.00) ori=(0.0,0.0,0.0)

[BODY]
name=driver_head mass=(6.0) inertia=(0.035,0.025,0.030)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

[JOINT&HINGE]
posbody=fl_wheel negbody=fl_spindle pos=fl_wheel axis=(-0.808,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

[JOINT&HINGE]
posbody=fr_wheel negbody=fr_spindle pos=fr_wheel axis=(0.808,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

// Front left suspension [double wishbone]
[BAR] // forward upper arm
name=fl_fore_upper posbody=body negbody=fl_spindle pos=(0.2949, 0.0880,-1.4587) neg=(0.7370, 0.1257,-1.3071)

[BAR] // rearward upper arm
name=fl_rear_upper posbody=body negbody=fl_spindle pos=(0.2949, 0.0786,-1.2063) neg=(0.7370, 0.1257,-1.3071)

[BAR] // forward lower arm
name=fl_fore_lower posbody=body negbody=fl_spindle pos=(0.2111,-0.1593,-1.4587) neg=(0.7934,-0.1397,-1.3325)

[BAR] // rearward lower arm
name=fl_rear_lower posbody=body negbody=fl_spindle pos=(0.2111,-0.1559,-1.2063) neg=(0.7934,-0.1397,-1.3325)

[BAR] // steering arm (must be named for identification)
name=fl_steering posbody=body negbody=fl_spindle pos=(0.2551, 0.1397,-1.5865) neg=(0.7556, 0.1397,-1.5865)

// Front right suspension [double wishbone]
[BAR] // forward upper arm
name=fr_fore_upper posbody=body negbody=fr_spindle pos=(-0.2949, 0.0880,-1.4587) neg=(-0.7370, 0.1257,-1.3071)

[BAR] // rearward upper arm
name=fr_rear_upper posbody=body negbody=fr_spindle pos=(-0.2949, 0.0786,-1.2063) neg=(-0.7370, 0.1257,-1.3071)

[BAR] // forward lower arm
name=fr_fore_lower posbody=body negbody=fr_spindle pos=(-0.2111,-0.1593,-1.4587) neg=(-0.7934,-0.1397,-1.3325)

[BAR] // rearward lower arm
name=fr_rear_lower posbody=body negbody=fr_spindle pos=(-0.2111,-0.1559,-1.2063) neg=(-0.7934,-0.1397,-1.3325)

[BAR] // steering arm (must be named for identification)
name=fr_steering posbody=body negbody=fr_spindle pos=(-0.2551, 0.1397,-1.5865) neg=(-0.7556, 0.1397,-1.5865)

// Rear left suspension [double wishbone]
[BAR] // forward upper arm
name=rl_fore_upper posbody=body negbody=rl_spindle pos=(0.3195, 0.0984, 1.2152) neg=(0.6186, 0.1257, 1.3579)

[BAR] // rearward upper arm
name=rl_rear_upper posbody=body negbody=rl_spindle pos=(0.3195, 0.0964, 1.4543) neg=(0.6186, 0.1257, 1.3579)

[BAR] // forward lower arm
name=rl_fore_lower posbody=body negbody=rl_spindle pos=(0.2950,-0.1354, 1.2241) neg=(0.6511,-0.1397, 1.3325)

[BAR] // rearward lower arm
name=rl_rear_lower posbody=body negbody=rl_spindle pos=(0.2950,-0.1457, 1.4409) neg=(0.6511,-0.1397, 1.3325)

[BAR] // straight link
posbody=body negbody=rl_spindle pos=(0.2270,-0.1397, 1.5665) neg=(0.6511,-0.1397, 1.5665)

// Rear right suspension [double wishbone]
[BAR] // forward upper arm
name=rr_fore_upper posbody=body negbody=rr_spindle pos=(-0.3195, 0.0984, 1.2152) neg=(-0.6246,0.12573, 1.3579)

[BAR] // rearward upper arm
name=rr_rear_upper posbody=body negbody=rr_spindle pos=(-0.3195, 0.0964, 1.4543) neg=(-0.6246,0.12573, 1.3579)

[BAR] // forward lower arm
name=rr_fore_lower posbody=body negbody=rr_spindle pos=(-0.2950,-0.1354, 1.2241) neg=(-0.6571,-0.1397, 1.3325)

[BAR] // rearward lower arm
name=rr_rear_lower posbody=body negbody=rr_spindle pos=(-0.2950,-0.1457, 1.4409) neg=(-0.6571,-0.1397, 1.3325)

[BAR] // straight link
posbody=body negbody=rr_spindle pos=(-0.2270,-0.1397, 1.5665) neg=(-0.6571,-0.1397, 1.5665)

[JOINT&HINGE]
posbody=rl_wheel negbody=rl_spindle pos=rl_wheel axis=(-0.804,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)

[JOINT&HINGE]
posbody=rr_wheel negbody=rr_spindle pos=rr_wheel axis=(0.804,0.0,0.0)
pos=(0.0,0.0,0.0) ori=(0.0,0.0,0.0)


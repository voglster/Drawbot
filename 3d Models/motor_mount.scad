// NEMA 17 stepper mount for dynamometer
// Ed Nisley KE4ZNU August 2011
mm = 1;
inch = 25.4 * mm;
 
//-- Layout Control
 
Layout = "Build";               // Build Show
 
//-- Extrusion parameters
 
ThreadThick = 0.4;
ThreadWT = 2.0;
ThreadWidth = ThreadThick * ThreadWT;
 
HoleWindage = 0.3;          // enlarge hole dia by this amount
 
function IntegerMultiple(Size,Unit) = Unit * ceil(Size / Unit);
 
//-- Useful sizes
 
Tap10_32 = 0.159 * inch;
Clear10_32 = 0.190 * inch;
Head10_32 = 0.373 * inch;
Head10_32Thick = 0.110 * inch;
Nut10_32Dia = 0.433 * inch;
Nut10_32Thick = 0.130 * inch;
 
NEMA17_ShaftDia = 5.0 * mm;
NEMA17_ShaftLength = 24.0 * mm;
NEMA17_PilotDia = 0.866 * inch;
NEMA17_PilotLength = 0.080 * inch;
NEMA17_BCD = 1.725 * inch;
NEMA17_BoltDia = 3.5 * mm;
NEMA17_BoltOC = 1.220 * inch;
 
//-- Mount Sizes
 
MountWidth = IntegerMultiple(NEMA17_BCD,ThreadWidth);       // use BCD for motor clearance
MountThick = IntegerMultiple(1.0,ThreadThick);              // for stiffness
 
MountBoltDia = 3.0;
 
StandThick = IntegerMultiple(1.0,ThreadWidth);              // baseplate
 
StrutThick = IntegerMultiple(1.0,ThreadWidth);              // sides holding motor mount
 
UprightLength = MountWidth + 2*StrutThick;
 
StandBoltHead = IntegerMultiple(Head10_32,5);               // bolt head rounded up
StandBoltOC = IntegerMultiple(UprightLength + 2*StandBoltHead,5);
 
StandLength = StandBoltOC + 2*StandBoltHead;
StandWidth = IntegerMultiple(2*StandBoltHead,ThreadThick);
 
StandBoltClear = (StandLength - UprightLength)/2;           // flat around bolt head
 
MotorRecess = StandWidth - MountThick;
 
echo(str("Stand Base: ",StandLength," x ",StandWidth," x ",StandThick));
echo(str("Stand Bolt OC: ",StandBoltOC));
echo(str("Strut Thick: ",StrutThick));
 
//-- Convenience values
 
Protrusion = 0.1;       // make holes look good and joints intersect properly
 
BuildOffset = 3 * ThreadWidth;
 
//----------------------
// Useful routines
 
module PolyCyl(Dia,Height,ForceSides=0) {           // based on nophead's polyholes
 
  Sides = (ForceSides != 0) ? ForceSides : (ceil(Dia) + 2);
 
  FixDia = Dia / cos(180/Sides);
 
  cylinder(r=(FixDia + HoleWindage)/2,
           h=Height,
       $fn=Sides);
}
 
module ShowPegGrid(Space = 10.0,Size = 1.0) {
 
  Range = floor(50 / Space);
 
    for (x=[-Range:Range])
      for (y=[-Range:Range])
        translate([x*Space,y*Space,Size/2])
          %cube(Size,center=true);
 
}
 
//----------------------
// Combined stand and mounting plate
 
module Combined() {
 
  difference() {
    translate([StandThick/2,0,StandWidth/2])
      cube([(MountWidth + StandThick),StandLength,StandWidth],center=true);
    translate([-Protrusion/2,0,StandWidth - (MotorRecess - Protrusion)/2])
      cube([(MountWidth + Protrusion),MountWidth,(MotorRecess + Protrusion)],center=true);
    translate([0,0,-Protrusion])                // pilot hole
      PolyCyl(NEMA17_PilotDia,(MountThick + 2*Protrusion));
    for (x=[-1,1])                              // motor bolt holes
      for (y=[-1,1])
        translate([x*NEMA17_BoltOC/2,y*NEMA17_BoltOC/2,-Protrusion])
          PolyCyl(MountBoltDia,(MountThick + 2*Protrusion));
    for (y=[-1,1])                              // cutouts over bolts
      translate([-Protrusion/2,
                y*((StandLength - StandBoltClear)/2 + Protrusion),
                StandWidth/2])
        cube([(MountWidth + Protrusion+ 20),
             (StandBoltClear + Protrusion),
             (StandWidth+ 2*Protrusion)],center=true);
    for (y=[-1,1])                              // stand bolt holes
      translate([(MountWidth/2 - Protrusion),y*NEMA17_BoltOC/2,StandWidth/2])
        rotate([0,90,0]){
          PolyCyl(Clear10_32,StandThick + 2*Protrusion,8);
          cylinder(r1=Clear10_32,r2=0,h=StandThick + 2*Protrusion);
        }
 
  }
 
}
 
//----------------------
// Lash everything together
 
ShowPegGrid();
 
if (Layout == "Build") {
  translate([0,0,0])
    Combined();
}
 
if (Layout == "Show") {
  translate([-StandWidth/2,0,(StandThick + MountWidth/2)])
    rotate([0,90,0])
      Combined();
}
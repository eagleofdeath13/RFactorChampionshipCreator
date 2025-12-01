Jacksonville500
{
  Filter Properties = 2006 NSCRS SRGrandPrix OWChallenge  
  Attrition = 30
  TrackName = Jacksonville Superspeedway
  EventName = Jacksonville 500
  GrandPrixName = Jacksonville 500			//this must be the same as event name in order to sort circuit info correctly.
  VenueName = Jacksonville Superspeedway
  Location = Jacksonville, FL, USA
  Length = 4.02 km / 2.50 miles
  TrackType = Superspeedway
  Track Record = Brad Shuber, 53.669
  FormationAndStart=2     // formation lap with rolling start (safety car leads the field and peels off into the pits)
  RollingStartLoc=1
  GarageDepth = 2.00

  NumStartingLights=1

  // Vehicle rules
  RestrictorPlate = true
  MinRearSpring=65672.0       // about 375 lbs/in (stockcar rules only)
  MinRearSlowBump=3940.0      // stockcar rules only
  MaxRearSlowBump=3941.0      // stockcar rules only
  MinRearSlowRebound=13134.0  // stockcar rules only
  MaxRearSlowRebound=13135.0  // stockcar rules only
  MaxRearWeight=0.5001        // stockcar rules only

  // DefaultScoring overrides
  FormationSpeedKPH = 100
  RaceLaps = 500
  RaceTime = 240

  // Time-of-day lighting
  SkyBlendSunAngles=(-20.5,-1.0,11.5,25.5)

  ShadowMinSunAngle=45.0

  Latitude = 30.331          // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 275   // the direction of North in degrees (range: 0 to 359)
  RaceDate = February 14   // default date for the race

  SunriseAmbientRGB = (120,120,110)      
  SunriseDirectionalRGB = (255,248,198)
  SunriseFogRGB = (204,174,240)

  DayAmbientRGB = (110,110,120)
  DayDirectionalRGB = (255,245,240)
  DayFogRGB = (203,214,236)

  SunsetAmbientRGB = (130,130,120)
  SunsetDirectionalRGB = (255,248,198)
  SunsetFogRGB = (204,196,122)

  NightAmbientRGB = (10,19,46)
  NightDirectionalRGB = (30,30,30)
  NightFogRGB = (0,0,0)

///////////////////////////SCORETOWER DATA////////////////////////////////////////////

ScoreboardFont=jackson_scorefont01.tga // default is scoreboardfont.bmp
ScoreboardBackground=jackson_scoretowerbg.tga // default is scoreboardbkg.bmp

ScoreboardMaxEntries=9 // how many car numbers can be displayed on tower (default is 32)
ScoreboardStartX=27 // x-position in texture to write first car number (default is 0)
ScoreboardStartY=7.5 // y-position in texture to write first car number (default is 10)
ScoreboardIncX=0 // increment in x-position for each new car number (default is 0)
ScoreboardIncY=55 // increment in y-position for each new car number (default is 16)
ScoreboardScaleX=2.2 // scale multiplier for x (default is 1.0)
ScoreboardScaleY=1.7 // scale multiplier for y (default is 1.0)

//////////////////////////////////////////////////////////////////////////////////////

  
  SettingsFolder = Jacksonville
  SettingsCopy = Jacksonville_NSCRS_Fast.svm
  SettingsCopy = Jacksonville_NSCRS_Easy.svm
  SettingsAI = Jacksonville.svm
  Qualify Laptime = 55.669
  Race Laptime = 55.869
}

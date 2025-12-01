NAS_BritishGP
{
  Filter Properties = 2006 SRGrandPrix OWChallenge *
  Attrition = 30
  TrackName = Northamptonshire GP
  EventName = British Grand Prix
  GrandPrixName = British Grand Prix //this must be the same as event name in order to sort circuit info correctly.
  VenueName = Northamptonshire
  Location = Northamptonshire, Great Britain
  Length = 5.141 km / 3.194 Miles
  TrackType = Permanent Road Course
  Track Record = , 78.739
  HeadlightsRequired = true  // whether headlights are required at night
  TerrainDataFile = ..\Northamptonshire.tdf         // terrain file override

  GarageDepth = 4.5
  TestDaystart = 10:00
  Practice1Start = 11:00
  Practice2Start = 14:00
  Practice3Start = 9:30
  QualifyStart = 12:30
  RaceStart = 12:00
  RaceLaps = 60

  NumStartingLights=5

  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)

  ShadowMinSunAngle=15.0

  Latitude = 52.09     // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 340 // the direction of North in degrees (range: 0 to 359)
  RaceDate = June 11   // default date for the race

  SunriseAmbientRGB = (120,120,110)      
  SunriseDirectionalRGB = (255,248,198)
  SunriseFogRGB = (204,174,240)

  DayAmbientRGB = (80,89,126)
  DayDirectionalRGB = (255,255,255)
  DayFogRGB = (203,214,236)

  SunsetAmbientRGB = (130,130,120)
  SunsetDirectionalRGB = (255,248,198)
  SunsetFogRGB = (204,196,122)

  NightAmbientRGB = (5,10,23)
  NightDirectionalRGB = (30,30,30)
  NightFogRGB = (0,0,0)

///////////////////////////SCORETOWER DATA////////////////////////////////////////////

ScoreboardFont=NorthAmpton_SCOREFONT.tga // default is scoreboardfont.bmp
ScoreboardBackground=SCORETOWERBKG.tga // default is scoreboardbkg.bmp

ScoreboardMaxEntries=6 // how many car numbers can be displayed on tower (default is 32)
ScoreboardStartX=0 // x-position in texture to write first car number (default is 0)
ScoreboardStartY=1 // y-position in texture to write first car number (default is 10)
ScoreboardIncX=0 // increment in x-position for each new car number (default is 0)
ScoreboardIncY=43 // increment in y-position for each new car number (default is 16)
ScoreboardScaleX=2.3 // scale multiplier for x (default is 1.0)
ScoreboardScaleY=1.8 // scale multiplier for y (default is 1.0)

//////////////////////////////////////////////////////////////////////////////////////

  SettingsFolder = British_GP
  SettingsCopy = Grip.svm
  SettingsCopy = British_GP.svm
  SettingsAI = British_GP.svm
  Qualify Laptime = 79.73
  Race Laptime = 83.50
}

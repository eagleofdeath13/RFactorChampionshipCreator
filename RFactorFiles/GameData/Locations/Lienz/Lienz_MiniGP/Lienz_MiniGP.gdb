LIENZ_MiniGP
{
  Filter Properties = Lienz SRGrandPrix OWChallenge *
  Attrition = 30
  TrackName = Lienz GP
  EventName = Lienz Week 3 - GP
  GrandPrixName = Lienz Week 3 - GP //this must be the same as event name in order to sort circuit info correctly.
  VenueName = Lienz Festival der Geschwindigkeit
  Location = Lienz, Tirol Austria
  Length = 6.26 KM / 3.89 Miles
  TrackType = Temporary Road Course
  Track Record = H6 GP1, 194.00
  HeadlightsRequired = true       // whether headlights are required at night
  TerrainDataFile = ..\Lienz.tdf  // terrain file override

  GarageDepth = 1.1
  TestDaystart = 13:00
  Practice1Day = Friday
  Practice1Start = 10:00
  Practice1Duration = 60
  Practice2Day = Friday
  Practice2Start = 13:00
  Practice2Duration = 60
  Practice3Day = Saturday
  Practice3Start = 11:00
  Practice3Duration = 45
  Practice4Day = Saturday
  Practice4Start = 14:00
  Practice4Duration = 45
  QualifyDay = Saturday
  QualifyStart = 13:00
  QualifyDuration = 60
  QualifyLaps = 15
  WarmupDay = Sunday
  WarmupStart = 12:00
  WarmupDuration = 30
  RaceDay = Sunday
  RaceStart = 14:00
  RaceLaps = 60
  RaceTime = 120

  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)

  ShadowMinSunAngle=15.0

  Latitude = 46.50     // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 180 // the direction of North in degrees (range: 0 to 359)
  RaceDate = August 05 // default date for the race

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

ScoreboardFont=Lienz_SCOREFONT.tga // default is scoreboardfont.bmp
ScoreboardBackground=Lienz_SCORETOWERBKG.tga // default is scoreboardbkg.bmp

ScoreboardMaxEntries=14 // how many car numbers can be displayed on tower (default is 32)
ScoreboardStartX=0 // x-position in texture to write first car number (default is 0)
ScoreboardStartY=2 // y-position in texture to write first car number (default is 10)
ScoreboardIncX=0 // increment in x-position for each new car number (default is 0)
ScoreboardIncY=36 // increment in y-position for each new car number (default is 16)
ScoreboardScaleX=2.25 // scale multiplier for x (default is 1.0)
ScoreboardScaleY=1.55 // scale multiplier for y (default is 1.0)

//////////////////////////////////////////////////////////////////////////////////////

  SettingsFolder = Lienz_GP
  SettingsCopy = Grip.svm
  SettingsCopy = Lienz_GP.svm
  SettingsAI = Lienz_GP.svm
  Qualify Laptime = 196.00
  Race Laptime = 200.00
}

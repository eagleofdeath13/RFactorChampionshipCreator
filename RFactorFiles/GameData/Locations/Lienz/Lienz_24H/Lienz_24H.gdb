LIENZ_24H
{
  Filter Properties = Lienz SRGrandPrix OWChallenge *
  Attrition = 30
  TrackName = Lienz 24 Hour GP
  EventName = Lienz Week 5 - 24 Hour GP
  GrandPrixName = Lienz Week 5 - 24 Hour GP //this must be the same as event name in order to sort circuit info correctly.
  VenueName = Lienz Festival der Geschwindigkeit
  Location = Lienz, Tirol Austria
  Length = 8.16 KM / 5.07 Miles
  TrackType = Temporary Road Course
  Track Record = Panoz GT2, 200.00
  HeadlightsRequired = true       // whether headlights are required at night
  TerrainDataFile = ..\Lienz.tdf  // terrain file override

  GarageDepth = 1.1
  TestDaystart = 14:00
  Practice1Day = Friday
  Practice1Start = 09:00
  Practice1Duration = 60
  Practice2Day = Friday
  Practice2Start = 13:00
  Practice2Duration = 60
  Practice3Day = Saturday
  Practice3Start = 14:00
  Practice3Duration = 45
  Practice4Day = Saturday
  Practice4Start = 17:00
  Practice4Duration = 45
  QualifyDay = Saturday
  QualifyStart = 12:00
  QualifyDuration = 60
  QualifyLaps = 10
  WarmupDay = Sunday
  WarmupStart = 14:00
  WarmupDuration = 30
  RaceDay = Sunday
  RaceStart = 16:00
  RaceLaps = 360
  RaceTime = 1440

  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)

  ShadowMinSunAngle=15.0

  Latitude = 46.50     // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 180 // the direction of North in degrees (range: 0 to 359)
  RaceDate = August 19 // default date for the race

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

  SettingsFolder = Lienz_24HGP
  SettingsCopy = Grip.svm
  SettingsCopy = Lienz_24HGP.svm
  SettingsAI = Lienz_24HGP.svm
  Qualify Laptime = 235.00
  Race Laptime = 240.00
}

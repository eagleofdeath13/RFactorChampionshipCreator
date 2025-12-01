Montreal_GP
{
  Filter Properties = SRGrandPrix OWChallenge
  Attrition = 30
  TrackName = Montreal GP
  EventName = Canadian Grand Prix
  GrandPrixName = Canadian Grand Prix //this must be the same as event name in order to sort circuit info correctly.
  VenueName = Montreal
  Location = Montreal, Quebec, Canada
  Length = 4.361km / 2.710 mi
  TrackType = Permanent Road Course
  Track Record = 
  HeadlightsRequired = true      // whether headlights are required at night
  TerrainDataFile = ..\Montreal.tdf  // terrain file override


  GarageDepth = 3.5
  Practice1Start = 11:00
  Practice2Start = 14:00
  Practice3Start = 10:00
  QualifyStart = 13:00
  RaceStart = 13:00
  RaceLaps = 70
  
  NumStartingLights=6

  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)

  ShadowMinSunAngle=10.0

  Latitude = 45.31     // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 0   // the direction of North in degrees (range: 0 to 359)
  RaceDate = June 25   // default date for the race

  SunriseAmbientRGB = (120,120,110)
  SunriseDirectionalRGB = (255,248,198)
  SunriseFogRGB = (204,174,240)

  DayAmbientRGB = (110,115,125)
  DayDirectionalRGB = (255,240,230)
  DayFogRGB = (205,215,230)

  SunsetAmbientRGB = (130,130,120)
  SunsetDirectionalRGB = (255,248,198)
  SunsetFogRGB = (204,196,122)

  NightAmbientRGB = (10,19,46)
  NightDirectionalRGB = (30,30,30)
  NightFogRGB = (0,0,0)

  SettingsFolder = Montreal
  SettingsCopy = Grip.svm
  SettingsCopy = Montreal.svm
  SettingsAI = Montreal.svm
  Qualify Laptime = 74.200
  Race Laptime = 77.500
}

Barcelona_GP
{
  Filter Properties = SRGrandPrix OWChallenge 2006
  Attrition = 30
  TrackName = Barcelona GP
  EventName = Spanish Grand Prix
  GrandPrixName = Spanish Grand Prix //this must be the same as event name in order to sort circuit info correctly.
  VenueName = Barcelona
  Location = Barcelona, Spain
  Length = 4.627 km / 2.875 mi
  TrackType = Permanent Road Course
  Track Record = 
  HeadlightsRequired = true      // whether headlights are required at night
  TerrainDataFile = ..\Barcelona.tdf // terrain file override


  GarageDepth = 1.0
  Practice1Start = 10:00
  Practice2Start = 13:00
  Practice3Start = 10:00
  QualifyStart = 13:00
  RaceStart = 13:00
  RaceLaps = 60
  
  NumStartingLights=6

  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)

  ShadowMinSunAngle=10.0

  Latitude = 41.34     // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 245 // the direction of North in degrees (range: 0 to 359)
  RaceDate = May 14    // default date for the race

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
  
  SettingsFolder = Barcelona
  SettingsCopy = Grip.svm
  SettingsCopy = Barcelona.svm
  SettingsAI = Barcelona.svm
  Qualify Laptime = 74.500
  Race Laptime = 76.000
}

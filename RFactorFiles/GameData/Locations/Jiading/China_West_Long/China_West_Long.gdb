China_West_Long	
{
  Filter Properties = SRGrandPrix OWChallenge
  Attrition = 30
  TrackName = Jiading West Long Circuit
  EventName =  Jiading Scramble
  GrandPrixName = Jiading Scramble  //this must be the same as event name in order to sort circuit info correctly.
  VenueName = Jiading Circuit
  Location = Jiading District, Shanghai, China
  Length = 
  TrackType = Permanent Road Course
  Track Record = 1:32.238
  HeadlightsRequired = true         // whether headlights are required at night
  TerrainDataFile = ..\Jiading.tdf  // terrain file override

  GarageDepth = 4.5
  FormationSpeedKPH = 110
  TestDaystart = 11:00
  Practice1Start = 11:00
  Practice2Start = 14:00
  Practice3Start = 11:00
  QualifyStart = 14:00
  RaceStart = 14:00
  RaceLaps = 53

  NumStartingLights=6
  
  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)

  ShadowMinSunAngle=10.0

  Latitude = 31.32       // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 0     // the direction of North in degrees (range: 0 to 359)
  RaceDate = October 01  // default date for the race

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

  SettingsFolder = Jiading
  SettingsCopy = Grip.svm
  SettingsCopy = Jiading.svm
  SettingsAI = Jiading.svm
  Qualify Laptime = 85.000
  Race Laptime = 86.500
}

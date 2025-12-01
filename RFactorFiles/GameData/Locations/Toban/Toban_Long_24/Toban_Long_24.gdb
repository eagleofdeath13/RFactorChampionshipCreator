Toban_Long_24
{
  Filter Properties = RoadCourse 2005 SRGrandPrix OWChallenge 
  Attrition = 30
  TrackName = Toban Raceway Park Long
  EventName = 24 Hours of Toban
  GrandPrixName = 24 Hours of Toban		//this must be the same as event name in order to sort circuit info correctly.
  VenueName = Toban Raceway Park
  Location = Toban, IN, USA
  Length = 4.012 km / 2.5 miles
  TrackType = Permanent Road Course
  Track Record = Brad Shuber, 113.669
  GarageDepth = 1.9

  // DefaultScoring overrides
  Practice1Day = Friday
  Practice1Start = 10:00
  QualifyDay = Saturday
  QualifyStart = 20:00
  WarmupDay = Sunday
  WarmupStart = 19:00
  RaceDay = Sunday
  RaceStart = 20:00
  RaceLaps = 960
  RaceTime = 1440

  // Time-of-day lighting 
  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)

  ShadowMinSunAngle=15.0

  Latitude = 0          // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 245  // the direction of North in degrees (range: 0 to 359)
  RaceDate = March 21   // default date for the race

  SunriseAmbientRGB = (120,120,110)      
  SunriseDirectionalRGB = (255,248,198)
  SunriseFogRGB = (204,174,240)

  DayAmbientRGB = (80,89,126)
  DayDirectionalRGB = (255,255,255)
  DayFogRGB = (203,214,236)

  SunsetAmbientRGB = (130,130,120)
  SunsetDirectionalRGB = (255,248,198)
  SunsetFogRGB = (204,196,122)

  NightAmbientRGB = (10,10,10)
  NightDirectionalRGB = (15,15,15)
  NightFogRGB = (0,0,0)

 
  SettingsFolder = Toban Long
  SettingsCopy = Grip.svm
  SettingsCopy = TOBAN_LONG.svm
  SettingsAI = TOBAN_LONG.svm
  Qualify Laptime = 55.669
  Race Laptime = 55.869
}

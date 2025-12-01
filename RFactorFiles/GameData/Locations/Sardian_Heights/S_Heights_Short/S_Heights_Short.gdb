S_Heights_Short
{
  Filter Properties = RoadCourse 2005 SRGrandPrix  
  Attrition = 30
  TrackName = Sardian Heights Short
  EventName = Sardian Heights 100
  GrandPrixName = Sardian Heights 100		//this must be the same as event name in order to sort circuit info correctly.
  VenueName = Sardian Heights Street Circuit
  Location = Sardian Heights, GA, USA
  Length = 1.35km / .84 Miles
  TrackType = Temporary Street Circuit
  Track Record = Brad Shuber, 43.669

  // DefaultScoring overrides
  TestDayStart = 13:00
  RaceLaps = 100
  RaceTime = 120

  // Time-of-day lighting
  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)

  ShadowMinSunAngle=15.0

  Latitude = 0          // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 11  // the direction of North in degrees (range: 0 to 359)
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

  NightAmbientRGB = (10,19,46)
  NightDirectionalRGB = (30,30,30)
  NightFogRGB = (0,0,0)

  SettingsFolder = Sardian Heights Short
  SettingsCopy = Grip.svm
  SettingsCopy = Sardian_Heights_Short.svm
  SettingsAI = Sardian_Heights_Short.svm
  Qualify Laptime = 55.669
  Race Laptime = 55.869
}

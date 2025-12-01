Brianza_HistB
{
  Filter Properties = SmallOval 2005 SRGrandPrix OWChallenge *
  Attrition = 30
  TrackName = Brianza Florio
  EventName = Brianza Classic - Round 3
  GrandPrixName = Brianza Classic - Round 3 //this must be the same as event name in order to sort circuit info correctly.
  VenueName = Autodromo Nazionale della Brianza
  Location = Milano, Italy
  Length = 6.8 km /  4.225 Miles
  TrackType = Permanent Road Course
  Track Record = , 81.046
  HeadlightsRequired = true  // whether headlights are required at night
  TerrainDataFile = ..\Brianza.tdf         // terrain file override

  GarageDepth = 4.0
  FormationSpeedKPH = 120
  RacePitKPH = 100.00
  QualPitKPH = 100.00
  NormalPitKPH = 80.00
  TestDaystart = 11:00
  Practice1Start = 11:00
  Practice2Start = 14:00
  Practice3Start = 11:00
  QualifyStart = 14:00
  RaceStart = 14:00
  RaceLaps = 53

  NumStartingLights=6

  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)

  ShadowMinSunAngle=15.0

  Latitude = 47.65     // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 340 // the direction of North in degrees (range: 0 to 359)
  RaceDate = September 10   // default date for the race

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

//ScoreboardFont=Brianza_SCOREFONT.tga // default is scoreboardfont.bmp
//ScoreboardBackground=SCORETOWERBKG.tga // default is scoreboardbkg.bmp

//ScoreboardMaxEntries=6 // how many car numbers can be displayed on tower (default is 32)
//ScoreboardStartX=0 // x-position in texture to write first car number (default is 0)
//ScoreboardStartY=1 // y-position in texture to write first car number (default is 10)
//ScoreboardIncX=0 // increment in x-position for each new car number (default is 0)
//ScoreboardIncY=43 // increment in y-position for each new car number (default is 16)
//ScoreboardScaleX=2.3 // scale multiplier for x (default is 1.0)
//ScoreboardScaleY=1.8 // scale multiplier for y (default is 1.0)

//////////////////////////////////////////////////////////////////////////////////////

  SettingsFolder = Brianza_HistB
  SettingsCopy = Grip.svm
  SettingsCopy = Brianza_HistB.svm
  SettingsAI = Brianza_HistB.svm
  Qualify Laptime = 82.00
  Race Laptime = 84.50
}

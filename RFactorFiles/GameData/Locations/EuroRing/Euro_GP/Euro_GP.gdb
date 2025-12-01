Euro_GP
{
  Filter Properties = 2005 2006 2007 SRGrandPrix OWChallenge *
  Attrition = 30
  TrackName = EuroRing_GP
  EventName = EuroRing Grand Prix
  GrandPrixName = EuroRing Grand Prix //this must be the same as event name in order to sort circuit info correctly.
  VenueName = EuroRing
  Location = Orkeny, Hungary // Örkény
  Length = 2.300 KM / 1.429 Miles
  TrackType = Road Course
  Track Record = F3000, 71.00
  HeadlightsRequired = true  // whether headlights are required at night
  TerrainDataFile = ..\Euroring.tdf         // terrain file override

  GarageDepth = 2.1
  FormationSpeedKPH = 100
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

  Latitude = 47.15     // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 340 // the direction of North in degrees (range: 0 to 359)
  RaceDate = September 10   // default date for the race

  SunriseAmbientRGB = (27,31,30, 120,120,120)      
  SunriseDirectionalRGB = (255,251,170, 120,120,120)
  SunriseFogRGB = (200,195,100)

  DayAmbientRGB = (57,71,79, 120,120,120)
  DayDirectionalRGB = (255,236,195, 120,120,120)
  DayFogRGB = (203,214,236, 203,214,236)

  SunsetAmbientRGB = (35,57,96, 120,120,120)
  SunsetDirectionalRGB = (255,159,58, 120,120,120)
  SunsetFogRGB = (204,196,122)

  NightAmbientRGB = (5,10,23)
  NightDirectionalRGB = (30,30,30)
  NightFogRGB = (0,0,0)

  NightLightThreshold=0.5

  PartlyCloudyScrollRate = (0.003, 0.001)
  OvercastScrollRate = (0.005, 0.002)
  SunApeture=0.06

  WetRoadAndLine = (0.0, 0.50)

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

///////////////////////////LOOSE OBJECT DATA///////////////////////////

sign_gate01=(500.0, 200.0, 100.0, 300.0, 65536.0, 2048.0, 0.70 ) // ( 5.0, 4.0, 2.0, 6.0, 1024.0, 44.8, 0.70 ) 
sign_gate02=(500.0, 200.0, 100.0, 300.0, 65536.0, 2048.0, 0.70 )

///////////////////////////////////////////////////////////////////////

  SettingsFolder = EuroRing_GP
  SettingsCopy = Grip.svm
  SettingsCopy = EuroRing_GP.svm
  SettingsAI = EuroRing_GP.svm
  Qualify Laptime = 73.0
  Race Laptime = 74.5
}

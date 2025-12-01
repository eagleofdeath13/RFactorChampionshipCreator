Orchard_Lake_Oval
{
  Filter Properties = SuperSpeedWay 2005 SRGrandPrix OWChallenge  
  Attrition = 30
  TrackName = Orchard Lake Speedway
  EventName = rFactor 400
  GrandPrixName = rFactor 400			//this must be the same as event name in order to sort circuit info correctly.
  VenueName = Orchard Lake Speedway
  Location = Washington, PA, USA
  Length = 2.91 km / 1.81 miles
  TrackType = Speedway
  TerrainDataFile = ..\orchard_lake.tdf         // terrain file override
  Track Record = Brad Shuber, 53.669
  FormationAndStart=2     // formation lap with rolling start (safety car leads the field and peels off into the pits)
  RollingStartLoc=1
  GarageDepth = 2.00

  // DefaultScoring overrides
  FormationLapSpeedKPH = 100
  RaceLaps = 400
  RaceTime = 240

  // Time-of-day lighting
  SkyBlendSunAngles=(-20.5,-1.0,11.5,25.5)

  ShadowMinSunAngle=15.0

  Latitude = 42          // degs from Equator (range: -90 to 90, positive is Northern Hemisphere)
  NorthDirection = 275   // the direction of North in degrees (range: 0 to 359)
  RaceDate = October 6   // default date for the race

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

///////////////////////////SCORETOWER DATA////////////////////////////////////////////

ScoreboardFont=orclake_scorefont.tga // default is scoreboardfont.bmp
ScoreboardBackground=scoretowerbkg.tga // default is scoreboardbkg.bmp

ScoreboardMaxEntries=35 // how many car numbers can be displayed on tower (default is 32)
ScoreboardStartX=0 // x-position in texture to write first car number (default is 0)
ScoreboardStartY=2 // y-position in texture to write first car number (default is 10)
ScoreboardIncX=0 // increment in x-position for each new car number (default is 0)
ScoreboardIncY=29 // increment in y-position for each new car number (default is 16)
ScoreboardScaleX=2.4 // scale multiplier for x (default is 1.0)
ScoreboardScaleY=1.2 // scale multiplier for y (default is 1.0)

//////////////////////////////////////////////////////////////////////////////////////

  Qualifying
  {
    Kevin Rodgers = 55.669
    Drake Evans = 55.700
    John Sullivan = 55.742
    Eric Fuller = 55.806
    Brandon Harvey = 56.001
    Corbin Legly= 56.100
    Greg Victors = 56.200
    Jacob Lewis = 56.250
    Chris Manning = 56.462
    Bruce Underwood = 56.500
    Joe Turnbill = 56.700
    Rick Grouper = 56.970
    Dan James = 57.000
    Brian Smith = 57.565
    Jack Cambell = 58.020
    Zander Cage = 58.345
    Wesley Crump = 58.500
    Rick Adams = 58.556
    Mike Lee = 58.612
    Bob Taylor = 58.756
    Elliot Matters = 60.1
    Lindsey Reid = 60.5

  }
  RaceEvents
  {
    Elliot Matters
    {
      29 = Engine
    }
    Lindsey Reid
    {
      33 = Suspension
    }
  }
  Weather
  {
    Practice1
    {
      Conditions = Best
      TrackWetness = Dry
      AmbientTemp = 30
      TrackTemp = 36
    }
    Practice2
    {
      Conditions = Best
      TrackWetness = Dry
      AmbientTemp = 31
      TrackTemp = 38
    }
    Practice3
    {
      Conditions = Best
      TrackWetness = Dry
      AmbientTemp = 29
      TrackTemp = 32
    }
    Practice4
    {
      Conditions = Best
      TrackWetness = Dry
      AmbientTemp = 30
      TrackTemp = 36
    }
    Qualify
    {
      Conditions = Best
      TrackWetness = Dry
      AmbientTemp = 29
      TrackTemp = 34
    }
    Warmup
    {
      Conditions = Best
      TrackWetness = Dry
      AmbientTemp = 24
      TrackTemp = 29
    }
    Race
    {
      Conditions = Nice
      TrackWetness = Dry
      AmbientTemp = 28
      TrackTemp = 32
    }
  }
  PitStopStrategies
  {
    Kevin Rodgers = 2 - 18,40
    Drake Evans  = 2 - 19,41
    John Sullivan = 2 - 18,40
    Eric Fuller = 2 - 29,41
    Brandon Harvey = 1 - 35
    Corbin Legly = 1 - 28
    Greg Victors = 1 - 30
    Jacob Lewis = 1 - 29
    Chris Manning = 1 - 32
    Bruce Underwood = 1 - 33
    Joe Turnbill = 2 - 22,32
    Rick Grouper = 2 - 23,33
    Dan James = 1 - 33
    Brian Smith = 1 - 27
    Jack Cambell = 1 - 28
    Zander Cage = 2 - 22,44
    Wesley Crump = 1 - 35
    Rick Adams = 1 - 36
    Mike Lee  = 1 - 27
    Bob Taylor  = 2 - 17,33
    Elliot Matters = 2 - 18,36
    Lindsey Reid = 1 - 32
  }

  SettingsFolder = Orchard Lake Oval
  SettingsCopy = OrchardLakeOval_NSCRS_Fast.svm
  SettingsCopy = OrchardLakeOval_NSCRS_Easy.svm
  SettingsAI = Orchard Lake.svm
  Qualify Laptime = 55.669
  Race Laptime = 55.869
}

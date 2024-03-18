# DASHBOARD

This is an example of a dashboard created to analyze the data of oil and gas wells in the Permain Basin.
To play the dashboard go into the Dashboard2dim folder and run the .bat file.

## Data Set

A sample data set can be found in the included file named “AnalysisData.csv”.
In this file, you will find data for 6098 wells from the Midland Basin,
with 1 row per well. The columns in the dataset are as follows:

| Column Name | Column Units | Description Column | Group |
| ------------|--------------|---------------------|-------|
|SurfaceHoleLongitude|Decimal Degrees| The Longitude of the surface hole location|Location|
|SurfaceHoleLatitude|Decimal Degrees| The Latitude of the surface hole location|Location|
|BottomHoleLongitude|Decimal Degrees| The Longitude of the bottom hole location|Location|
|BottomHoleLatitude|Decimal Degrees| The Latitude of the bottom hole location|Location|
| Operator | None (string) | Company that operates the well | Completion |
|CompletionDate | None (date) |Date in which the well was completed| Completion|
|Reservoir | None (string) | Geologic formation that the well is targeting |Geology|
|LateralLength_FT | Feet | Completed length of the horizontal well |Completion|
|ProppantIntensity_LBSPerFT | Pounds / Feet | Amount of proppant (frac sand) per lateral foot used to complete the well | Completion
|FluidIntensity_BBLPerFT | Barrels / Feet | Amount of fluid per lateral foot used to complete the well | Completion
|HzDistanceToNearestOffsetAtDrill | Feet | Horizontal distance to the nearest offset well - measured at the time the well was completed | Well spacing
|HzDistanceToNearestOffsetCurrent | Feet | Horizontal distance to the nearest offset well - measured at current time | Well spacing
|VtDistanceToNearestOffsetCurrent | Feet | Vertical distance to the nearest offset well - measured at the time the well was completed | Well spacing
|VtDistanceToNearestOffsetAtDrill | Feet | Vertical distance to the nearest offset well - measured at current time | Well spacing
|WellDepth                       | Feet | Depth of the horizontal well | Geology
|ReservoirThickness | Feet | Thickness of the targeted reservoir | Geology
|OilInPlace | Million barrels of oil / square mile | Amount of oil in place for the target reservoir | Geology
|Porosity | Percent | Porosity of the target reservoir | Geology
|ReservoirPressure | PSI |Pressure of the target reservoir | Geology
|WaterSaturation | Percent | % saturation of water in the target reservoir fluid | Geology
|StructureDerivative | Percent | % change in depth of the target formation - proxy for geologic faults | Geology
|TotalOrganicCarbon | Percent | % of total organic carbon of the target formation | Geology
|ClayVolume | Percent | % clay of the target reservoir | Geology
|CarbonateVolume | Percent | % carbonate of the target reservoir | Geology
|Maturity |Percent |Maturity of the target reservoir |Geology|
|TotalWellCost_USDMM |Millions of dollars |Total cost of the horizontal well |Completion|
|CumOil12Month |Barrels of oil| Amount of oil produced in the first 12 months of production |Production
|rowID |None (ID) |unique identifier for each well| ID

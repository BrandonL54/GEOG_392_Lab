import arcpy   

#assign bands
source = r"P:\GEOG 392\GEOG_392_Lab\Lab7\Imagery"
band1 = arcpy.sa.Raster(source + r"\Band1.tif") #blue
band2 = arcpy.sa.Raster(source + r"\Band2.tif") #green
band3 = arcpy.sa.Raster(source + r"\Band3.tif") #red
band4 = arcpy.sa.Raster(source + r"\Band4.tif") #NIR
combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\combined2.tif")

#Hillshade
azimuth = 315
altitude = 45
shadows = 'NO_SHADOWS'
z_factor = 1
arcpy.ddd.HillShade(
    source + r"\DEM.tif",
    source + r"\Hillshade3.tif", 
    azimuth, altitude, shadows, z_factor
)

#Slope
output_measurement = "DEGREE"
z_factor = 1
arcpy.ddd.Slope(
    source + r"\DEM.tif",
    source + r"\Slope3.tif",
    output_measurement, z_factor
)
print("success!")
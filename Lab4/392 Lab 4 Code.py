import arcpy

#create GDB
arcpy.CreateFileGDB_management(r'P:\GEOG 392\GEOG_392_Lab\Lab4', 'lab4test.gdb')

import CSV
lab4test = arcpy.MakeXYEventLayer_management(
     r'P:\GEOG 392\GEOG_392_Lab\Lab4\garages.csv',
     'X',
     'Y',
     'lab4feature'
 )
arcpy.FeatureClassToGeodatabase_conversion(lab4test,r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb')

#copying a shapefile
campus = r'P:\GEOG 392\GEOG_392_Lab\Lab4\Campus.gdb\Structures'
structures = r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb\copytest'
arcpy.Copy_management(campus, structures)

# #Re-projection
spatialref = arcpy.Describe(structures).spatialReference
arcpy.Project_management(
     r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb\lab4feature',
     r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb\garagesreproj',
     spatialref
 )

#buffer and intersect output
garagebuffer = arcpy.Buffer_analysis(
    r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb\garagesreproj',
    r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb\garagesreproj_buffer',
    250
# )
gbuffer = r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb\garagesreproj_buffer'
arcpy.Intersect_analysis(
    [
        r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb\garagesreproj_buffer',
        structures  
    ],
    r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb\intersect',
    'ALL'
)
arcpy.TableToTable_conversion(
    r'P:\GEOG 392\GEOG_392_Lab\Lab4\lab4test.gdb\intersect.dbf',
    r'P:\GEOG 392\GEOG_392_Lab\Lab4',
    'IntersectTab.csv'
)
import arcpy

#Set workspace/establish file locations
workspace = r'P:\GEOG 392\GEOG_392_Lab\Lab5\Lab5Tool'
campusgdb = workspace + "\Campus.gdb"
structures_og = campusgdb + "\Structures"
garages_tab = r'P:\GEOG 392\GEOG_392_Lab\Lab5\Lab5Tool\garages.csv'

#create GDB
#arcpy.CreateFileGDB_management(workspace, 'lab5_tool_gdb.gdb')
toolgdb = workspace + '\lab5_tool_gdb.gdb'
#import CSV
garages = arcpy.MakeXYEventLayer_management(
     workspace +'\garages.csv',
     'X',
     'Y',
     'garage_pt'
 )
arcpy.FeatureClassToGeodatabase_conversion(garages,toolgdb)

#copying a shapefile
structures = toolgdb + '\structures'
arcpy.Copy_management(structures_og, structures)

# #Re-projection
spatialref = arcpy.Describe(structures).spatialReference
garages_reproj = arcpy.Project_management(
      garages,
      toolgdb + '\garagesreproj',
      spatialref
  )

#User Inputs
garagename_input = input('please input a garage name: ')
bufferSize_input = int(input('please input a buffer zone size: '))

#Where Clause
wclause = "Name = '%s'" % garagename_input

cursor = arcpy.SearchCursor(garages_reproj, where_clause=wclause)

shouldProceed = False
for row in cursor:
    if row.getValue("Name") == garagename_input:
        shouldProceed = True

if shouldProceed:
    #Extract Garage for Analysis
    garageFeature = arcpy.Select_analysis(garages_reproj, toolgdb + r'/Name_%s' % (garagename_input), wclause)
    
    #buffer and intersect output
    garagebuffer = arcpy.Buffer_analysis(
        garageFeature,
        toolgdb + "/%s_buffed_%sm" % (garagename_input, bufferSize_input),
        bufferSize_input
    )

    #Intersect
    intersect = arcpy.Intersect_analysis(
        [
            garagebuffer,
            structures  
        ],
    toolgdb + '\intersect',
        'ALL'
    )
    arcpy.TableToTable_conversion(
        r'P:\GEOG 392\GEOG_392_Lab\Lab5\Lab5Tool\lab5_tool_gdb.gdb\intersect.dbf',
        workspace,
        'IntersectTab2.csv'
    )
    print("Job Done")
else:
    print("it didn't work, rip")
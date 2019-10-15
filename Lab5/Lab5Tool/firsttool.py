import arcpy
arcpy.env.workspace = r'C:\Users\hcai1\Desktop\Lecture15'
campus = arcpy.env.workspace + "\Campus.gdb"
structures = campus + "/Structures"

#take user input
buildingname_input = input('please input a building name:')
bufferSize_input = int(input('please input a buffer zone size: '))

# check if the input building exist or not
queryexp="BldgAbbr = '%s'" % buildingname_input
# %s is to pass the input building name to the string
# if buildingname_input is 'OMB', the queryexp is 'BldgAbbr = 'OMB'

cursor = arcpy.SearchCursor(structures, where_clause=queryexp)

shouldProceed = False
for row in cursor:
    if row.getValue("BldgAbbr") == buildingname_input:
        shouldProceed = True

if shouldProceed:
     # extract the input building feature from the feature class 'structures'
    buildingFeature = arcpy.Select_analysis(structures, campus + "/building_%s" % (buildingname_input), queryexp)
    
    # define the name for the buffer zone to be created
    buildingBuff = "/building_%s_buffed_%s" % (buildingname_input, bufferSize_input)

    # create Buffer zone for the selected building
    arcpy.Buffer_analysis(buildingFeature, campus + buildingBuff, bufferSize_input)


   # export the building features within the buffer zone
    arcpy.Clip_analysis(structures, campus + buildingBuff, campus + "/clip_%s" % (buildingname_input))

    # Remove the intermediate output to avoid Error if use the tool again
    arcpy.Delete_management(campus + "/building_%s" % (buildingname_input))
    
    # use print to tell the job is done
    print("We found the buildings you can reach!")

else:
    print("Seems we couldn't find the building you entered!Please change to another building")


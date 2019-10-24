# -*- coding: utf-8 -*-
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab 5 Garage Tool"
        self.description = "Create a Buffer and Intersect for a TAMU Garage"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="GDB Name(include.gdb)",
            name="GDBName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="CampusGDB",
            datatype="DEType",
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Selected Garage Name",
            name="GarageName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param6 = arcpy.Parameter(
            displayName="Buffer Distsance",
            name="BufferDistance",
            datatype="GPLong",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3, param4, param5, param6]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        #Set workspace/establish file locations
        workspace = r'P:\GEOG 392\GEOG_392_Lab\Lab5\Lab5Toolbox'
        campusgdb = parameters[4].valueAsText
        structures_og = campusgdb + "\Structures"
        garages_tab = r'P:\GEOG 392\GEOG_392_Lab\Lab5\Lab5Toolbox\garages.csv'

        #create GDB
        GDBparam0 = parameters[0].valueAsText
        GDBparam1 = parameters[1].valueAsText
        arcpy.CreateFileGDB_management(GDBparam0, '\\' + GDBparam1)
        toolgdb = GDBparam0 + '\\' + GDBparam1
        #import CSV
        CSVParam2 = parameters[2].valueAsText
        CSVParam3 = parameters[3].valueAsText
        garages = arcpy.MakeXYEventLayer_management(
            CSVParam2,
            'X',
            'Y',
            CSVParam3
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
        garagename_input = parameters[5].valueAsText
        bufferSize_input = int(parameters[6].valueAsText)

        #Where Clause
        wclause = "Name = '%s'" % garagename_input

        cursor = arcpy.SearchCursor(garages_reproj, where_clause=wclause)

        proceed = False
        for row in cursor:
            if row.getValue("Name") == garagename_input:
                proceed = True

        if proceed:
            #Extract Garage for Analysis
            garageFeature = arcpy.Select_analysis(garages_reproj, toolgdb + '/Name_%s' % (garagename_input), wclause)
            
            #buffer and intersect output
            garagebuffer = arcpy.Buffer_analysis(
                garageFeature,
                toolgdb + "\%s_buffed_%sm" % (garagename_input, bufferSize_input),
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
                'IntersectTab.csv'
            )
        else:
            messages.addErrorMessage('Error: check inputs')
            raise arcpy.ExecuteError
                
        return None
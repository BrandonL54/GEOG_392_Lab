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
        self.label = "Graduated Colors Renderer"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Input Map",
            name="inputmap",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="Layer Name",
            name="Layer",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Output Map Name",
            name="output",
            datatype="String",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2]
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
        """The source code of the tool."""
    
        ###PROGRESSOR###
        #variables
        readTime = 1
        start = 0
        max = 100

        #set up progressor
        arcpy.SetProgressor(
            "step", 
            "Verifying Layer..."
            , start, max, 33
        )
        time.sleep(readTime)
        #results pane message
        arcpy.AddMessage('Verifying Layer...')
        #establish variables
        project = arcpy.mp.ArcGISProject(
            parameters[0].valueAsText
        )
        campus = project.listMaps('Map')[0]

        # Loop through available layers in the map
        for layer in campus.listLayers():
            # Check that the layer is a feature layer
            if layer.isFeatureLayer:
                # Obtain a copy of the layer's symbology
                symbology = layer.symbology
                # Makes sure symbology has an attribute "renderer"
                if hasattr(symbology, 'renderer'):
                    # Check if the layer's name is "Structures"
                    if layer.name == parameters[1].valueAsText:
                        #progressor step
                        arcpy.SetProgressorPosition(33)
                        arcpy.SetProgressorLabel("Layer Verified! Rendering New Map...")
                        arcpy.AddMessage("Layer Verified! Rendering New Map...")
                        # Update the copy's renderer to be "UniqueValueRenderer"
                        symbology.updateRenderer('GraduatedColorsRenderer')
                        # Use "Shape_Area" field for render
                        symbology.renderer.classificationField = 'Shape_Area'
                        #how many breaks will we have
                        symbology.renderer.breakCount = 10
                        #color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Orange*')[0]
                        # Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology # Very important step
                        #progressor step
                        arcpy.SetProgressorPosition(67)
                        arcpy.SetProgressorLabel("Rendered! Saving Map...")
                        arcpy.AddMessage('Rendered! Saving Map...')
                    else:
                        print("NOT Structures")
        project.saveACopy(parameters[2].valueAsText)
                #progressor step
        arcpy.SetProgressorPosition(max)
        arcpy.SetProgressorLabel("Success!")
        arcpy.AddMessage('Success!')
        return None

import arcpy

#establish variables
project = arcpy.mp.ArcGISProject(
    r'P:\GEOG 392\GEOG_392_Lab\Lab6\Lab6Proj\Lab6Proj.aprx'
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
            if layer.name == "Structures":
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
            else:
                print("NOT Structures")
project.saveACopy(r'P:\GEOG 392\GEOG_392_Lab\Lab6\Lab6Proj\Lab6Proj_copy.aprx')
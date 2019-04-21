#If the error is No permission to perform the operation upon the datasource. May need to run as admin

import arcpy
import random
import os 
arcpy.env.overwriteOutput = True
#parameters for tool
In_Feat = arcpy.GetParameterAsText(0)
Purpose = arcpy.GetParameterAsText(1)
Output = arcpy.GetParameterAsText(2)

#random integer to select one of the shape projections
x = random.randint(0,3)


#Create a txt file to store data infomation that is usefull for the user 
f= open(Output+".txt","w+")


#Area projection for Ohio
Area = [
    "NAD 1983 (2011) Contiguous USA Albers"
    ]

#Distance projection for Ohio
Distance = ["USA Contiguous Equidistant Conic"]

#Shape projections for Ohio
Shape = [
"NAD 1983 (2011) UTM Zone 17N", 
"North America Lambert Conformal Conic", 
"NAD 1983 (2011) StatePlane Ohio South FIPS 3402 (US Feet)", 
"NAD 1983 (2011) StatePlane Ohio North FIPS 3401 (US Feet)"
]



 #Following lists hold information about the projections
areaInfo = ["\nProjection: NAD 1983 (2011) Contiguous USA Albers \nThis is a conic projection with two standard parallels. This greatly reduces distortion compaired to one. \nNote: A standard parallel in conic projections is the place where the cone touches the globe and thus has the least amount of distortion.\nThis makes for little distortion in East to West data though North and South will be more distorted.\n This projection best preserves area though both shape and distance are preserved at the parallels."]

distInfo = ["\nProjection: USA Contiguous Equidistant Conic \nAs the name inplies, this conic projection is best used for distance analysis. \nTo achieve this, circles of latitude are placed evenly at the meridians. In essence this results in perfectly square graticules at these points. \nThis allows for correct distance calculations at the standard parallels though area and shape are distorted.\nNote:Distance preservation is only between two points along the two standard parallels."]

shapeInfo = ["\nProjection: NAD 1983 (2011) UTM Zone 17N\nThis projection uses the Universal Transverse Mercator (UTM) Projection which is actually a cartesian coordinate system which divides the world into 60 sections each with a 6 degree width (360/6 = 60). The contiguous United States spans zones 10-19 with ohio being located in 17 (though the very eastern edge is in 16)\nThe actual projection is based on the secant transverse Mercator (a cylinder projection).\n Think of this like putting an orange inside a cylinder. The center of the cylinder creates a meridian. Rotating the cylinder creates a new meridian and this is how the UTM is created.\n\nImportant Note: UTM does not use lat long coordinates. Instead it uses false easting and northings. Because each zone has a new central meridian which is 500,000 meters in length.\n\nDue to the small degree span, UTM preserves everything quite well but is only useful for smaller areas such as a state or small country.",  
"\nProjection: North America Lambert Conformal Conic\nThis conic projection has standard paralels at 20 and 50 degrees North.\nOf interest with this projection is its frequent use in aeronautical charts\ndue to its ability to replicate a great-circle route between two points.\n Thus this projection is applicable to the middle latitudes.\n This would be a good choice if you need to use states adjacent to Ohio as well.\nNote: Latitude range is best kept under 35 degrees and shape is generally only preserved at a small scale.", 
"\nProjection: NAD 1983 (2011) StatePlane Ohio South FIPS 3402 (US Feet)\nThis is one of two projections in Ohio's state plane system.\nThe system is divided at county lines with south being used for Licking County and below. The state capital of Columbus is best used with the south projection.\nOhio's state plane system is based on the Lambert Conformal Conic projection used for the mid latitudes. Measures in this coordinate system are in feet with all possitive values for Ohio.\nNote: A map and more information for the state plane can be found here:\nhttp://geosurvey.ohiodnr.gov/portals/geosurvey/PDFs/Misc_State_Maps&Pubs/coordsys.pdf", 
"\nProjection: NAD 1983 (2011) StatePlane Ohio North FIPS 3401 (US Feet)\nThis is one of two projections in Ohio's state plane system.\nThe system is divided at county lines with north being used for Deleware County and above. The northern city of Cleveland is best used with the north projection.\nOhio's state plane system is based on the Lambert Conformal Conic projection used for the mid latitudes. Measures in this coordinate system are in feet with all possitive values for Ohio.\nNote: A map and more information for the state plane can be found here:\nhttp://geosurvey.ohiodnr.gov/portals/geosurvey/PDFs/Misc_State_Maps&Pubs/coordsys.pdf"]


#fuction to project 
arcpy.env.overwriteOutput = True
def ed_Project(In_Feat=In_Feat, Purp_List=Area[0], Output=Output):
    fieldCount = 1
    #create a .prj with a dummy coordinate which can be changed
    prj = open(In_Feat+".prj", "w+")    
    crs_string = 'GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'    
    prj.write(crs_string)    
    prj.close()

    #using the dummy projection re-define and then project the data in the selected projection
    scratch_name = arcpy.CreateScratchName("temp", data_type="Shapefile", workspace=arcpy.env.scratchFolder)
    
    #using the dummy projection re-define and then project the data in the selected projection
    sr = arcpy.SpatialReference(In_Feat+".prj")
    topro = arcpy.Project_management(In_Feat, scratch_name, sr)
    sr = arcpy.SpatialReference(Purp_List)
    arcpy.Project_management(topro, Output, sr)
    desc = arcpy.Describe(In_Feat)

    #useful information for the user placed in the .txt
    f.write("Your Filepath: "+Output+"\n"+100*'-'+"\nData Information: \n\nX,Y min: ({0},{1})\nX, Y max: ({2},{3})\n\nFields:\n".format(desc.extent.XMin, desc.extent.YMin,desc.extent.XMax, desc.extent.YMax))
    fields = arcpy.ListFields(In_Feat)
    for field in fields:
        f.write(str(fieldCount)+". {0} is a type of {1} with a length of {2}\n".format(field.name, field.type, field.length))
        fieldCount+=1

#based on purpose run the code
if Purpose == "Area":
    ed_Project(In_Feat, Area[0], Output)
    f.write(areaInfo[0])
    
elif Purpose == "Distance":
    ed_Project(In_Feat, Distance[0], Output)
    f.write(distInfo[0])
    
elif Purpose == "Shape":
    ed_Project(In_Feat, Shape[x], Output)
    f.write(shapeInfo[x])
    

f.write("\n\nIf you are having trouble reading this file it may help to enable wordwrapping")
f.close()
os.startfile(Output+".txt")

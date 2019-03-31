import arcpy
import random

In_Feat = arcpy.GetParameterAsText(0)
Purpose = arcpy.GetParameterAsText(1)
Output = arcpy.GetParameterAsText(2)
x = random.randint(0,3)
arcpy.AddMessage("X = {0}".format(x))


Area = [
    "NAD 1983 (2011) Contiguous USA Albers"
    ]


Distance = ["USA Contiguous Equidistant Conic"]

Shape = [
"NAD 1983 (2011) UTM Zone 17N", 
"North America Lambert Conformal Conic" , 
"NAD 1983 (2011) StatePlane Ohio South FIPS 3402 (US Feet)", 
"NAD 1983 (2011) StatePlane Ohio North FIPS 3401 (US Feet)"
]

def ed_Project(In_Feat=In_Feat, Purp_List=Area[0], Output=Output):
    
    sr = arcpy.SpatialReference(Purp_List)
    arcpy.Project_management(In_Feat, Output, sr)
    #arcpy.DefineProjection_management(Output, sr)


if Purpose == "Area":
    ed_Project(In_Feat, Area[0], Output)

elif Purpose == "Distance":
    ed_Project(In_Feat, Distance[0], Output)

elif Purpose == "Shape":
    ed_Project(In_Feat, Shape[x], Output)
 
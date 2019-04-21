# If the error is No permission to perform the operation upon the datasource. May need to run as admin

import arcpy
import random
import os
arcpy.env.overwriteOutput = True
# parameters for tool
In_Feat = arcpy.GetParameterAsText(0)
Prj = arcpy.GetParameterAsText(1)
Output = arcpy.GetParameterAsText(3)
Grat_points = arcpy.GetParameterAsText(2)


# List of all projections
Projections = [54032,
54024,
54028,
54014,
102034,
54059,
54091,
54008,
54051,
54078,
54029,
54025]

Str_pro = ["Azimuthal Equidistant", "Bonne", "Cassini", "Eckert II", "Gnomonic", "Goode Homolosine",
    "Peirce Quincuncial", "Sinusoidal", "Cube", "Natural Earth II", "Van der Grinten", "Hotine Oblique Mercator"]
 # Following lists hold information about the projections
ProjectionsInfo = ["\n\nProjection: Azimuthal Equidistant Projection\nIt is an azimuthal map projection in which all points on the map are at proportionally correct distances from the center point, and all points on the map are at the correct direction from the center. A useful application for this projection is a polar projection that shows all the line of longitude as straight, with their distances from the pole being represented correct. The flag of the United Nations has a map using the polar azimuthal equidistant projection on it.",
"\n\nProjection: Bonne Projection\nUsed as early as 1511, the Bonne projection is a pseudoconical equal-area map projection with an interesting butterfly or heart shape. It maintains accurate shapes along the central meridian and the standard parallel but distorts progressively away from those areas. Because of this, it is best at mapping “t” shaped regions. This projection has been used extensively on maps depicting Europe and Asia.",
"\n\nProjection: Cassini Projection\nFirst described in 1745, the Cassini projection is the transverse aspect of the equirectangular projection in that the globe is first rotated so that the central meridian becomes the “equator,” and then the normal equirectangular projection is applied. This projection has always been applied to models of the earth as an ellipsoid, which greatly complicates the mathematical development but is useful for surveying. The use of this projection has largely been superseded by the transverse Mercator projection.",
"\n\nProjection: Eckert II Projection\nThe Eckert II projection is an equal-area pseudocylindrical map projection in which the network of longitude and latitude lines of the equatorial aspect consist of straight lines, and the outer boundary has the distinctive shape of an elongated hexagon. It was first described in 1906 as one of a series of pairs of pseudocylindrical projections where in each pair, the meridians have the same shape, the odd-numbered projection has equally spaced parallels, and the even-numbered projection has parallels spaced to preserve area. The pair to Eckert II is the Eckert I projection.",
"\n\nProjection: North Pole Gnomonic Projection\nThe Gnomonic projection shows all great circles as straight lines, which results in any straight line segment showing a geodesic, which is the shortest route between the segment’s two endpoints. Less than half the globe can be projected onto the map, and no distortion occurs at the center, but it increases rapidly away from it. Gnomonic projections are used in seismic work because seismic waves tend to travel along great circles. Here the North Pole us used as the origin point.",
"\n\nProjection: Goode Homolosine Projection\nFirst developed in 1923 to provide an alternative to the Mercator projection for portraying global areal relationships, the Goode Homolosine projection is a pseudocylindrical, equal-area composite map projection that is used for world maps. Its equal-area property makes it useful for presenting spatial distribution of phenomena. It is sometimes known as an “orange peel map” because of its resemblance to a flattened, hand-peeled orange rind.",
"\n\nProjection: Peirce Quincuncial Diamond Projection\nDeveloped in 1879, the Peirce Quincuncial projection is a conformal map projection that has the distinctive property that it can be tiled forever on the plane, with the edge-crossings being completely smooth except for four singular points per tile. This projection is typically oriented so that the north pole lies at the center, and it has seen use in digital photography for portraying 360° views. Here a diamond is portrayed",
"\n\nProjection: Sinusoidal Projection\nAppearing as early as 1570, the Sinusoidal projection is a pseudocylindrical equal-area projection where scale is constant along the central meridian, and east-west scale being constant throughout the whole map. Because of this, the length of each parallel on the map is proportional to the cosine of the latitude, which is the same as on a globe. The true distance between two points on the map can be measured on the map as the vertical distance between the parallels that intersect the meridian at those points.",
"\n\nProjection: Cube\nThis projection is just as the name implies, a cube. This projection is an unrapped cube. There aren't any practical uses for this projection though you can print out this map and reasemble the cube for a unique desk decoration.",
"\n\nProjection: Natural Earth II\nCreated by Tom Patterson, Bojan Savric, and Bernhard Jenny in 2015, this more recent projection was created as a compromise Pseudocylindric similar to the Robinson or Winkel Tripel. The difference here are that the sides bulge considerably less. It is intended for use when such size considereations need be taken into acount.",
"\n\nProjection: Van der Grinten\nAlphons J. van der Grinten invented this projection in 1898 and was used exstensivley for refrence maps up until widespread adoption of the Robinson. This is a compromising projection and was developed to be distort less than the Mercator projection. To do this, diistortion increases from the equator with the poles being greatly distorted.",
"\n\nProjection: Hotine Oblique Mercator\nAlso reffered to as the oblique cylindrical orthomorphic is an oblique rotation of the Mercator projection. Although many different types of this rotation exist, the purpose is to create a conformal area for obliquely shaped areas. Examples include the Alaskan panhandle or specific regions within Switzerland."]

if Prj == "Random":
    # random integer to select one of the shape projections
    x = random.randint(0, 11)
    arcpy.AddMessage(x)
    Prj = Projections[x]
else:
    x = 0
    for p in Str_pro:
        if Prj == p:
            Prj = Projections[x]
            break
        else:
            x += 1

# Create a txt file to store data infomation that is usefull for the user
f = open(Output+".txt", "w+")


# Area projection for Ohio


# fuction to project
arcpy.env.overwriteOutput = True


def ex_Project(In_Feat=In_Feat, Prj=Prj, Output=Output):
    fieldCount = 1
    # create a .prj with a dummy coordinate which can be changed
    prjFile = open(In_Feat+".prj", "w+")
    crs_string = 'GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
    prjFile.write(crs_string)
    prjFile.close()

    # using the dummy projection re-define and then project the data in the selected projection
    scratch_name = arcpy.CreateScratchName(
        "temp", data_type="Shapefile", workspace=arcpy.env.scratchFolder)

    # using the dummy projection re-define and then project the data in the selected projection
    sr = arcpy.SpatialReference(In_Feat+".prj")
    topro = arcpy.Project_management(In_Feat, scratch_name, sr)
    sr = arcpy.SpatialReference(Prj)
    arcpy.Project_management(topro, Output, sr)
    desc = arcpy.Describe(In_Feat)

    insertLyr = Output
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    map1 = aprx.activeMap.name
    aprxMap = aprx.listMaps(map1)[0]
    aprxMap.addDataFromPath(insertLyr)

    # useful information for the user placed in the .txt
    f.write("Your Filepath: "+Output+"\n"+100*'-'+"\nData Information: \n\nX,Y min: ({0}, {1})\nX, Y max: ({2}, {3})\n\nFields:\n".format(
        desc.extent.XMin, desc.extent.YMin, desc.extent.XMax, desc.extent.YMax))
    fields = arcpy.ListFields(In_Feat)
    for field in fields:
        f.write(str(fieldCount)+". {0} is a type of {1} with a length of {2}\n".format(
            field.name, field.type, field.length))
        fieldCount += 1


def gratANDpoints():
    if Output[-4:] == ".shp":
        gratOut = Output[:-4]+"_Graticule.shp"
        pointOut = Output[:-4]+"_Points.shp"
    else:
        gratOut = gratOut
        pointOut = pointOut

    arcpy.CreateFishnet_management(gratOut,"-20037507.073813 -19971868.872273","-20037507.073813  19971868.884530","1000000","1000000","0","0","20037507.061556 19971868.884530","NO_LABELS","#","POLYGON")
    arcpy.DefineProjection_management(gratOut, 54004)
    arcpy.GeneratePointsAlongLines_management(gratOut, pointOut, "PERCENTAGE", Percentage=50)
       
    insertLyr = pointOut
    insertLyr2 = gratOut
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    map1 = aprx.activeMap.name
    aprxMap = aprx.listMaps(map1)[0]
    move = aprxMap.listLayers()[0]
    aprxMap.addDataFromPath(insertLyr2)
    aprxMap.addDataFromPath(insertLyr)
    ref = aprxMap.listLayers()[0]
    aprxMap.moveLayer(ref, move)    

ex_Project(In_Feat, Prj, Output)

if Grat_points == "true":
    gratANDpoints()
    
f.write(ProjectionsInfo[x])
    
f.write("\n\n\n\n\n\nIf you are having trouble reading this file it may help to enable wordwrapping")
f.close()
os.startfile(Output+".txt")


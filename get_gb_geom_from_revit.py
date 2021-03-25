import System
gb_cl = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType()
wall_cl = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Walls).WhereElementIsNotElementType()

gbs = []
walls = []
cols = []
for el in gb_cl:
    if str(el.StructuralMaterialType).lower() == 'concrete':
        if str(el.StructuralType).lower() == 'beam':
            gbs.append(el)
        elif str(el.StructuralType).lower() == 'column':
            cols.append(el)
for el in wall_cl:
    if str(el.StructuralUsage).lower() == 'bearing':
        walls.append(el)

#Set the file path
filepath = 'C:/Users/civy/Desktop/revit_output.txt'
 
#Delete the file if it exists.
if (System.IO.File.Exists(filepath) == True):
    System.IO.File.Delete(filepath)
 
#Create the file
file = System.IO.StreamWriter(filepath)
 
#Write some things to the file
for el in gbs:
    start_loc = el.Location.Curve.GetEndPoint(0).ToString()
    end_loc = el.Location.Curve.GetEndPoint(1).ToString()
    width_param = el.LookupParameter('Beam Width')
    depth_param = el.LookupParameter('Beam Depth')
    if width_param:
        width = width_param.AsDouble()
    else:
        width = .25
    if depth_param:
        depth = depth_param.AsDouble()
    else:
        depth = .25

    file.WriteLine('%s %s %f %f' %(start_loc, end_loc, width, depth))

for el in walls:
    start_loc = el.Location.Curve.GetEndPoint(0).ToString()
    end_loc = el.Location.Curve.GetEndPoint(1).ToString()
    width_param = el.Width
    depth_param = el.LookupParameter('Unconnected Height')
    if width_param:
        width = width_param
    else:
        width = .25
    if depth_param:
        depth = depth_param.AsDouble()
    else:
        depth = .25

    file.WriteLine('%s %s %f %f' %(start_loc, end_loc, width, depth))
 
#Close the StreamWriter
file.Close()


# # VERY USEFUL CODE TO FIND PARAMETERS OF ELEMENTS IN REVIT
# for param in el.Parameters:
#     print(param.Definition.Name)

# h = el.GetParameters('Depth')
# print(h[0].AsDouble())
# Python Script, API Version = V17
    
def SelectFacesWithType(type):
'''
Loop through all faces in the root part and return list of faces whos shape equals provided type.
'''
# Get all bodies
    bodies = GetRootPart().GetChildren[IDesignBody]()
    faces = List[IDesignFace]()

    for body in bodies:
        for desFace in body.Faces:
            surface = desFace.Shape.Geometry
            if isinstance(surface, type):
                faces.Add(desFace)

    return faces

#Select Cylinders for tubes, and assing NS to them.
selected_cylinders = SelectFacesWithType(Cylinder)
result_tubewalls = NamedSelection.Create(Selection.Create(selected_cylinders), Selection())
result_tubewalls = NamedSelection.Rename("Group1", "tubewalls")
#Endblock

# Create Named Selection Group ## Find a logic to define the two inlet and outlets automatically
primarySelection1 = Selection.Create(GetRootPart().Bodies[0].Faces[3]) #This can change. Is equal in dimension to outlet as of now.
secondarySelection1 = Selection()
result_inlet = NamedSelection.Create(primarySelection1, secondarySelection1)
result_inlet = NamedSelection.Rename("Group1", "inlet")
#Endblock

#Create NS group for outlet
primarySelection2 = Selection.Create(GetRootPart().Bodies[0].Faces[18])
secondarySelection2 = Selection()
result_inlet = NamedSelection.Create(primarySelection2, secondarySelection2)
result_inlet = NamedSelection.Rename("Group1", "outlet")
#Endblock

#Create NS for manifold-walls
all_except_manifoldwalls = Selection.CreateByGroups("tubewalls","inlet", "outlet")
manifoldwalls = s1.GetInverse()
primarySelection3 = manifoldwalls
secondarySelection3 = Selection()
result_manifolds = NamedSelection.Create(primarySelection3, secondarySelection3)
result_manifolds = NamedSelection.Rename("Group1", "manifold-walls")
#Endblock

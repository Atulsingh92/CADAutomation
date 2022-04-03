n=7

for i in range(n):
    case=i
    # Open File
    DocumentOpen.Execute(r"C:\\Local\\SW-tests\\analysis\\"+str(case)+"\\"+str(case)+".SLDPRT.pmdb",FileSettings1,GetMaps("2cacdaca"))
    # If FileSettings1 gives an error. Import a file and close it. Rerun the script.
    # EndBlock

    # Save File
    DocumentSave.Execute(r"C:\\Local\\SW-tests\\analysis\\"+str(case) +"\\"+str(case)+".scdoc",FileSettings1)
    # EndBlock
    wall_face = GetRootPart().Bodies[0].Faces[0]
    groove_face = GetRootPart().Bodies[0].Faces[3]
    blend1_face =  GetRootPart().Bodies[0].Faces[4]
    blend2_face = GetRootPart().Bodies[0].Faces[5]
    wall_area = wall_face.Area
    groove_area=groove_face.Area + blend1_face.Area + blend2_face.Area
    wetperimeter = wall_area+groove_area

   # print(wetperimeter)
    volume = GetRootPart().Bodies[0].MassProperties
    resvolume = volume.Mass
   # print (resvolume)
    #hydraulicD = 4*resvolume/wetperimeterSelection.Create(GetRootPart().Bodies[0].Faces[0])
    hydraulicD = 4*resvolume/wetperimeter
    print("D_Hydraulic for "+str(case)+" is: " , hydraulicD)
    print("\n")
    
    GetActiveWindow().Close()

import win32com.client
import pythoncom

class commSW:
    def __init__(self):
        self.drawing = self.drawing();
        self.utils = self.utils();
        
    class utils:
        def __init__(self):
            pass;
            
            def _getTolType(self, tolTypeNum):
                tolType = {
                        1  : 'swTolBASIC',
                        2  : 'swTolBILAT',
                        10 : 'swTolBLOCK',
                        7  : 'swTolFIT',
                        9  : 'swTolFITTOLONLY',
                        8  : 'swTolFITWITHTOL',
                        11 : 'swTolGeneral',
                        3  : 'swTolLIMIT',
                        6  : 'swTolMAX',
                        7  : 'swTolMETRIC',
                        5  : 'swTolMIN',
                        0  : 'swTolNONE',
                        4  : 'swTolSYMMETRIC',
                        };
                        
                return tolType[tolTypeNum];
        
        def _getDimType(self, dimTypeNum):
                dimType = {
                        3   : 'swAngularDimension',
                        4   : 'swArcLengthDimension',
                        10  : 'swChamferDimension',
                        6   : 'swDiameterDimension',
                        0   : 'swDimensionTypeUnknown',
                        11  : 'swHorLinearDimension',
                        7   : 'swHorOrdinateDimension',
                        2   : 'swLinearDimension',
                        1   : 'swOrdinateDimension',
                        5   : 'swRadialDimension',
                        13  : 'swScalarDimension',
                        12  : 'swVertLinearDimension',
                        8   : 'swVertOrdinateDimension',
                        9   : 'swZAxisDimension',
                        };
            
                if dimTypeNum == 0:
                    return dimType[dimTypeNum].replace('sw','');
                else:
                    return dimType[dimTypeNum].replace('sw','').replace('Dimension','');
        
        def _getDocUnits(self, swModel):
            dimUnit = {
                    'millimeters'   : 'mm',
                    'degrees'       : 'deg',
                    'meters'        : 'm',
                    'radians'       : 'rad',
                    'inches'        : 'in'
                    };
        
            docUserUnitLinear   = swModel.GetUserUnit(win32com.client.VARIANT(pythoncom.VT_I4, 0));
            docUserUnitAngular  = swModel.GetUserUnit(win32com.client.VARIANT(pythoncom.VT_I4, 1));
        
            linearunit  = docUserUnitLinear.GetFullUnitName(True);
            angularunit = docUserUnitAngular.GetFullUnitName(True);
            
            return dimUnit[linearunit], dimUnit[angularunit];
        
        def _getModelLengthUnits(self, LengthUnit):
            unitType = {
                    6   : 'ANGSTROM',
                    1   : 'CM',
                    4   : 'FEET',
                    5   : 'FEETINCHES',
                    3   : 'INCHES',
                    2   : 'METER',
                    8   : 'MICRON',
                    9   : 'MIL',
                    0   : 'MM',
                    7   : 'NANOMETER',
                    10  : 'UIN',
                    };
        
            return unitType[LengthUnit];
        
        def _getModelUnits(self, swModel):
            LengthUnit, FractionBase, FractionValue, SignificantDigits, RoundToFraction = swModel.GetUnits;
            
            return self._getModelLengthUnits(LengthUnit)
        
    def runMacro(self, macroPath, moduleName, procedureName, *args):
    
        arg1 = win32com.client.VARIANT(pythoncom.VT_BSTR, macroPath);
        arg2 = win32com.client.VARIANT(pythoncom.VT_BSTR, moduleName);
        arg3 = win32com.client.VARIANT(pythoncom.VT_BSTR, procedureName);
        arg4 = win32com.client.VARIANT(pythoncom.VT_I4, 1);
        arg5 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 20);
        
        if not args:
            response = swcom.RunMacro2(arg1, arg2, arg3, arg4, arg5);
        elif args[0] == "C#":
            response = swcom.RunMacro2(arg1, "", arg3, arg4, arg5);
    
        if response == True:
            return None
        else:
            print('Macro execution failed.')
        
    def startSW(self, *args):
        """
        Start the SolidWorks process.
        If there are multiple versions of SolidWorks installed on the system
        the the method takes an argument of the version year of the program.
        
        Parameters
        ----------
        args : str (optional)
        Version year of SolidWorks to start if there are multiple versions
        of SolidWorks installed.
        
        """
        
        import subprocess as sb
        
        if not args:
            SW_PROCESS_NAME = r'C:/Program Files/SOLIDWORKS Corp/SOLIDWORKS/\
            SLDWORKS.exe';
            sb.Popen(SW_PROCESS_NAME);
        else:
            year= int(args[0][-1]);
            SW_PROCESS_NAME = "SldWorks.Application.%d" % (20+(year-2));
            win32com.client.Dispatch(SW_PROCESS_NAME);
    #
    def shutSW(self):
        """
        Stop the sldwrks.exe process running currently.
        Does not take any arguments.

        """

        import subprocess as sb
            
        sb.call('Taskkill /IM SLDWORKS.exe /F');
    #
    def connectToSW(self):
        """
        Establish a connection to SolidWorks.
        
        """
            
        global swcom
        swcom = win32com.client.Dispatch("SLDWORKS.Application");
    #
    def openAssy(self, prtNameInp):
        """
        Opens an SolidWorks assembly.
        
        Parameters
        ----------
        prtNameInp : str
        The file location of the assembly with assembly name appended at
        the end.
        E.g.: r"myDirectory\mySubDirectory\myAssembly"
        
        """
            
        import os
            
        self.prtNameInn = prtNameInp;
        self.prtNameInn = self.prtNameInn.replace('\\','/');
        #
        if os.path.basename(self.prtNameInn).split('.')[-1].lower() == 'sldasm': 
            pass;
        else:
            self.prtNameInn+'.SLDASM'
        #
        openDoc     = swcom.OpenDoc6;
        arg1        = win32com.client.VARIANT(pythoncom.VT_BSTR, self.prtNameInn);
        arg2        = win32com.client.VARIANT(pythoncom.VT_I4, 2);
        arg3        = win32com.client.VARIANT(pythoncom.VT_I4, 1);
        arg5        = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 2);
        arg6        = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 128);
        #
        openDoc(arg1, arg2, arg3, "", arg5, arg6);
    #
    def openPrt(self, prtNameInp):
        """
        Opens an SolidWorks part.
        
        Parameters
        ----------
        prtNameInp : str
        The file location of the part with part name appended at
        the end.
        E.g.: r"myDirectory\mySubDirectory\myPart"
        
        """
    
        import os
    
        self.prtNameInn = prtNameInp;
        self.prtNameInn = self.prtNameInn.replace('\\','/');
        #
        if os.path.basename(self.prtNameInn).split('.')[-1].lower() == 'sldprt': 
            pass;
        else:
            self.prtNameInn+'.SLDPRT'
        #
        openDoc     = swcom.OpenDoc6;
        arg1        = win32com.client.VARIANT(pythoncom.VT_BSTR, self.prtNameInn);
        arg2        = win32com.client.VARIANT(pythoncom.VT_I4, 1);
        arg3        = win32com.client.VARIANT(pythoncom.VT_I4, 1);
        arg5        = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 2);
        arg6        = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 128);
        #
        openDoc(arg1, arg2, arg3, "", arg5, arg6);
    #
    def openDrw(self, drwNameInp):
        """
        Opens an SolidWorks drawing.
        
        Parameters
        ----------
        prtNameInp : str
        The file location of the drawing with drawing name appended at
        the end.
        E.g.: r"myDirectory\mySubDirectory\myDrawing"
        
        """
    
        import os
    
        self.prtNameInn = drwNameInp;
        self.prtNameInn = self.prtNameInn.replace('\\','/');
        #
        if os.path.basename(self.prtNameInn).split('.')[-1].lower() == 'slddrw': 
            pass;
        else:
            self.prtNameInn+'.SLDDRW'
        #
        openDoc     = swcom.OpenDoc6;
        arg1        = win32com.client.VARIANT(pythoncom.VT_BSTR, self.prtNameInn);
        arg2        = win32com.client.VARIANT(pythoncom.VT_I4, 3);
        arg3        = win32com.client.VARIANT(pythoncom.VT_I4, 1);
        arg5        = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 2);
        arg6        = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 128);
        #
        openDoc(arg1, arg2, arg3, "", arg5, arg6);
    #
    def update(self):
        """
        Update the currently open active file.
        
        """
    
        model   = swcom.ActiveDoc;
        value = model.EditRebuild3;
        
        return value;
    #
    def closeDoc(self, prtName):
        """
        Closes a SolidWorks file.
        
        Parameters
        ----------
        prtName : str
            Name of the file to be closed.
            
        """
    
        import os
        
        swcom.CloseDoc(os.path.basename(prtName));
    #
    def save(self, directory, fileName, fileExtension):
        """
        Save a SolidWorks file in different formats.
        
        Parameters
        ----------
        directory : str
            Name of the directory in which the file is to be saved.
            r"myDirectory\mySubDirectory"
            
        fileName : str
            Name of the file.
            r"myFile"
            
        fileExtension : str
            Extension/format of the file.
            r"STP"/r"SAT"/r"ACIS" etc.
            
            """
    
        model   = swcom.ActiveDoc;
        directory   = directory.replace('\\','/');
        comFileName = directory+'/'+fileName+'.'+fileExtension;
        arg         = win32com.client.VARIANT(pythoncom.VT_BSTR, comFileName);
        model.SaveAs3(arg, 0, 0);
    #
    def getGlobalVars(self):
        """
        Retrieve list of global variables in a file, if there are any.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        data: list
            A list of strings with the global variable/equation name
            
        units: list
            A list of strings with units of the corresponding global variable/
            equation
            
        eqnNum: list
            A list of strings with equation number of the corresponding global 
            variable/equation that SolidWorks has assigned it.
            
        """
    
        model   = swcom.ActiveDoc;
        
        eqMgr = model.GetEquationMgr;
        
        n = eqMgr.getCount;
        
        data    = {};
        units   = {};
        eqnNum  = {};
        
        utils = self.utils
        unitLinear, unitAngular  = utils._getDocUnits(model);
        
        for i in range(n):
            if eqMgr.GlobalVariable(i) == True:
                if eqMgr.Equation(i).split('"')[2].replace('= ','')[-3:] ==  unitLinear:
                    data[eqMgr.Equation(i).split('"')[1]] = eqMgr.Equation(i).split('"')[2].replace('= ','').replace(unitAngular.lower(), '')
                    units[eqMgr.Equation(i).split('"')[1]] = unitAngular.lower();
                    eqnNum[eqMgr.Equation(i).split('"')[1]] = i;
                else:
                    data[eqMgr.Equation(i).split('"')[1]] = eqMgr.Equation(i).split('"')[2].replace('= ','').replace(unitLinear.lower(), '')
                    units[eqMgr.Equation(i).split('"')[1]] = unitLinear.lower();
                    eqnNum[eqMgr.Equation(i).split('"')[1]] = i;
        
        if len(data.keys()) == 0:
            raise KeyError("There are not any 'Global Variables' present in the currently active Solidworks document.");
        else:
            return data, units, eqnNum;
    #
    def modifyGlobalVar(self, variable, modifiedVal, unit):
        """
        Modify one or many global variables in a file and update the file to 
        reflect the changes.
        Please note when modifying multiple global variables make sure the
        length of the list for the three parameters is equal to avoid 
        unncessary erros.
        
        Parameters
        ----------
        variable: str or a list of strings
            The name of the global variable/equation to be modified.
            
        modifiedVal: float or a list of floats
            New value of the global variable/equation
            
        unit: str or a list of strings
            Unit of the global variable
    
        """
    
        model   = swcom.ActiveDoc;
        #
        eqMgr   = model.GetEquationMgr;
        #
        data, units, eqnNum    = self.getGlobalVars();
        #
        if isinstance(variable, str) == True:
            eqMgr.Equation(eqnNum[variable], "\""+variable+"\" = "+str(modifiedVal)+unit+"");
        elif isinstance(variable, list) == True:
            if isinstance(modifiedVal, list) == True:
                if isinstance(unit, list) == True:
                    for i in range(len(variable)):
                        eqMgr.Equation(eqnNum[variable[i]], "\""+variable[i]+"\" = "+str(modifiedVal[i])+unit[i]+"");
                else:
                    raise TypeError("If a list of multiple variables is given, then lists of equal \n\
lengths should be given for 'modifiedVal' and 'unit' inputs.");
            else:
                raise TypeError("If a list of multiple variables is given, then lists of equal \n\
lengths should be given for 'modifiedVal' and 'unit' inputs.");
        else:
            raise TypeError("Incorrect input for the variables. Inputs can either be string, integer and string or lists containing variables, values and units.");
        #
        self.update();
    #
    def modifyLinkedVar(self, variable, modifiedVal, unit, *args):
        """
        Modify externally linked variables in a file and update the file to 
        reflect the changes.
        
        Parameters
        ----------
        variable: list of strings
            A list of names of the linked variables to be modified.
            There could be only one linked variable in which case the list will
            contain only one element.
    
        modifiedVal: list of floats
            A list of new values of the linked variables to be changed.
            There could be only one linked variable in which case the list will
            contain only one element.
    
        unit: list of strings
            A list of units of the linked variables to be changed.
            There could be only one linked variable in which case the list will
            contain only one element.
    
        """
    
        if len(args) == 0:
            file = 'equations.txt';
        else:
            file = args[0];
        #
        # READ FILE WITH ORIGINAL DIMENSIONS
        try:
            reader      = open(file, 'r');
        except IOError:
            raise IOError;
        finally:
            data = {};
            numLines    = len(reader.readlines());
            reader.close();
            reader      = open(file);
            lines       = reader.readlines();
            reader.close();
            for i in range(numLines):
                dim     = lines[i].split('"')[1];
                tempVal = lines[i].split(' ')[1];
                #
                val     = tempVal.replace(unit,'').replace('= ','').replace('\n','');
                data[dim] = val;
        #
        # MODIFY DIMENSIONS
        if isinstance(variable, list) == True:
            if isinstance(modifiedVal, list) == True:
                if isinstance(unit, list) == True:
                    for z in range(len(variable)):
                        data[variable[i]] = modifiedVal[i];
                else:
                    raise TypeError("If a list of multiple variables is given, then lists of equal \n\
lengths should be given for 'modifiedVal' and 'unit' inputs.");
            else:
                raise TypeError("If a list of multiple variables is given, then lists of equal \n\
lengths should be given for 'modifiedVal' and 'unit' inputs.");
        elif isinstance(variable, str) == True:
            data[variable] = modifiedVal;
        else:
            raise TypeError("The inputs types given are not same.");
        #
        # WRITE FILE WITH MODIFIED DIMENSIONS
        writer      = open(file, 'w');
        for key, value in data.items():
            writer.write('"'+key+'"= '+str(value)+unit+'\n');
        writer.close();
    
        value = self.update();
        
        return value;
    #
    def getAllDimensions(self):
        """
        Retrieve all dimensions in a part.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        df: dataframe
            Returns a dataframe with 'partName', 'featureName', 'dimensionName'
            'dimensionType', 'dimensionValue', ''dimensionUnit'.
    
        """
    
        model   = swcom.ActiveDoc;
    
        # swModelExtension = model.Extension
        aBodies = model.GetBodies2(win32com.client.VARIANT(pythoncom.VT_I4, -1), False)
    
        swFeat = model.FirstFeature
    
        utils = self.utils;
        unitLinear, unitAngular  = utils._getDocUnits(model);
    
        for i in range(16):
            swFeat = swFeat.GetNextFeature
        
        bodies = [];
    
        if aBodies is not None:
            for i in aBodies:
                bodies.append(i.Name);
        else:
            print('There are no bodies in the current part.');
    
        partName        = [];
        featureName     = [];
        dimensionName   = [];
        dimensionType   = [];
        dimensionValue  = [];
        dimensionUnit   = [];
    
        
        while swFeat is not None:
            swDispDim = swFeat.GetFirstDisplayDimension
        
            if swFeat.Name in bodies:
                while swDispDim is not None:
                    # swAnn   =   swDispDim.GetAnnotation
                    swDim   =   swDispDim.GetDimension
                
                    partName.append(swDim.FullName.split('@')[2]);
                    featureName.append(swFeat.Name);
                    dimensionName.append(swDim.FullName.split('@')[0]+'@'+swDim.FullName.split('@')[1]);
                    
                    dimensionType.append(utils._getDimType((swDispDim.Type2)));
                
                    if unitLinear == 'mm':
                        if utils._getDimType((swDispDim.Type2)) == 'Linear':
                            dimensionValue.append(float(swDim.GetSystemValue2(""))*1e3);
                            dimensionUnit.append(unitLinear);
                        elif utils._getDimType((swDispDim.Type2)) == 'Diameter' or utils._getDimType((swDispDim.Type2)) == 'Radial':
                            dimensionValue.append(float(swDim.GetSystemValue2(""))*1e3);
                            dimensionUnit.append(unitLinear);
                        elif utils._getDimType((swDispDim.Type2)) == 'Angular':
                            dimensionValue.append(float(swDim.GetSystemValue2("")));
                            dimensionUnit.append(unitAngular);
                    else:
                        if utils._getDimType((swDispDim.Type2)) == 'Linear':
                            dimensionValue.append(float(swDim.GetSystemValue2("")));
                            dimensionUnit.append(unitLinear);
                        elif utils._getDimType((swDispDim.Type2)) == 'Diameter' or utils._getDimType((swDispDim.Type2)) == 'Radial':
                            dimensionValue.append(float(swDim.GetSystemValue2("")));
                            dimensionUnit.append(unitLinear);
                        elif utils._getDimType((swDispDim.Type2)) == 'Angular':
                            dimensionValue.append(float(swDim.GetSystemValue2("")));
                            dimensionUnit.append(unitAngular);

                    swDispDim = swFeat.GetNextDisplayDimension(swDispDim)
                    
            else:
                pass;
            
            swFeat = swFeat.GetNextFeature
            
        import pandas as pd
    
        df = pd.DataFrame();
        
        df['partName'] = partName; df['featureName'] = featureName;
        df['dimensionName'] = dimensionName; df['dimensionType'] = dimensionType;
        #print(df);
        print(dimensionValue);
        print(df)
        df['dimensionValue'] = dimensionValue;
        df['dimensionUnit'] = dimensionUnit;
            
        return df
    #    
    def modifyPrtDimension(self, dimName, sketchName, prtName, newDimValue):
        """
        Modify a dimension in a part.
        
        Parameters
        ----------
        dimName: str
            A string of name of a dimension in a part.
    
        sketchName: str
            A string of name of a sketch/feature in a part.
        
        prtName: str
            A string of name of the part.
    
        newDimValue: float
            New value of the dimension.
    
        """
        
        model   = swcom.ActiveDoc;
    
        arg1 = dimName + "@" +sketchName+ "@" +prtName+ ".SLDPRT";
        arg8 = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None);
        model.Extension.SelectByID2(arg1, "DIMENSION", 0, 0, 0, False, 0, arg8, 0);
        # model.Extension.SelectByID2(arg1, "", 0, 0, 0, False, 0, arg8, 0);
        
        dimension = model.Parameter(arg1.replace("@" +prtName+ ".SLDPRT", ""));
        dimension.SystemValue = newDimValue;
    
        model.EditRebuild3;
    
        del arg1, arg8, model, dimension;

    class drawing:
        def __init__(self):
            pass;
        
        def getDimensions(self):
            """
            Retrieve dimension from all views in a drawing.
            
            Parameters
            ----------
            None
            
            Returns
            -------
            df: dataframe
                Returns a dataframe with 'DimensionName', 'FeatureName', 
                'ModelName', 'DimensionValue', 'DimensionUnit', 'DimensionType'
                'ToleranceType', 'MaxTolerance', 'MinTolerance'.
            
            """
            
            swModel     = swcom.ActiveDoc;
            
            # ModelDocExtension = swModel.Extension;
            
            linearunit, angularunit = self._getDocUnits(swModel)
            
            swView      = swModel.GetFirstView;
            swView      = swView.GetNextView;

            data        = pd.DataFrame();
            dimName     = [];

            featureName = [];
            modelName   = [];
            dimValue    = [];
            dimType     = [];
            tolType     = [];
            maxTol      = [];
            minTol      = [];
            unit        = [];

            while isinstance(swView, win32com.client.CDispatch) == True:
                swDispDim   = swView.GetFirstDisplayDimension5;
                dimCount    = swView.GetDimensionCount4;
                
                #print(str(swView.GetDatumTargetSymCount)+'  '+str(swView.GetDisplayDimensionCount));
                #print(isinstance(swDispDim, win32com.client.CDispatch));
                
                for i in range(dimCount):
                                      
                    dimType.append(self._getDimType(swDispDim.Type2));
                                       
                    if self._getDimType(swDispDim.Type2) == 'Chamfer':
                        argAngle    = win32com.client.VARIANT(pythoncom.VT_I4, 0);
                        swDimAngle  = swDispDim.GetDimension2(argAngle);
                        argLength   = win32com.client.VARIANT(pythoncom.VT_I4, 1);
                        swDimLength = swDispDim.GetDimension2(argLength);
                        
                        dimName.append(swDimAngle.Name);
                        
                    else:
                        swDim = swDispDim.GetDimension;
                        dimName.append(swDim.Name);
                    
                    featureName.append(swDim.FullName.split('@')[1]);
                    modelName.append(swDim.FullName.split('@')[2]);

                    if self._getDimType(swDispDim.Type2) == 'Chamfer':
                        
                        dimValue.append(str(round(float(swDimLength.GetSystemValue2(""))*1e3,4))+' x '+str(round((((float(swDimAngle.GetSystemValue2("")))*(180))/math.pi)-90,4)));
                        unit.append(linearunit+'x'+angularunit);
                        tolType.append(self._getTolType(swDimAngle.GetToleranceType).replace('swTol','')+ ' x ' +self._getTolType(swDimLength.GetToleranceType).replace('swTol',''));
                        
                        if self._getTolType(swDimLength.GetToleranceType) == 'swTolSYMMETRIC':
                            
                            if self._getTolType(swDimAngle.GetToleranceType) == 'swTolSYMMETRIC':
                                maxTol.append(str(swDimAngle.Tolerance.GetMaxValue*1e3)+ ' x ' +str(round((((float(swDimLength.Tolerance.GetMaxValue))*(180))/math.pi)-0,4)));
                                minTol.append(str(-1*swDimAngle.Tolerance.GetMaxValue*1e3)+ ' x ' +str(-1*round((((float(swDimLength.Tolerance.GetMaxValue))*(180))/math.pi)-0,4)));
                            elif self._getTolType(swDimAngle.GetToleranceType) == 'swTolBILAT':
                                maxTol.append(str(swDimAngle.Tolerance.GetMaxValue*1e3)+ ' x ' +str(round((((float(swDimLength.Tolerance.GetMaxValue))*(180))/math.pi)-0,4)));
                                minTol.append(str(-1*swDimAngle.Tolerance.GetMaxValue*1e3)+ ' x ' +str(round((((float(swDimLength.Tolerance.GetMinValue))*(180))/math.pi)-0,4)));
                                
                        elif self._getTolType(swDim.GetToleranceType) == 'swTolBILAT':
                            
                            if self._getTolType(swDimAngle.GetToleranceType) == 'swTolSYMMETRIC':
                                maxTol.append(str(swDimAngle.Tolerance.GetMaxValue*1e3)+ ' x ' +str(round((((float(swDimLength.Tolerance.GetMaxValue))*(180))/math.pi)-0,4)));
                                minTol.append(str(swDimAngle.Tolerance.GetMinValue*1e3)+ ' x ' +str(-1*round((((float(swDimLength.Tolerance.GetMaxValue))*(180))/math.pi)-0,4)));
                            elif self._getTolType(swDimAngle.GetToleranceType) == 'swTolBILAT':
                                maxTol.append(str(swDimAngle.Tolerance.GetMaxValue*1e3)+ ' x ' +str(round((((float(swDimLength.Tolerance.GetMaxValue))*(180))/math.pi)-0,4)));
                                minTol.append(str(swDimAngle.Tolerance.GetMinValue*1e3)+ ' x ' +str(round((((float(swDimLength.Tolerance.GetMinValue))*(180))/math.pi)-0,4)));
                                
                        else:
                            maxTol.append(0);
                            minTol.append(0);
                        
                    elif self._getDimType(swDispDim.Type2) == 'Angular':
                        
                        dimValue.append(round((((float(swDim.GetSystemValue2("")))*(180))/math.pi),4));
                        unit.append(angularunit);
                        tolType.append(self._getTolType(swDim.GetToleranceType).replace('swTol',''));
                        
                        if self._getTolType(swDim.GetToleranceType) == 'swTolSYMMETRIC':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(-1*swDim.Tolerance.GetMaxValue*1e3);
                        elif self._getTolType(swDim.GetToleranceType) == 'swTolBILAT':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(swDim.Tolerance.GetMinValue*1e3);
                        elif self._getTolType(swDim.GetToleranceType) == 'swTolLIMIT':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(swDim.Tolerance.GetMinValue*1e3);
                        else:
                            maxTol.append(0);
                            minTol.append(0);
                        
                    elif swDim.GetType == 0:
                        
                        dimValue.append(round(float(swDim.GetSystemValue2(""))*1e3,4));
                        unit.append(linearunit);
                        tolType.append(self._getTolType(swDim.GetToleranceType).replace('swTol',''));
                        
                        if self._getTolType(swDim.GetToleranceType) == 'swTolSYMMETRIC':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(-1*swDim.Tolerance.GetMaxValue*1e3);
                        elif self._getTolType(swDim.GetToleranceType) == 'swTolBILAT':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(swDim.Tolerance.GetMinValue*1e3);
                        elif self._getTolType(swDim.GetToleranceType) == 'swTolLIMIT':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(swDim.Tolerance.GetMinValue*1e3);
                        else:
                            maxTol.append(0);
                            minTol.append(0);
                        
                    elif swDim.GetType == 2:
                        
                        dimValue.append(round(float(swDim.GetSystemValue2(""))*1e3,4));
                        unit.append(linearunit);
                        tolType.append(self._getTolType(swDim.GetToleranceType).replace('swTol',''));
                        
                        if self._getTolType(swDim.GetToleranceType) == 'swTolSYMMETRIC':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(-1*swDim.Tolerance.GetMaxValue*1e3);
                        elif self._getTolType(swDim.GetToleranceType) == 'swTolBILAT':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(swDim.Tolerance.GetMinValue*1e3);
                        elif self._getTolType(swDim.GetToleranceType) == 'swTolLIMIT':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(swDim.Tolerance.GetMinValue*1e3);
                        else:
                            maxTol.append(0);
                            minTol.append(0);
                        
                    elif swDim.GetType == -1:
                        
                        dimValue.append(round(float(swDim.GetSystemValue2(""))*1e3,4));
                        unit.append(linearunit);
                        tolType.append(self._getTolType(swDim.GetToleranceType).replace('swTol',''));
                        
                        if self._getTolType(swDim.GetToleranceType) == 'swTolSYMMETRIC':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(-1*swDim.Tolerance.GetMaxValue*1e3);
                        elif self._getTolType(swDim.GetToleranceType) == 'swTolBILAT':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(swDim.Tolerance.GetMinValue*1e3);
                        elif self._getTolType(swDim.GetToleranceType) == 'swTolLIMIT':
                            maxTol.append(swDim.Tolerance.GetMaxValue*1e3);
                            minTol.append(swDim.Tolerance.GetMinValue*1e3);
                        else:
                            maxTol.append(0);
                            minTol.append(0);
                        
                    else:
                        pass;
                    #
                    swDispDim = swDispDim.GetNext3;

                swView = swView.GetNextView;
            
            data['DimensionName']   = np.asarray(dimName, dtype='<U64');
            data['FeatureName']     = np.asarray(featureName, dtype='<U64');
            data['ModelName']       = np.asarray(modelName, dtype='<U64');
            data['DimensionValue']  = np.asarray(dimValue, dtype='<U64');
            data['DimensionUnit']   = np.asarray(unit, dtype='<U64');
            data['DimensionType']   = np.asarray(dimType, dtype='<U64');
            data['ToleranceType']   = np.asarray(tolType, dtype='<U64');
            data['MaxTolerance']    = np.asarray(maxTol, dtype='<U64');
            data['MinTolerance']    = np.asarray(minTol, dtype='<U64');

            return data;
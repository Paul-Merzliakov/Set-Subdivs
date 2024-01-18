from maya import cmds
class SS_Window(object):
    
    
     def __init__(self):
        
                
        self.window = "SS_Window"
        self.title = "Set Subdivs"
        self.size = (300, 100)
        self.buildUI()
    
     def buildUI(self, *args):
         
        if cmds.window(self.window, exists = True):# close old window if open
            cmds.deleteUI(self.window, window=True)
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size) #create and formatting  new window
        cmds.columnLayout( adjustableColumn=True)
        cmds.separator( height = 20) 
        cmds.text("Select the object you want to reference" )
        cmds.separator( height = 10, style = 'none')
        self.objTxtField = cmds.textField()
        self.selectObjBtn = cmds.button( label = "Add Reference Object", command = self.select_obj )
        cmds.separator( height = 10)
        cmds.text("Select the number of subdivs for object")
        cmds.separator( height = 10, style = 'none')
        self.subdivs = cmds.intSliderGrp( field=True, label = 'Subdivs', minValue = 1, maxValue = 7, value = 1)
        cmds.separator( height = 10, style = 'none')
        self.setSubdivsBtn = cmds.button( label = "Set Subdivs", command=self.set_subdivs )
        cmds.showWindow()
        
 #adds selected obj to text field

     def select_obj(self, *args):

        ogObject = cmds.ls( selection = True )
        if not ogObject:

            raise RuntimeError("you have no object selected")
            
        cmds.textField(self.objTxtField, edit = True, text = ogObject[0] )
        

 #function to get object aproximate size by finding bounding box measurements.
        
     def get_measurements(self,obj):
                       
        x1, y1, z1, x2, y2, z2 = cmds.exactWorldBoundingBox(obj)
        x = abs( x2 -  x1 )
        y = abs( y2 -  y1 )
        z = abs( z2 -  z1 )
        size = x + y + z
        return size
    
 #final function that queries ui inputs and uses get measurements  to calculate and set subdivs. 
        
     def set_subdivs(self, *args):
        
        selectedObj = cmds.textField(self.objTxtField, query = True, text = True)
        if not selectedObj:
            
            raise RuntimeError("Select reference object before setting subdiv")
            
        objectsList = cmds.ls( geometry = True, type = 'mesh')
        subdiv_amnt =  cmds.intSliderGrp(self.subdivs, value = True, query = True) 
        quotient = subdiv_amnt /self.get_measurements(selectedObj)

        for obj in objectsList:
            
            iterations = round(self.get_measurements(obj) * quotient, 0)
            cmds.setAttr( '{0}.aiSubdivType'.format(obj),1)
            cmds.setAttr( '{0}.aiDispZeroValue'.format(obj), 0.5)
            cmds.setAttr( '{0}.aiSubdivIterations'.format(obj), iterations )
        print("Your subdivs have been set!")
        
    
my_window = SS_Window()
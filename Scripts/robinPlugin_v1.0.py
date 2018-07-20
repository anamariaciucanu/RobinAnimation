import maya.cmds as cmds
import math
import random  

#To fix: When pressing on Hop and other buttons twice,
# the Robin movement starts at different points
#To do: Add clear buttons on each tab to remove effect

#Setup 
rowSpacingNumber = 10

#Global parameters------------------------------------------------
widgets = {}
mirrorShakeHead = True
mirrorNodHead = True
mirrorWagTail = True
mirrorLiftTail = True
mirrorBendTorso = True

pi = math.pi
animationStart = 1
animationEnd = 120

hopFrames = 5
hopAmplitude = 5
hopSpeed = 1

flapWingsFrames = 5
flapWingsAmplitude = 5
flapWingsSpeed = 1

wagTailFrames = 5
wagTailAmplitude = 5
wagTailSpeed = 1

nodHeadFrames = 5
nodHeadAmplitude = 5
nodHeadSpeed = 1

shakeHeadFrames = 5
shakeHeadAmplitude = 5
shakeHeadSpeed = 1

liftTailFrames = 5
liftTailAmplitude = 5
liftTailSpeed = 1

torsoBendFrames = 5
torsoBendAmplitude = 5
torsoBendSpeed = 1

shakeHeadFrames = 5
shakeHeadAmplitude = 5
shakeHeadSpeed = 1


#Interface ----------------------------------------------------------------------------------
def createUI():    
    #If window exists, delete window
    if cmds.window('robinWindow', exists = True):
        cmds.deleteUI('robinWindow')
        
    #Create window 
    widgets['window'] = cmds.window('robinWindow', t='Robin Animator', w = 300, sizeable = False, mxb = False, mnb = False)
    windowLayout = cmds.columnLayout(adj = True, rowSpacing = rowSpacingNumber)
 
    #Create image logo
    logoPath = cmds.internalVar(upd = True) + 'icons/robinAnimator.png'
    logoImage = cmds.image(image = logoPath)

    #Create reset button for robin
    cmds.button( label='Reset Robin', c = 'resetRobin()', h = 50)
    
    #Ask user how many animation frames he wants
    cmds.text('What is the start frame?');
    widgets['startFrame'] = cmds.intFieldGrp( numberOfFields=1, label='Animation Start Frame')
    cmds.text('What is the end frame?')
    widgets['endFrame'] = cmds.intFieldGrp( numberOfFields=1, label='Animation End Frame')
        
    #Create tabs 
    widgets['tabLayout'] = cmds.tabLayout(imw = 5, imh = 5)
    
    #Feet tab --------------------------------------------------------------------------------
    widgets['feetTab'] = cmds.columnLayout('Feet', parent = widgets['tabLayout'], rowSpacing = rowSpacingNumber, co = ('left', 20))    
    cmds.separator()
    cmds.text('How many frames per hop?');
    widgets['hopFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Hop Frames')
    cmds.text('How high should the robin hop?');
    widgets['hopAmplitude'] = cmds.intFieldGrp( numberOfFields=1, label='Hop Amplitude')
    cmds.text('How fast should the robin hop?');
    widgets['hopSpeed'] = cmds.intFieldGrp( numberOfFields=1, label='Hop Speed')   
    
    cmds.rowLayout( numberOfColumns = 2 )     
    cmds.button( label='Hop', c = 'createRobinHopInADirectionAnimation()', w = 100, align = 'left')
    cmds.button( label='Clear Hop', c = 'clearRobinHopInADirectionAnimation()', w = 100, align = 'right')

        
    #Torso tab --------------------------------------------------------------------------------
    widgets['torsoTab'] = cmds.columnLayout('Torso', parent = widgets['tabLayout'], rowSpacing = rowSpacingNumber, co = ('left', 20))
    cmds.separator()
    cmds.text('How many frames per bending motion?');
    widgets['torsoBendFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Torso Bending Frames')
    cmds.text('How much should the torso bend?');
    widgets['torsoBendAmplitude'] = cmds.intFieldGrp( numberOfFields=1, label='Torso Bending Amplitude')
    cmds.text('How fast should the torso bend?');
    widgets['bendTorsoSpeed'] = cmds.intFieldGrp( numberOfFields=1, label='Bend Torso Speed')  
    
    cmds.rowLayout( numberOfColumns = 2 ) 
    cmds.button( label='Bend Torso', c = 'createBendTorsoAnimation()', w = 100, align = 'left')
    cmds.button( label='Clear Bend Torso', c = 'clearBendTorsoAnimation()', w = 100, align = 'right')
    
    
    #Wings tab----------------------------------------------------------------------------------
    widgets['wingsTab'] = cmds.columnLayout('Wings', parent = widgets['tabLayout'], rowSpacing = rowSpacingNumber, co = ('left', 20))
    cmds.separator()
    cmds.text('How many frames per wing flap?');
    widgets['flapWingsFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Flap Wings Frames')
    cmds.text('How high should the wings go?');
    widgets['flapWingsAmplitude'] = cmds.intFieldGrp( numberOfFields=1, label='Flap Wings Amplitude')
    cmds.text('How fast should the wings flap?');
    widgets['flapWingsSpeed'] = cmds.intFieldGrp( numberOfFields=1, label='Flap Wings Speed')  
   
    cmds.rowLayout( numberOfColumns = 2 ) 
    cmds.button( label='Flap Wings', c = 'createFlapWingsAnimation()', w = 100, align = 'left')
    cmds.button( label='Clear Flap Wings', c = 'clearFlapWingsAnimation()', w = 100, align = 'right') 
       
    #Head tab----------------------------------------------------------------------------------
    widgets['headTab'] = cmds.columnLayout('Head', w = 400, parent = widgets['tabLayout'], rowSpacing = rowSpacingNumber, co = ('left', 20))
    cmds.separator()
    cmds.text('How many frames per head nod?');
    widgets['nodHeadFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Nod Head Frames')
    cmds.text('How much should the head turn?');
    widgets['nodHeadAmplitude'] = cmds.intFieldGrp( numberOfFields=1, label='Nod Head Amplitude')
    cmds.text('How fast should the head nod?');
    widgets['nodHeadSpeed'] = cmds.intFieldGrp( numberOfFields=1, label='Nod Head Speed')  
    
    child1 = cmds.rowColumnLayout(numberOfColumns = 2)
    cmds.button( label = 'Nod Head', c = 'createNodHeadAnimation()', w = 100, align = 'left')
    cmds.button( label = 'Clear Nod Head', c = 'clearNodHeadAnimation()', w = 100, align = 'right')
    cmds.setParent( '..' )
    cmds.separator()
    
    cmds.text('How many frames per head shake?');
    widgets['shakeHeadFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Shake Head Frames')
    cmds.text('How much should the head turn?');
    widgets['shakeHeadAmplitude'] = cmds.intFieldGrp( numberOfFields=1, label='Shake Head Amplitude')
    cmds.text('How fast should the head shake?');
    widgets['shakeHeadSpeed'] = cmds.intFieldGrp( numberOfFields=1, label='Shake Head Speed')
    
    child2 = cmds.rowColumnLayout(numberOfColumns = 2)
    cmds.button( label = 'Shake Head', c = 'createShakeHeadAnimation()', w = 100, align = 'left')
    cmds.button( label = 'Clear Shake Head', c = 'clearShakeHeadAnimation()', w = 100, align = 'right')
    cmds.setParent( '..' )
    cmds.separator()  
        
    #Tail tab-----------------------------------------------------------------------------------
    widgets['tailTab'] = cmds.columnLayout('Tail', w = 400, parent = widgets['tabLayout'], rowSpacing = rowSpacingNumber, co = ('left', 20))   
    cmds.separator()
    cmds.text('How many frames per tail wag?');
    widgets['wagTailFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Wag Tail Frames')
    cmds.text('How high should the tail go?');
    widgets['wagTailAmplitude'] = cmds.intFieldGrp( numberOfFields=1, label='Wag Tail Amplitude')
    cmds.text('How fast should the tail wag?');
    widgets['wagTailSpeed'] = cmds.intFieldGrp( numberOfFields=1, label='Wag Tail Speed')      
    
    child1 = cmds.rowColumnLayout(numberOfColumns = 2)
    cmds.button( label = 'Wag Tail', c = 'createWagTailAnimation()', w = 100, align = 'left')
    cmds.button( label = 'Clear Wag Tail', c = 'clearWagTailAnimation()', w = 100, align = 'right')
    cmds.setParent( '..' )
    cmds.separator()    
    
    cmds.text('How many frames per tail lift?');
    widgets['liftTailFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Lift Tail Frames')
    cmds.text('How high should the tail go?');
    widgets['liftTailAmplitude'] = cmds.intFieldGrp( numberOfFields=1, label='Lift Tail Amplitude')
    cmds.text('How fast should the tail lift?');
    widgets['liftTailSpeed'] = cmds.intFieldGrp( numberOfFields=1, label='Lift Tail Speed')   
    
    child2 = cmds.rowColumnLayout(numberOfColumns = 2)
    cmds.button( label = 'Lift Tail', c = 'createLiftTailAnimation()', w = 100, align = 'left')
    cmds.button( label = 'Clear Lift Tail', c = 'clearLiftTailAnimation()', w = 100, align = 'right')    
    cmds.setParent( '..' )
    cmds.separator()  
    
    #Show button   
    cmds.showWindow(widgets['window'])
    
  
#Get variables ------------------------------------------------------------------------------------    
#Get animation start position
def getAnimationStart():
    localAnimationStart = cmds.intFieldGrp(widgets['startFrame'], q = True, v = True)
    if localAnimationStart > 0:
        global animationStart
        animationStart = localAnimationStart[0]
        
#Get animation end position    
def getAnimationEnd():
    localAnimationEnd = cmds.intFieldGrp(widgets['endFrame'], q = True, v = True)
    if localAnimationEnd > 0:
        global animationEnd
        animationEnd = localAnimationEnd[0] + 1

#Hop methods    
def getHopFrames():
    localHopFrames = cmds.intFieldGrp(widgets['hopFrames'], q = True, v = True)
    if localHopFrames > 0:
        global hopFrames
        hopFrames = localHopFrames[0]
        
def getHopAmplitude():
    localHopAmplitude = cmds.intFieldGrp(widgets['hopAmplitude'], q = True, v = True)
    if localHopAmplitude > 0:
        global hopAmplitude
        hopAmplitude = localHopAmplitude[0]
                 
def getHopSpeed():
    localHopSpeed = cmds.intFieldGrp(widgets['hopSpeed'], q = True, v = True)
    if localHopSpeed > 0:
        global hopSpeed
        hopSpeed = localHopSpeed[0]

#Torso bend methods
def getTorsoBendFrames():
    localTorsoBendFrames = cmds.intFieldGrp(widgets['torsoBendFrames'], q = True, v = True)
    if localTorsoBendFrames > 0:
        global torsoBendFrames
        torsoBendFrames = localTorsoBendFrames[0]
        
def getTorsoBendAmplitude():
    localTorsoBendAmplitude = cmds.intFieldGrp(widgets['torsoBendAmplitude'], q = True, v = True)
    if localTorsoBendAmplitude > 0:
        global torsoBendAmplitude
        torsoBendAmplitude = localTorsoBendAmplitude[0]
                 
def getBendTorsoSpeed():
    localBendTorsoSpeed = cmds.intFieldGrp(widgets['bendTorsoSpeed'], q = True, v = True)
    if localBendTorsoSpeed > 0:
        global bendTorsoSpeed
        bendTorsoSpeed = localBendTorsoSpeed[0]
                
#Flap wings methods    
def getFlapWingsFrames():
    localFlapWingsFrames = cmds.intFieldGrp(widgets['flapWingsFrames'], q = True, v = True)
    if localFlapWingsFrames > 0:
        global flapWingsFrames
        flapWingsFrames = localFlapWingsFrames[0]
        
def getFlapWingsAmplitude():
    localFlapWingsAmplitude = cmds.intFieldGrp(widgets['flapWingsAmplitude'], q = True, v = True)
    if localFlapWingsAmplitude > 0:
        global flapWingsAmplitude
        flapWingsAmplitude = localFlapWingsAmplitude[0]
                 
def getFlapWingsSpeed():
    localFlapWingsSpeed = cmds.intFieldGrp(widgets['flapWingsSpeed'], q = True, v = True)
    if localFlapWingsSpeed > 0:
        global flapWingsSpeed
        flapWingsSpeed = localFlapWingsSpeed[0]
        
#Nod head methods    
def getNodHeadFrames():
    localNodHeadFrames = cmds.intFieldGrp(widgets['nodHeadFrames'], q = True, v = True)
    if localNodHeadFrames> 0:
        global nodHeadFrames
        nodHeadFrames = localNodHeadFrames[0]
        
def getNodHeadAmplitude():
    localNodHeadAmplitude = cmds.intFieldGrp(widgets['nodHeadAmplitude'], q = True, v = True)
    if localNodHeadAmplitude > 0:
        global nodHeadAmplitude
        nodHeadAmplitude = localNodHeadAmplitude[0]
                 
def getNodHeadSpeed():
    localNodHeadSpeed = cmds.intFieldGrp(widgets['nodHeadSpeed'], q = True, v = True)
    if localNodHeadSpeed > 0:
        global nodHeadSpeed
        nodHeadSpeed = localNodHeadSpeed[0]

#Shake head methods
def getShakeHeadFrames():
    localShakeHeadFrames = cmds.intFieldGrp(widgets['shakeHeadFrames'], q = True, v = True)
    if localShakeHeadFrames> 0:
        global shakeHeadFrames
        shakeHeadFrames = localShakeHeadFrames[0]
        
def getShakeHeadAmplitude():
    localShakeHeadAmplitude = cmds.intFieldGrp(widgets['shakeHeadAmplitude'], q = True, v = True)
    if localShakeHeadAmplitude > 0:
        global shakeHeadAmplitude
        shakeHeadAmplitude = localShakeHeadAmplitude[0]
                 
def getShakeHeadSpeed():
    localShakeHeadSpeed = cmds.intFieldGrp(widgets['shakeHeadSpeed'], q = True, v = True)
    if localShakeHeadSpeed > 0:
        global shakeHeadSpeed
        shakeHeadSpeed = localShakeHeadSpeed[0]
                
#Wag tail methods    
def getWagTailFrames():
    localWagTailFrames = cmds.intFieldGrp(widgets['wagTailFrames'], q = True, v = True)
    if localWagTailFrames> 0:
        global wagTailFrames
        wagTailFrames = localWagTailFrames[0]
        
def getWagTailAmplitude():
    localWagTailAmplitude = cmds.intFieldGrp(widgets['wagTailAmplitude'], q = True, v = True)
    if localWagTailAmplitude > 0:
        global wagTailAmplitude
        wagTailAmplitude = localWagTailAmplitude[0]
                 
def getWagTailSpeed():
    localWagTailSpeed = cmds.intFieldGrp(widgets['wagTailSpeed'], q = True, v = True)
    if localWagTailSpeed > 0:
        global wagTailSpeed
        wagTailSpeed = localWagTailSpeed[0]

#Lift tail methods
def getLiftTailFrames():
    localLiftTailFrames = cmds.intFieldGrp(widgets['liftTailFrames'], q = True, v = True)
    if localLiftTailFrames> 0:
        global liftTailFrames
        liftTailFrames = localLiftTailFrames[0]
        
def getLiftTailAmplitude():
    localLiftTailAmplitude = cmds.intFieldGrp(widgets['liftTailAmplitude'], q = True, v = True)
    if localLiftTailAmplitude > 0:
        global liftTailAmplitude
        liftTailAmplitude = localLiftTailAmplitude[0]
                 
def getLiftTailSpeed():
    localLiftTailSpeed = cmds.intFieldGrp(widgets['liftTailSpeed'], q = True, v = True)
    if localLiftTailSpeed > 0:
        global liftTailSpeed
        liftTailSpeed = localLiftTailSpeed[0]
 
#Animations ---------------------------------------------------------------------------------                                  
                            
#Hopping animation            
def createRobinHopInADirectionAnimation():
    #Select robin controler
    robinCtrl = cmds.select( 'RobinCTRL', r=True )
        
    #Get parameters 
    getAnimationStart()   
    getAnimationEnd()
    getHopFrames()
    getHopAmplitude()   
    getHopSpeed() 
        
    #Animate the hop    
    for i in range(animationStart, animationEnd, hopFrames):
        for j in range(0, hopFrames, 1):
            if (i+j < animationEnd):
                teta = j*pi/hopFrames
                newY = hopAmplitude * math.fabs(math.sin(teta)) 
                newX = hopSpeed * math.fabs(math.cos(teta)) 
                newZ = 0              
          
                oldX = cmds.getAttr('RobinCTRL.translateX') 
                oldY = cmds.getAttr('RobinCTRL.translateY') 
                oldZ = cmds.getAttr('RobinCTRL.translateZ') 
                
                currentX = oldX - newX 
                currentY = newY
                currentZ = oldZ - newZ 
                cmds.setAttr('RobinCTRL.translateX', currentX)
                cmds.setKeyframe( 'RobinCTRL', attribute='translateX', t=i+j )
                cmds.setAttr('RobinCTRL.translateY', currentY)
                cmds.setKeyframe( 'RobinCTRL', attribute='translateY', t=i+j )
                cmds.setAttr('RobinCTRL.translateZ', currentZ)
                cmds.setKeyframe( 'RobinCTRL', attribute='translateZ', t=i+j )   
            else:
                break 
  

#Torso bending animation
def createBendTorsoAnimation(): 
    #Select robin controller 
    robinCtrl = cmds.select( 'RobinCTRL', r=True )
       
    #Get parameters
    getAnimationStart()
    getAnimationEnd()
    getTorsoBendFrames()
    getTorsoBendAmplitude()  
    getBendTorsoSpeed() 
    flip = 1
    
    #Animate the bend    
    for i in range(animationStart, animationEnd, torsoBendFrames):
        if mirrorBendTorso:
            flip = -flip   
            
        for j in range(0, torsoBendFrames, 1):
            if (i+j < animationEnd):
                teta = j*pi/torsoBendFrames
                torsoRotation = flip * torsoBendAmplitude * math.sin(bendTorsoSpeed * teta) 
        
                if torsoRotation < -30:
                    torsoRotation = -30
                if torsoRotation > 60:
                    torsoRotation = 60
                    
                feetReverseRotation = -torsoRotation
            
                cmds.setAttr('RobinCTRL.BendTorso', torsoRotation)
                cmds.setKeyframe( 'RobinCTRL', attribute='BendTorso', t=i+j )
                cmds.setAttr('RobinCTRL.SwingLegs', feetReverseRotation)
                cmds.setKeyframe('RobinCTRL', attribute='SwingLegs', t=i+j )
            else:
                break
    

#Wing flapping animation
def createFlapWingsAnimation():
    robinCtrl = cmds.select( 'RobinCTRL', r=True )
    getAnimationStart()
    getAnimationEnd()
    getFlapWingsFrames()
    getFlapWingsAmplitude()   
    getFlapWingsSpeed()
    flip=1
    
    for i in range(animationStart, animationEnd, flapWingsFrames):
        for j in range(0, flapWingsFrames, 1):
            if (i+j < animationEnd):
                teta = j*pi/flapWingsFrames
                rightWingRotation = flip * flapWingsAmplitude * math.sin(flapWingsSpeed * teta) 
                leftWingRotation = -flip * flapWingsAmplitude * math.sin(flapWingsSpeed * teta)
            
                cmds.setAttr('RobinCTRL.LiftRightWing', rightWingRotation)
                cmds.setKeyframe( 'RobinCTRL', attribute='LiftRightWing', t=i+j )
                cmds.setAttr('RobinCTRL.LiftLeftWing', leftWingRotation)
                cmds.setKeyframe('RobinCTRL', attribute='LiftLeftWing', t=i+j )
            else:
                break

#Tail wagging animation    
def createWagTailAnimation():
    robinCtrl = cmds.select('RobinCTRL', r=True)
    getAnimationStart()
    getAnimationEnd()
    getWagTailFrames()
    getWagTailAmplitude() 
    getWagTailSpeed()      
    flip = 1
            
    for i in range(animationStart, animationEnd, wagTailFrames):
        if mirrorWagTail:
            flip = -flip    
        
        for j in range(0, wagTailFrames, 1):
            if (i+j < animationEnd):
                teta = j*pi/wagTailFrames            
                tailRotation = flip * wagTailAmplitude * math.sin(wagTailSpeed * teta) 
                        
                if tailRotation > 60.0:
                    tailRotation = 60.0
                cmds.setAttr('RobinCTRL.WagTail', tailRotation)
                cmds.setKeyframe('RobinCTRL', attribute='WagTail', t=i+j )
            else:
                break
                           
#Tail lifting animation
def createLiftTailAnimation():
    robinCtrl = cmds.select('RobinCTRL', r=True)
    getAnimationStart()
    getAnimationEnd()
    getLiftTailFrames()
    getLiftTailAmplitude()   
    getLiftTailSpeed()    
    flip = 1
            
    for i in range(animationStart, animationEnd, liftTailFrames):
        if mirrorLiftTail:
            flip = -flip    
        
        for j in range(0, liftTailFrames, 1):
            if (i+j < animationEnd):
                teta = j*pi/liftTailFrames            
                tailRotation = flip * liftTailAmplitude * math.sin(liftTailSpeed * teta) 
                        
                if tailRotation > 60.0:
                    tailRotation = 60.0
                cmds.setAttr('RobinCTRL.LiftTail', tailRotation)
                cmds.setKeyframe('RobinCTRL', attribute='LiftTail', t=i+j )
            else:
                break            
 
#Head shaking animaion                        
def createShakeHeadAnimation():
    robinCtrl = cmds.select('RobinCTRL', r=True)
    getAnimationStart()
    getAnimationEnd()
    getShakeHeadFrames()
    getShakeHeadAmplitude() 
    getShakeHeadSpeed()      
    flip = 1
            
    for i in range(animationStart, animationEnd, shakeHeadFrames):
        if mirrorShakeHead:
            flip = -flip    
        
        for j in range(0, shakeHeadFrames, 1):
            if (i+j < animationEnd):
                teta = j*pi/shakeHeadFrames            
                headRotation = flip * shakeHeadAmplitude * math.sin(shakeHeadSpeed * teta) 
                        
                if headRotation > 90.0:
                    headRotation = 90.0
                cmds.setAttr('RobinCTRL.ShakeHead', headRotation)
                cmds.setKeyframe('RobinCTRL', attribute='ShakeHead', t=i+j )
            else:
                break
                
#Head nodding animation
def createNodHeadAnimation():
    robinCtrl = cmds.select('RobinCTRL', r=True)
    getAnimationStart()
    getAnimationEnd()
    getNodHeadFrames()
    getNodHeadAmplitude()  
    getNodHeadSpeed()     
    flip = 1
            
    for i in range(animationStart, animationEnd, nodHeadFrames):
        if mirrorNodHead:
            flip = -flip    
        
        for j in range(0, nodHeadFrames, 1):
            if (i+j < animationEnd):
                teta = j*pi/nodHeadFrames            
                headRotation = flip * nodHeadAmplitude * math.sin(nodHeadSpeed * teta) 
                        
                if headRotation > 90.0:
                    headRotation = 90.0
                cmds.setAttr('RobinCTRL.NodHead', headRotation)
                cmds.setKeyframe('RobinCTRL', attribute='NodHead', t=i+j )  
            else:
                break
           
  
#Reset Robin animation --------------------------------------------------------------------

#Get max frames
def getMaxFrame():
    maxFrame = cmds.playbackOptions( max = True, query = True ) + 1
    return maxFrame 

#Clearing
def clearRobinHopInADirectionAnimation():
    maxFrame = getMaxFrame()
    resetRobinTranslation(maxFrame)
 
def clearBendTorsoAnimation():
    maxFrame = getMaxFrame()
    resetBendTorso(maxFrame)
    resetSwingLegs(maxFrame)

def clearFlapWingsAnimation():
    maxFrame = getMaxFrame()
    resetLiftWings(maxFrame)  

def clearNodHeadAnimation():
    maxFrame = getMaxFrame()
    resetNodHead(maxFrame) 

def clearShakeHeadAnimation():
    maxFrame = getMaxFrame()
    resetShakeHead(maxFrame) 

def clearWagTailAnimation():
    maxFrame = getMaxFrame()
    resetWagTail(maxFrame)

def clearLiftTailAnimation():
    maxFrame = getMaxFrame()
    resetLiftTail(maxFrame)    
              
#Reseting       
def resetRobinTranslation(maxFrame):
    #Reset transformations
    cmds.setAttr('RobinCTRL.translateX', 0)
    cmds.setAttr('RobinCTRL.translateY', 0)
    cmds.setAttr('RobinCTRL.translateZ', 0)
    
   #Delete key frames
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='translateX', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='translateY', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='translateZ', option='keys' )
    
def resetRobinRotation(maxFrame):  
    #Reset transformations
    cmds.setAttr('RobinCTRL.rotateX', 0)
    cmds.setAttr('RobinCTRL.rotateY', 0)
    cmds.setAttr('RobinCTRL.rotateZ', 0)  
    
    #Delete key frames
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='rotateX', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='rotateY', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='rotateZ', option='keys' ) 
    
def resetLiftTail(maxFrame):
    cmds.setAttr('RobinCTRL.LiftTail', 0)
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='LiftTail', option='keys' )

def resetWagTail(maxFrame):
    cmds.setAttr('RobinCTRL.WagTail', 0)
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='WagTail', option='keys' )
 
def resetNodHead(maxFrame):
    cmds.setAttr('RobinCTRL.NodHead', 0) 
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='NodHead', option='keys' )
 
def resetShakeHead(maxFrame):
    cmds.setAttr('RobinCTRL.ShakeHead', 0) 
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='ShakeHead', option='keys' )
          

def resetBendTorso(maxFrame):
    cmds.setAttr('RobinCTRL.BendTorso', 0)
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='BendTorso', option='keys' ) 
        
def resetSwingLegs(maxFrame):
    cmds.setAttr('RobinCTRL.SwingLegs', 0)
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='SwingLegs', option='keys' ) 

 
def resetLiftWings(maxFrame):
    cmds.setAttr('RobinCTRL.LiftRightWing', 0)
    cmds.setAttr('RobinCTRL.LiftLeftWing', 0)   
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='LiftRightWing', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='LiftLeftWing', option='keys' )
            
def resetRobin():
    #Get max frames
    maxFrame = getMaxFrame()

    #Select robin controller
    cmds.select( 'RobinCTRL', r=True )
    
    #Reset transformations and delete key frames
    resetRobinTranslation(maxFrame)
    resetRobinRotation(maxFrame)
    resetLiftTail(maxFrame)
    resetWagTail(maxFrame)
    resetNodHead(maxFrame) 
    resetShakeHead(maxFrame)
    resetBendTorso(maxFrame)
    resetSwingLegs(maxFrame)
    resetLiftWings(maxFrame)   
    
        
#Actual start of script
createUI()
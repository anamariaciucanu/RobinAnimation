import maya.cmds as cmds
import math
import random  

#To fix: When pressing on Hop and othr buttons twice,
# the Robin movement starts at different points

#Global parameters
#Get parameters from fields and defaults
widgets = {}
mirrorShakeHead = True

pi = math.pi
animationStart = 0
animationEnd = 120
hopFrames = 5
hopHeight = 5
hopSpeed = 1
flapWingsFrames = 5
flapWingsHeight = 5
flapWingsSpeed = 1
shakeHeadFrames = 5
shakeHeadHeight = 5
shakeHeadSpeed = 1


def createUI():    
    #If window exists, delete window
    if cmds.window('robinWindow', exists = True):
        cmds.deleteUI('robinWindow')
        
    #Create window
    widgets['window'] = cmds.window('robinWindow', t='Robin Animator', w = 400, h = 500, sizeable = False, mxb = False, mnb = False)
    windowLayout = cmds.columnLayout(adj = True)
 
    #Create image logo
    logoPath = cmds.internalVar(upd = True) + 'icons/robinAnimator.png'
    logoImage = cmds.image(w = 400, h = 100, image = logoPath)

    #Create reset button for robin
    cmds.button( label='Reset Robin', c = 'resetRobin()', h = 50)
    cmds.separator(h=10, style = 'double')
    
    #Ask user how many animation frames he wants
    cmds.text('How many frames would you like the animation to have?');
    widgets['animationFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Animation Frames')
        
    #Create tabs
    widgets['tabLayout'] = cmds.tabLayout(imw = 5, imh = 5)
    
    #Feet tab
    widgets['feetTab'] = cmds.columnLayout('Feet', w = 400, parent = widgets['tabLayout'])        
    cmds.separator(h=10, style = 'double')
    cmds.text('How many frames per hop?');
    widgets['hopFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Hop Frames')
    cmds.separator(h=10, style = 'double')
    cmds.text('How high should the robin hop?');
    widgets['hopHeight'] = cmds.intFieldGrp( numberOfFields=1, label='Hop Height')
    cmds.separator(h=10, style = 'double')
    cmds.text('How fast should the robin hop?');
    widgets['hopSpeed'] = cmds.intFieldGrp( numberOfFields=1, label='Hop Speed')      
    
    #Create move button
    cmds.separator(h=10, style = 'double')
    cmds.button( label='Hop', c = 'createRobinHopInADirectionAnimation()', w = 100)
    
    #Torso tab
    widgets['torsoTab'] = cmds.columnLayout('Torso', w = 400, parent = widgets['tabLayout'])
    
    #Wings tab
    widgets['wingsTab'] = cmds.columnLayout('Wings', w = 400, parent = widgets['tabLayout'])
    cmds.separator(h=10, style = 'double')
    cmds.text('How many frames per wing flap?');
    widgets['flapWingsFrames'] = cmds.intFieldGrp( numberOfFields=1, label='Flap Wings Frames')
    cmds.separator(h=10, style = 'double')
    cmds.text('How high should the wings go?');
    widgets['flapWingsHeight'] = cmds.intFieldGrp( numberOfFields=1, label='Flap Wings Height')
    cmds.separator(h=10, style = 'double')
    cmds.text('How fast should the wings flap?');
    widgets['flapWingsSpeed'] = cmds.intFieldGrp( numberOfFields=1, label='Flap Wings Speed') 

    #Create move button
    cmds.separator(h=10, style = 'double')    
    cmds.button( label='Flap Wings', c = 'createFlapWingsAnimation()', w = 100)
    
    #Head tab
    widgets['headTab'] = cmds.columnLayout('Head', w = 400, parent = widgets['tabLayout'])
    cmds.button( label = 'Shake Head', c = 'createShakeHeadAnimation()', w = 100)
    
    #Tail tab
    widgets['tailTab'] = cmds.columnLayout('Tail', w = 400, parent = widgets['tabLayout'])    
    cmds.button( label = 'Wag Tail', c = 'createWagTailAnimation()', w = 100)
    
    #Animation sequence tab
    widgets['sequenceTab'] = cmds.columnLayout('Sequence', w = 400, parent = widgets['tabLayout'])    
    cmds.button( label='Create Sequence', c = 'createSequenceAnimation()', w = 100)

    #Show button   
    cmds.showWindow(widgets['window'])
    
def getAnimationEnd():
    localAnimationEnd = cmds.intFieldGrp(widgets['animationFrames'], q = True, v = True)
    if localAnimationEnd > 0:
        global animationEnd
        animationEnd = localAnimationEnd[0]

#Hop methods    
def getHopFrames():
    localHopFrames = cmds.intFieldGrp(widgets['hopFrames'], q = True, v = True)
    if localHopFrames > 0:
        global hopFrames
        hopFrames = localHopFrames[0]
        
def getHopHeight():
    localHopHeight = cmds.intFieldGrp(widgets['hopHeight'], q = True, v = True)
    if localHopHeight > 0:
        global hopHeight
        hopHeight = localHopHeight[0]
                 
def getHopSpeed():
    localHopSpeed = cmds.intFieldGrp(widgets['hopSpeed'], q = True, v = True)
    if localHopSpeed > 0:
        global hopSpeed
        hopSpeed = localHopSpeed[0]

#Flap wings methods    
def getFlapWingsFrames():
    localFlapWingsFrames = cmds.intFieldGrp(widgets['flapWingsFrames'], q = True, v = True)
    if localFlapWingsFrames > 0:
        global flapWingsFrames
        flapWingsFrames = localFlapWingsFrames[0]
        
def getFlapWingsHeight():
    localFlapWingsHeight = cmds.intFieldGrp(widgets['flapWingsHeight'], q = True, v = True)
    if localFlapWingsHeight > 0:
        global flapWingsHeight
        flapWingsHeight = localFlapWingsHeight[0]
                 
def getFlapWingsSpeed():
    localFlapWingsSpeed = cmds.intFieldGrp(widgets['flapWingsSpeed'], q = True, v = True)
    if localFlapWingsSpeed > 0:
        global flapWingsSpeed
        flapWingsSpeed = localFlapWingsSpeed[0]
        flapWingsSpeed = flapWingsSpeed / 10.0
        
def createAnimationSequence():
    animationTypes = random.sample(xrange(5), 5)
    animationTimes = random.sample(xrange(50), 5)
    print animationTypes
    print animationTimes
    
    for a in range(0, 5):
        global animationEnd
        animationEnd = animationEnd + animationTimes[a]
        if animationTypes[a] <= 2:
            #hopping 
            print 'Here 1'
            createRobinHopInADirectionAnimation()
        elif animationTypes[a] > 2:
            #flapping wings 
            createFlapWingsAnimation()
            print 'Here 2'
        global animationStart
        animationStart = animationEnd               
                            
            
def createRobinHopInADirectionAnimation():
    robinCtrl = cmds.select( 'RobinCTRL', r=True )
    getAnimationEnd()
    getHopFrames()
    getHopHeight()   
    getHopSpeed() 
    
    for i in range(animationStart, animationEnd, hopFrames):
        for j in range(0, hopFrames, 1):
            teta = j*pi/hopFrames
            newY = hopHeight * math.fabs(math.sin(teta)) 
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
    

def createFlapWingsAnimation():
    robinCtrl = cmds.select( 'RobinCTRL', r=True )
    getAnimationEnd()
    getFlapWingsFrames()
    getFlapWingsHeight()   
    getFlapWingsSpeed()
    
    for i in range(animationStart, animationEnd, flapWingsFrames):
        for j in range(0, flapWingsFrames, 1):
            teta = j*pi/flapWingsFrames
            rightWingRotation = flapWingsHeight * math.sin(flapWingsSpeed * teta) 
            leftWingRotation = -flapWingsHeight * math.sin(flapWingsSpeed * teta)
        
            cmds.setAttr('RobinCTRL.LiftRightWing', rightWingRotation)
            cmds.setKeyframe( 'RobinCTRL', attribute='LiftRightWing', t=i+j )
            cmds.setAttr('RobinCTRL.LiftLeftWing', leftWingRotation)
            cmds.setKeyframe('RobinCTRL', attribute='LiftLeftWing', t=i+j )
    

def createShakeHeadAnimation():
    robinCtrl = cmds.select('RobinCTRL', r=True)
    getAnimationEnd()
    getShakeHeadFrames()
    getShakeHeadHeight()       
    flip = 1
            
    for i in range(animationStart, animationEnd, shakeHeadFrames):
        if mirrorShakeHead:
            flip = -flip    
        
        for j in range(0, shakeHeadFrames, 1):
            teta = j*pi/shakeHeadFrames            
            headRotation = flip * shakeHeadHeight * math.sin(teta) 
                    
            if headRotation > 90.0:
                headRotation = 90.0
            cmds.setAttr('RobinCTRL.ShakeHead', headRotation)
            cmds.setKeyframe('RobinCTRL', attribute='ShakeHead', t=i+j )
           
    
def resetRobin():
    #Reset robin's position and delete key frames
    maxFrame = cmds.playbackOptions( max = True, query = True )

    #Reset transformations
    cmds.select( 'RobinCTRL', r=True )
    cmds.setAttr('RobinCTRL.translateX', 0)
    cmds.setAttr('RobinCTRL.translateY', 0)
    cmds.setAttr('RobinCTRL.translateZ', 0)
    cmds.setAttr('RobinCTRL.rotateX', 0)
    cmds.setAttr('RobinCTRL.rotateY', 0)
    cmds.setAttr('RobinCTRL.rotateZ', 0)
    cmds.setAttr('RobinCTRL.LiftTail', 0)
    cmds.setAttr('RobinCTRL.WagTail', 0)
    cmds.setAttr('RobinCTRL.NodHead', 0)
    cmds.setAttr('RobinCTRL.ShakeHead', 0)
    cmds.setAttr('RobinCTRL.WagHead', 0)
    cmds.setAttr('RobinCTRL.SwingLegs', 0)
    cmds.setAttr('RobinCTRL.LiftRightWing', 0)
    cmds.setAttr('RobinCTRL.LiftLeftWing', 0)
    
    #Delete key frames
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='translateX', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='translateY', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='translateZ', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='rotateX', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='rotateY', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='rotateZ', option='keys' )  
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='LiftTail', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='WagTail', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='NodHead', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='ShakeHead', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='WagHead', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='SwingLegs', option='keys' )    
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='LiftRightWing', option='keys' )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='LiftLeftWing', option='keys' )
    
#Actual start of script
createUI()
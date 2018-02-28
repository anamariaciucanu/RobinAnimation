import maya.cmds as cmds
import math

#If window exists, delete window
if cmds.window("robinWindow", exists = True):
    cmds.deleteUI("robinWindow")
    
#Create window and imge logo
robinWindow = cmds.window("robinWindow", t="Robin Animator", w = 400, h = 300, sizeable = False)
cmds.columnLayout(adj = True)
logoPath = cmds.internalVar(upd = True) + "icons/robinAnimator.png"
cmds.image(w = 400, h = 100, image = logoPath)

#Create reset button for robin
cmds.separator(h=10, style = 'double')
cmds.button( label='Reset Robin', c = "resetRobin()", h = 50)

#Ask user how many animation frames he wants
cmds.separator(h=10, style = 'double')
cmds.text('How many frames would you like the nimation to have?');
animationFrames = cmds.intFieldGrp( numberOfFields=1, label='Animation Frames')
cmds.separator(h=10, style = 'double')
cmds.text('How many frames would you like per hop?');
hopFrames = cmds.intFieldGrp( numberOfFields=1, label='Hop Frames')
cmds.separator(h=10, style = 'double')
cmds.text('How high should the robin hop?');
hopAmplitude = cmds.intFieldGrp( numberOfFields=1, label='Hop Height')

#Create animate button
cmds.separator(h=10, style = 'double')
cmds.button( label='Move Robin', c = "createRobinMoveDirectionAnimation()", h = 50)
cmds.button( label='Flap Wings', c = "createFlapWingsAnimation()", h = 50)
   
cmds.showWindow(robinWindow)


def createRobinMoveDirectionAnimation():
    robinCtrl = cmds.select( 'RobinCTRL', r=True )
    frames = cmds.intFieldGrp(animationFrames, q = True, v = True)
    steps = cmds.intFieldGrp(hopFrames, q = True, v = True)
    amplitude = cmds.intFieldGrp(hopAmplitude, q = True, v = True)
    pi=math.pi
    
    for i in range(0, frames[0], steps[0]):
        for j in range(0, steps[0], 1):
            radius = steps[0]/2.0
            teta = j*pi/steps[0]
            newY = radius * amplitude[0] * math.fabs(math.sin(teta)) 
            newX = radius * math.fabs(math.cos(teta)) 
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
    frames = cmds.intFieldGrp(animationFrames, q = True, v = True)
    steps = cmds.intFieldGrp(hopFrames, q = True, v = True)
    amplitude = cmds.intFieldGrp(hopAmplitude, q = True, v = True)
    pi=math.pi
    
    for i in range(0, frames[0], steps[0]):
        for j in range(0, steps[0], 1):
            radius = steps[0]/2.0
            teta = j*pi/steps[0]
            rightWingRotation = radius * amplitude[0] * math.sin(teta) 
            leftWingRotation = -radius * amplitude[0] * math.sin(teta)
        
            cmds.setAttr('RobinCTRL.LiftRightWing', rightWingRotation)
            cmds.setKeyframe( 'RobinCTRL', attribute='LiftRightWing', t=i+j )
            cmds.setAttr('RobinCTRL.LiftLeftWing', leftWingRotation)
            cmds.setKeyframe( 'RobinCTRL', attribute='LiftLeftWing', t=i+j )
    

    
#Reset robin's position and delete key frames
maxFrame = cmds.playbackOptions( max = True, query = True )

def resetRobin():
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
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='translateX', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='translateY', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='translateZ', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='rotateX', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='rotateY', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='rotateZ', option="keys" )  
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='LiftTail', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='WagTail', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='NodHead', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='ShakeHead', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='WagHead', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='SwingLegs', option="keys" )    
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='LiftRightWing', option="keys" )
    cmds.cutKey( 'RobinCTRL', time=(0,maxFrame), attribute='LiftLeftWing', option="keys" )
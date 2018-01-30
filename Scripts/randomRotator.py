import maya.cmds as cmds
import random as rand

def getSpecificObjectsIntoArray(objectName):
	return cmds.ls(objectName)

def randomRotator(objectName):
	for objects in getSpecificObjectsIntoArray(objectName):
		#rotate objects around Y change here if you want other axises
		rN = rand.uniform(-0.1,0.1)
		print rN
		cmds.rotate(0,rN,0, objects, a = True)


randomRotator('group*')
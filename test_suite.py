#Kyle Chen
#test_suite
#nemo prototype 1
#1/24/07

import unittest
from pygame.locals import *
from nemo import *



#class DefaultWidgetSizeTestCase(unittest.TestCase):
#	def runTest(self):
#        	widget = Widget("The widget")
#                assert widget.size() == (50,50), 'incorrect default size'

class NemoTest(unittest.TestCase):
	def testKeyStart(self):
		M=fMarlin()
		M.processKeyPress(pygame.K_s)
		result = M.isrunning()
		self.assertEqual(result, 1)

	def testKeyStop(self):
		M=fMarlin()
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_s)
		result = M.isrunning()
		self.assertEqual(result, 0)

	def testMoveDown(self):
		M=fMarlin()
		r = M.rect.bottom
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_DOWN)
		M.think()
		new_r = M.rect.bottom
		difference = new_r-r
		self.assertEqual(difference, 3) #Marlin move by speed 3
	
	def testMoveUp(self):
		M=fMarlin()
		r = M.rect.top
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_UP)
		M.think()
		new_r = M.rect.top
		difference = new_r-r
		self.assertEqual(difference, -3) #Marlin move by speed 3

	def testMoveLeft(self):
		M=fMarlin()
		r = M.rect.left
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_LEFT)
		M.think()
		new_r = M.rect.left
		difference = new_r-r
		self.assertEqual(difference, -3) #Marlin move by speed 3

	def testMoveRight(self):
		M=fMarlin()
		r = M.rect.right
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_RIGHT)
		M.think()
		new_r = M.rect.right
		difference = new_r-r
		self.assertEqual(difference, 3) #Marlin move by speed 3

	def testMoveLeftScreen(self):
		M =fMarlin()
		#start: 160-35 = 125
		M.rect.move_ip(-125, 0) #move to very left
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_LEFT)
		M.think()
		r = M.rect.left
		self.assertEqual(r, 0)

	def testMoveRightScreen(self):
		M =fMarlin()
		#start: 160+35 = 195  640 -195 = 445
		M.rect.move_ip(445, 0) #move to very right
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_RIGHT)
		M.think()
		r = M.rect.right
		self.assertEqual(r, 640)

	def testMoveBottomScreen(self):
		M =fMarlin()
		#start: 368+21 = 389  480-389 = 91
		M.rect.move_ip(0, 91) #move to very bottom
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_DOWN)
		M.think()
		r = M.rect.bottom
		self.assertEqual(r, 480)
		
	def testMoveTopScreen(self):
		M =fMarlin()
		#start: 368-21 = 347  0-347 = -347
		M.rect.move_ip(0, -347) #move to very top
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_UP)
		M.think()
		r = M.rect.top
		self.assertEqual(r, 0)
	
	def testCollideJellyMarlin(self):
		M=fMarlin()
		#75+35 = 110
		J=Jellyfish(160-110,368) #start right infront of Marlin
		#move Marlin toward Jellyfish
		M.processKeyPress(pygame.K_s)
		M.processKeyPress(pygame.K_LEFT)
		M.think()
		self.assertTrue(M.rect.colliderect(J.rect), "M and J doesn't collide")
		
if __name__ == "__main__":
	unittest.main()

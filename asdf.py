from Link import Link
import pygame
import math

screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

p = []
stationary = [0,50,95,96,97,98,99,100,101,490,491,492,493,494,495,496,497,498,499,500,501]
for x in range(501):
	p.append(Link([20+0.001*x + 300,180],[40,-40]))

p.append(Link([100 + 300,180],[40,-40]))

"""
for x in range(51):
	xpi = x*math.pi/25+1.5*math.pi
	p.append(Link([360+100*math.cos(xpi),150+100*math.sin(xpi)], [0,0])) 
"""
equil = 1
k = 250
gravity = 10
timestep = 25
timestamp = 50
damping = 0.999

while True:
	clock.tick(FPS)

	"""Temporarily making the first block stationary"""
	for i in range(len(p)):
		if i not in stationary:
			p[i].set_pos([p[i].get_pos()[0] + p[i].get_vel()[0] / timestep , p[i].get_pos()[1] + p[i].get_vel()[1] / timestep]) 

	d = []
	for i in range(len(p)-1):	
		d.append(math.sqrt((p[i+1].get_pos()[0]-p[i].get_pos()[0]) ** 2 + (p[i+1].get_pos()[1] - p[i].get_pos()[1]) ** 2))

	f = []
	for i in range(len(p)-1):
		new_force = k * (d[i] - equil) * (-1)
		f.append(new_force)
	
	fx = []
	fy = []
	for j in range(len(p)-2):
		i = j+1
		horizontal = (p[i].get_pos()[0] - p[i-1].get_pos()[0])/d[i-1] * f[i-1] + (p[i].get_pos()[0] - p[i+1].get_pos()[0])/d[i] * f[i]
		vertical = gravity + (p[i].get_pos()[1] - p[i-1].get_pos()[1])/d[i-1] * f[i-1] + (p[i].get_pos()[1] - p[i+1].get_pos()[1])/d[i] * f[i]
		fx.append(horizontal)
		fy.append(vertical)


	# Update the first and last positions	
	fx.append((p[len(p)-1].get_pos()[0] - p[len(p)-2].get_pos()[0])/d[-1] * f[-1])
	fy.append(gravity + (p[len(p)-1].get_pos()[1] - p[len(p)-2].get_pos()[1])/d[-1] * f[-1])	
	fx.insert(0, (p[0].get_pos()[0] - p[1].get_pos()[0])/d[0] * f[0])
	fy.insert(0, gravity + (p[0].get_pos()[1] - p[1].get_pos()[1])/d[0] * f[0]) 

	for i in range(len(p)):
		p[i].set_vel([p[i].get_vel()[0]*damping + fx[i] / timestamp, p[i].get_vel()[1]*damping + fy[i] / timestamp])
	"""
	fx0 = (positions[0][0] - positions[1][0])/d1 * f1
	fx1 = (positions[1][0] - positions[0][0])/d1 * f1 + (positions[1][0]-positions[2][0])/d2 * f2 
	fx2 = (positions[2][0] - positions[1][0])/d2 * f2
	fy0 = gravity + (positions[0][1] - positions[1][1])/d1 * f1
	fy1 = gravity + (positions[1][1] - positions[0][1])/d1 * f1 + (positions[1][1]-positions[2][1])/d2 * f2 
	fy2 = gravity + (positions[2][1] - positions[1][1])/d2 * f2

	velocities[0][0] += fx0 / timestamp
	velocities[1][0] += fx1 / timestamp
	velocities[2][0] += fx2 / timestamp
	velocities[0][1] += fy0 / timestamp
	velocities[1][1] += fy1 / timestamp
	velocities[2][1] += fy2 / timestamp
	"""
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				p.pop(len(p) // 2 )
			elif event.key == pygame.K_s:
				p.pop(-1)
			elif event.key == pygame.K_UP:
				p[-1].set_pos([p[-1].get_pos()[0], p[-1].get_pos()[1] - 3])
			elif event.key == pygame.K_DOWN:
				p[-1].set_pos([p[-1].get_pos()[0], p[-1].get_pos()[1] + 3])
			elif event.key == pygame.K_LEFT:
				p[-1].set_pos([p[-1].get_pos()[0] - 3, p[-1].get_pos()[1]])
			elif event.key == pygame.K_RIGHT:
				p[-1].set_pos([p[-1].get_pos()[0] + 3, p[-1].get_pos()[1]])

	screen.fill(WHITE)
	for lin in p:
		# pygame.draw.circle(screen, BLACK, lin.get_pos(), 2)
		pass	
	for i in range(len(p)-1):
		pygame.draw.line(screen,BLACK, p[i].get_pos(), p[i+1].get_pos())
	pygame.display.update()  # Or pygame.display.flip()

import pygame, math

WIDTH, HEIGHT = 800, 600
G = 6.674e-1
DT = 0.1
TRAIL_LENGTH = 500 #in pixels

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Body:
    def __init__(self, x, y, vx, vy, m, color, radius):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.m = m
        self.color = color
        self.radius = radius
        self.trail = []
    def update(self, bodies):
        Fx, Fy = 0, 0

        for other in bodies:

            if other == self:
                continue
            
            dx = other.x - self.x
            dy = other.y - self.y

            r = math.sqrt(dx*dx + dy*dy)

            if r == 0:
                continue

            F = G * ((self.m * other.m) / (r*r))

            Fx += F * (dx / r)
            Fy += F * (dy / r)

        ax = Fx / self.m
        ay = Fy / self.m

        self.vx = self.vx + ax * DT
        self.vy = self.vy + ay * DT

        self.x = self.x + self.vx * DT
        self.y = self.y + self.vy * DT

        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

sun = Body(WIDTH//2, HEIGHT//2, 0, 0, 50000, (255, 180, 42), 10)
planet1 = Body(WIDTH//2 + 250, HEIGHT//2, 0, -6, 3000, (0, 50, 255), 5)
planet2 = Body(WIDTH//2 + 350, HEIGHT//2, 2, -9, 5000, (0, 255, 50), 7)


bodies = [sun, planet1, planet2]

running = True

while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for body in bodies:
        body.update(bodies)

        pygame.draw.circle(screen, body.color, (int(body.x), int(body.y)), body.radius)

        if len(body.trail) > 1:
            pygame.draw.lines(screen, body.color, False, body.trail, 1)

    font = pygame.font.SysFont("Arial", 20)

    fps = int(clock.get_fps())

    fps_text = font.render(f"Fps: {fps}", True, (255, 255, 255))

    screen.blit(fps_text, (10, 10))
     
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
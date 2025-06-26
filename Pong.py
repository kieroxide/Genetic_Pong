from Canvas import Canvas
import pygame

class Pong:
    def __init__(self):
        self.score = 0

        self.canvas = Canvas()
        self.paddle = None
        self.ball = None

        self.paddle_speed = 10
        self.velocity = [8,8]

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.score_text = self.canvas.font.render(f"Score: {self.score}", True, self.WHITE)

        self.running = True
    
    def start(self):
        self.setup()
        self.game_loop()

    def setup(self):
        self.ball = pygame.Rect(400, 300, 15, 15)
        self.paddle = pygame.Rect(30, 200, 10, 100)

    def quitCheck(self):
        #Allows to quit using window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def controlsCheck(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.paddle.y -= self.paddle_speed
        if keys[pygame.K_s]:
            self.paddle.y += self.paddle_speed  

        # Clamp paddle inside window
        if self.paddle.top < 0:
                self.paddle.top = 0
        if self.paddle.bottom > 600:
            self.paddle.bottom = 600

    def collision_detection(self):
        if(self.paddle.colliderect(self.ball)):
            self.ball.left = self.paddle.right
            self.velocity[0] = -self.velocity[0]
            self.score += 1
            self.score_text = self.canvas.font.render(f"Score: {self.score}", True, self.WHITE)
    
    def boundary_detection(self):
        if(self.ball.top < 0 or self.ball.bottom > self.canvas.HEIGHT):
            self.velocity[1] = -self.velocity[1]
        if(self.ball.left < 0 or self.ball.right > self.canvas.WIDTH):
            self.velocity[0] = -self.velocity[0]
    
    def update(self):
        self.ball.x += self.velocity[0]
        self.ball.y += self.velocity[1]

    def draw(self):
        #Clears, Draws objects, then updates display
        self.canvas.screen.fill(self.BLACK)
        self.canvas.screen.blit(self.score_text,(self.canvas.WIDTH/2 , 20))

        pygame.draw.rect(self.canvas.screen, self.WHITE, self.paddle)
        pygame.draw.rect(self.canvas.screen, self.WHITE, self.ball)

        pygame.display.flip()

    def game_loop(self):
        self.running = True
        while self.running:
            self.quitCheck()
            self.controlsCheck()

            self.boundary_detection()
            self.collision_detection()

            self.update()
            self.draw()

            self.canvas.clock.tick(60)
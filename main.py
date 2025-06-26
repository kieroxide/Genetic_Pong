import pygame

# Settings
WIDTH, HEIGHT = 1000, 600
FPS = 60

# Colours
WHITE = (255, 255, 255)
BLACK = (0  , 0, 0)

# Ball Velocity
velocity = [8, 8]

# Paddle Speed
speed = 10

score = 0

def main():
    screen, clock, font = init()
    paddle = pygame.Rect(50, 250, 10, 100)
    ball = pygame.Rect(400, 300, 15, 15)
    rects = {'paddle' : paddle, 'ball' : ball}
    
    game_loop(screen, clock, rects, font)

def game_loop(screen, clock, rects, font):
    running = True
    while running:
        running = quitCheck()
        controlsCheck(rects)

        boundary_detection(rects['ball'])
        collision_detection(rects['paddle'], rects['ball'])

        rects['ball'] = update(rects['ball'])
        score_text = font.render(f"Score: {score}", True, WHITE) 
        draw(screen, rects, score_text)
        clock.tick(60)

def collision_detection(paddle, ball):
    global score
    if(paddle.colliderect(ball)):
        ball.left = paddle.right
        velocity[0] = -velocity[0]
        score += 1

def boundary_detection(rect):
    if(rect.top < 0 or rect.bottom > HEIGHT):
        velocity[1] = -velocity[1]
    if(rect.left < 0 or rect.right > WIDTH):
        velocity[0] = -velocity[0]

def update(ball):
    ball.x += velocity[0]
    ball.y += velocity[1]
    return ball

def init():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong GA")
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 30)

    return screen, clock, font

def quitCheck(running = True):
    #Allows to quit using window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    return running

def controlsCheck(rects):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        rects['paddle'].y -= speed 
    if keys[pygame.K_s]:
        rects['paddle'].y += speed  

    # Clamp paddle inside window
    if rects['paddle'].top < 0:
            rects['paddle'].top = 0
    if rects['paddle'].bottom > 600:
        rects['paddle'].bottom = 600

def draw(screen, rects, score_text):
    #Clears, Draws objects, then updates display
    screen.fill(BLACK)
    screen.blit(score_text,( WIDTH/2 , 20))
    for rect in rects.values():
        pygame.draw.rect(screen, WHITE , rect)
    pygame.display.flip()

main()
import numpy as np
from NeuralNet import NeuralNet

def ai_controls(pong, net):
    #normalized inputs
    inputs = np.array([
        pong.ball.centerx / pong.WIDTH,
        pong.ball.centery / pong.HEIGHT,
        pong.velocity[0] / pong.max_speed,
        pong.velocity[1] / pong.max_speed,
        pong.paddle.centery / pong.HEIGHT,
        (pong.ball.centery - pong.paddle.centery) / pong.HEIGHT
    ])

    output = net.forward(inputs)[0]
    if(output < 0.4):
        pong.paddle.y += pong.paddle_speed
    elif(output > 0.6):
        pong.paddle.y -= pong.paddle_speed

    if(pong.paddle.top < 0) : pong.paddle.top = 0
    if(pong.paddle.bottom > pong.HEIGHT) : pong.paddle.bottom = pong.HEIGHT
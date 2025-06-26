import numpy as np
from NeuralNet import NeuralNet

def GA(pong, net):
    inputs = np.array([
        [pong.ball.y / pong.HEIGHT],       
        [pong.velocity[1] / pong.max_speed], 
        [pong.paddle.y / pong.HEIGHT]
    ])

    output = net.forward(inputs)  # Output between 0 and 
    if(output < 0.50):
        pong.paddle.y += pong.paddle_speed
    else:
        pong.paddle.y -= pong.paddle_speed
    if(pong.paddle.top < 0) : pong.paddle.top = 0
    if(pong.paddle.bottom > pong.HEIGHT) : pong.paddle.bottom = pong.HEIGHT
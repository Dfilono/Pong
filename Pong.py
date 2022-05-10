# -*- coding: utf-8 -*-
"""
Created on Mon May  9 17:54:32 2022

@author: filon
"""

import pygame

pygame.init()
width, height = 800, 500

window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Pong")
FPS = 60
white = (255,255,255)
black = (0,0,0)

paddle_w, paddle_h = 20, 100
ball_radius = 7
score_font = pygame.font.SysFont("times new roman", 50)
winning = 10

class Paddle:
    vel = 4
    
    def __init__(self,x,y,w,h):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.w = w
        self.h = h
        
    def draw_pad(self,win):
        pygame.draw.rect(win,white,(self.x,self.y,self.w,self.h))

    def move(self, up=True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    max_vel = 5
    
    def __init__(self,x,y,radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.r = radius
        self.x_vel = self.max_vel
        self.y_vel = 0
        
    def draw_ball(self,win):
        pygame.draw.circle(win,white,(self.x,self.y),self.r)
        
    def move_ball(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def collision(ball, left_paddle, right_paddle):
    if ball.y + ball.r >= height:
        ball.y_vel *= -1
    elif ball.y - ball.r <= 0:
        ball.y_vel *= -1
        
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.h:
            if ball.x - ball.r <= left_paddle.x + left_paddle.w:
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.h / 2
                dif_y = middle_y - ball.y
                reduc = (left_paddle.h / 2) / ball.max_vel
                y_vel = dif_y / reduc
                ball.y_vel = -1*y_vel
                
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.h:
            if ball.x + ball.r >= right_paddle.x:
                ball.x_vel *= -1
                
                middle_y = right_paddle.y + right_paddle.h / 2
                dif_y = middle_y - ball.y
                reduc = (right_paddle.h / 2) / ball.max_vel
                y_vel = dif_y / reduc
                ball.y_vel = -1*y_vel
                
                
def draw(win, paddles,ball, left_score, right_score):
    win.fill(black)
    
    left_score_txt = score_font.render(f"{left_score}",1,white)
    right_score_txt = score_font.render(f"{right_score}",1,white)
    win.blit(left_score_txt, (width//4 - left_score_txt.get_width()//2,20))
    win.blit(right_score_txt, (width*3//4 - right_score_txt.get_width()//2,20))
    
    for paddle in paddles:
        paddle.draw_pad(win)
        
    for i in range(10, height, height//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win,white,(width//2 - 5, i, 10, height//20))
        
    ball.draw_ball(win)
    
    pygame.display.update()

def paddle_move(keys,left_paddle,right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.vel >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.vel + left_paddle.h <= height:
        left_paddle.move(up=False)
    
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.vel >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.vel + right_paddle.h <= height:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10,height//2 - paddle_h//2,paddle_w,paddle_h)
    right_paddle = Paddle(width - paddle_w - 10,height//2 - paddle_h//2,paddle_w,paddle_h)
    
    ball = Ball(width//2,height//2,ball_radius)
    
    left_score = 0
    right_score = 0
    
    while run:
        clock.tick(FPS)
        draw(window, [left_paddle,right_paddle],ball, left_score, right_score)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        paddle_move(keys,left_paddle,right_paddle)
        
        ball.move_ball()
        collision(ball, left_paddle, right_paddle)
        
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > width:
            left_score += 1
            ball.reset()
        
        won = False
        if left_score >= winning:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= winning:
            won = True
            win_text = "Right Player Won!"
            
        if won:
            text = score_font.render(win_text,1,white)
            window.blit(text,(width//2 - text.get_width()//2, height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
        
    pygame.quit()
    
if __name__ == "__main__":
    main()
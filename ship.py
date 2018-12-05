#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 21:56
# @Author  : zsj
# @File    : ship.py
# @Description:

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen  = screen
        self.settings= settings

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每艘船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船的属性center中存储小数值
        self.centerx = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        #飞船的移动，上下左右
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.shot = False

        #飞船的速度，可以调整
        self.speed_factor = settings.ship_speed_factor

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.centerx -= self.settings.ship_speed_factor
        self.rect.centerx = self.centerx

        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.bottom -= self.settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.settings.ship_speed_factor
        self.rect.bottom = self.bottom

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.centerx = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom


    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)


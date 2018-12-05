#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/3 11:27
# @Author  : zsj
# @File    : alien.py
# @Description:
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像，设置rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #每个外星人最初都是在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人的准确位置
        self.x = float(self.rect.x)

    def update(self):
        """向右移动外星人"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """屏幕画外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人在边缘就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left:
            return True


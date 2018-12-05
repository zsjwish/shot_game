#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 15:27
# @Author  : zsj
# @File    : button.py
# @Description:
import pygame

class Button():
    """Pygame没有内置创建按钮的方法，我们创建一个Button 类，用于创建带标签的实心矩形"""
    def __init__(self, ai_settings, screen, msg):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        #设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.botton_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)
        #创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #按钮的标签只创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.botton_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本,使用fill来填充颜色
        self.screen.fill(self.botton_color, self.rect)
        #使用blit传递一幅图片并设置关联的rect对象
        self.screen.blit(self.msg_image, self.msg_image_rect)

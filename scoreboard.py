#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 20:27
# @Author  : zsj
# @File    : scoreboard.py
# @Description:

import pygame
from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # 最高得分
        with open(self.ai_settings.score_text_name, 'r') as file_object:
            high_score = file_object.read()
        if high_score is None or len(high_score) == 0:
            self.high_score_str = 0
        else:
            self.high_score_str = int(high_score)
        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.high_score_color = (255,0,0)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像
        self.prep_score()
        #准备初始化最高得分
        self.prep_high_score()
        #准备初始化游戏难度等级
        self.prep_level()
        #准备初始化剩余飞船数量
        self.prep_ships()

    def prep_score(self):
        """将得分转换成一幅渲染的图像"""
        round_score = round(self.stats.score, -1)
        score_str = format(round_score,',')
        self.score_image = self.font.render("score:"+score_str, True, self.text_color, self.ai_settings.bg_color)
        #将得分放在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        #重置最高得分
        if int(self.high_score_str) < round_score:
            self.high_score_str = round_score

    def prep_high_score(self):
        """将最高分转换成一副渲染的图像"""
        high_score_str = format(self.high_score_str, ',')
        self.high_score_image = self.font.render("high:"+high_score_str, True, self.high_score_color, self.ai_settings.bg_color)
        #将最高分放在个人得分的下面
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.right / 2 - 40
        self.high_score_rect.top = 20

    def prep_level(self):
        """将游戏等级显示在界面上"""
        self.level_image = self.font.render("level:"+str(self.stats.level),True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = 60

    def prep_ships(self):
        """显示剩余飞船数量"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        #绘制游戏得分
        self.screen.blit(self.score_image, self.score_rect)
        #绘制游戏最高得分
        self.screen.blit(self.high_score_image, self.high_score_rect)
        #绘制游戏难度等级
        self.screen.blit(self.level_image, self.level_rect)
        #绘制剩余飞船数量
        self.ships.draw(self.screen)
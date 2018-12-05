#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 20:44
# @Author  : zsj
# @File    : setting.py
# @Description:
import pygame


class Setting():
    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #飞船速度设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        #子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60

        #连续发射子弹频率
        self.bullet_rate = 50

        #发射子弹时钟
        self.ticks = 0

        #外星人向下移动速度
        self.fleet_drop_speed = 20

        #加快游戏速度

        self.speed_up = 1.1
        #外星人得分增长
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        #最高分存储文件名
        self.score_text_name = 'score.txt'

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        #fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1
        #记分，每个外星人50分
        self.alien_points = 50
        #难度等级，显示在界面上
        self.level = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speed_up
        self.bullet_speed_factor *= self.speed_up
        self.alien_speed_factor *= self.speed_up
        self.alien_points = int(self.alien_points * self.score_scale)
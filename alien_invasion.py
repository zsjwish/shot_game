#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 20:33
# @Author  : zsj
# @File    : alien_invasion.py
# @Description:


import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from setting import Setting
from ship import Ship


def run_game():
    pygame.init()
    ai_settings = Setting()
    #创建一个窗口，参数就是窗口的宽和高
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    #设置窗口的title
    pygame.display.set_caption("星球大战")

    #创造一艘飞船
    ship = Ship(ai_settings, screen)

    #用于创建一个用于存储子弹的编组
    bullets = Group()

    #创造外星人编组
    aliens = Group()

    #创造外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    #创建一个开始游戏button
    play_button = Button(ai_settings, screen, "play")

    #创建记分牌
    scoreboard = Scoreboard(ai_settings, screen, stats)

    #初始化背景音乐
    pygame.mixer_music.load('music/bgm.mp3')
    pygame.mixer_music.play(-1)

    while True:
        #监视鼠标和键盘
        gf.check_events(ai_settings, screen, stats, ship, aliens, bullets, play_button, scoreboard)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, ship, aliens, bullets, scoreboard)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)
        gf.update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button)
run_game()
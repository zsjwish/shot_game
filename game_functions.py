#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 23:30
# @Author  : zsj
# @File    : game_functions.py
# @Description:
import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet

def check_events(ai_settings, screen, stats, ship, aliens, bullets, play_button, scoreboard):
    """键盘鼠标事件检测"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game(ai_settings, scoreboard)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, scoreboard, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets, scoreboard)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship, ai_settings, scoreboard)

def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets, scoreboard):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        print("向右")
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
        print("向左")
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
        print("向后")
    elif event.key == pygame.K_UP:
        ship.moving_up = True
        print("向前")
    elif event.key == pygame.K_SPACE:
        #连续射击
        ship.shot = True
        ai_settings.ticks = 0
        #单点射击
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        reset_game(ai_settings, screen, stats, ship, aliens, bullets, scoreboard)

def check_keyup_events(event, ship, ai_settings, scoreboard):
    """松开键响应"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_SPACE:
        ship.shot = False
        ai_settings.ticks = 0
    elif event.key == pygame.K_ESCAPE:
        quit_game(ai_settings, scoreboard)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, scoreboard, mouse_x, mouse_y):
    """在玩家单击play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        """如果点击了play按钮并且游戏处于未激活状态"""
        reset_game(ai_settings, screen, stats, ship, aliens, bullets, scoreboard)

def quit_game(ai_settings, scoreboard):
    """退出游戏，退出之前先保存最高分成绩"""
    with open(ai_settings.score_text_name, 'w+') as file_object:
        file_object.write(str(scoreboard.high_score_str))
    sys.exit()

def reset_game(ai_settings, screen, stats, ship, aliens, bullets, scoreboard):
    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True

    #重置游戏得分
    scoreboard.prep_score()
    scoreboard.prep_level()
    scoreboard.prep_ships()

    #重置游戏设置
    ai_settings.initialize_dynamic_settings()
    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()



def fire_bullet(ai_settings, screen, ship, bullets):
    """创造子弹"""
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)

def get_number_alien_x(ai_settings, alien_width):
    """获取每行可以放多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))

def get_number_alien_y(ai_settings, ship_height, alien_height):
    """获取外星人行数"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_fleet(ai_settings, screen, ship, aliens):
    """创造外星人集合"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_alien_x = get_number_alien_x(ai_settings, alien_width)
    number_alien_y = get_number_alien_y(ai_settings, ship.rect.height, alien.rect.height)
    """循环生成矩阵外星人"""
    for alien_number_x in range(number_alien_x):
        for alien_number_y in range(number_alien_y):
            create_alien(ai_settings, screen, aliens, alien_number_x, alien_number_y)

def create_alien(ai_settings, screen, aliens, alien_number_x, alien_number_y):
    """创造外星人"""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number_x
    alien.y = alien_height + 2 * alien_height * alien_number_y
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
    """
    检查是否到达了边缘并在屏幕上更新外星人
    """
    check_fleet_edges(ai_settings, aliens)
    #检查是否有外星人到达了屏幕底部
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)
    aliens.update()
    """检测外星人碰撞到了飞船"""
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, scoreboard, ship, aliens, bullets)

def ship_hit(ai_settings, stats, screen, scoreboard, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    stats.ships_left -= 1
    # 更新飞船数量
    scoreboard.prep_ships()

    if stats.ships_left > 0:
        #清空子弹列表和外星人列表
        aliens.empty()
        bullets.empty()

        #重新创建一群外星人和一个ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #暂停0.5s
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_bullets(ai_settings, screen, stats, ship, aliens, bullets, scoreboard):
    """更新子弹"""
    if ship.shot:
        ai_settings.ticks += 1
        if ai_settings.ticks % 20 == 0:
            fire_bullet(ai_settings, screen, ship, bullets)
    bullets.update()
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets, scoreboard)

def check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets, scoreboard):
    """
    检查是否子弹击中了外星人，如果击中则同时删除这个子弹和外星人
    参数:两个group检查是否碰撞，第一个True是否删除第一个group,即是否删除子弹，如果为False则一颗子弹一直消灭外形人
    """
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    #记分 collisions是一个字典，key是子弹，value是aliens列表，所以只需要计算得出所有的alien数量就可以计算得分
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
            scoreboard.prep_high_score()
    """如果所有的外形人都被消灭了，则重新初始化一群外形人,并删除之前的子弹"""
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        scoreboard.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def check_fleet_edges(ai_settings, aliens):
    """检查每个外星人是否达到了左右边界"""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
    """检查是否有外星人到达了屏幕低端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom > screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, scoreboard, ship, aliens, bullets)
            break

def change_fleet_direction(ai_settings, aliens):
    """外星人整体下移并更改其移动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)

    #在飞船和外星人后面重新绘制多有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #飞船更新
    ship.blitme()
    #外星人更新
    aliens.draw(screen)

    #显示计分板
    scoreboard.show_score()
    #如果游戏处于非活动状态则绘制开始游戏按钮
    if not stats.game_active:
        play_button.draw_button()
    #绘制图像
    pygame.display.flip()


import arcade
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Spaceshooter"

PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        
        self.player_list = None
        self.player = None
        self.bullets = None
        self.enemies = None
        self.bosses = None
        self.enemy_bullets = None
        self.boss_bullets = None
        self.explosions = None
        self.score = 0
        self.player_lives = 3
        self.boss_spawned = False
        self.boss_hp = 5
        self.enemy_speed = 2
        self.enemy_bullet_speed = -4

        self.boss_shoot_timer = 0
        self.enemy_shoot_timer = 0

        #HIntergrund
        self.background_sprite = arcade.Sprite("/Users/anton/Library/CloudStorage/OneDrive-Persönlich/Python/Games/SpaceShooter/Grafik/wallpaper.jpg")
        self.background_sprite.center_x = WINDOW_WIDTH // 2
        self.background_sprite.center_y = WINDOW_HEIGHT // 2
        self.background_sprite.width = WINDOW_WIDTH
        self.background_sprite.height = WINDOW_HEIGHT

        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background_sprite)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.bosses = arcade.SpriteList()
        self.enemy_bullets = arcade.SpriteList()
        self.boss_bullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.score = 0
        self.player_lives = 3
        self.boss_spawned = False
        self.boss_defeated = False
        self.boss_hp = 5

        self.player = arcade.Sprite("/Users/anton/Library/CloudStorage/OneDrive-Persönlich/Python/Games/SpaceShooter/Grafik/spaceship.png", 2)
        self.player.center_x = WINDOW_WIDTH // 2
        self.player.center_y = 80
        self.player_list.append(self.player)

    def spawn_enemy(self):
        enemy = arcade.Sprite("/Users/anton/Library/CloudStorage/OneDrive-Persönlich/Python/Games/SpaceShooter/Grafik/enemy.png", 2)
        enemy.center_x = WINDOW_WIDTH + 40
        enemy.center_y = random.randint(40, WINDOW_HEIGHT - 40)
        enemy.change_x = -self.enemy_speed
        self.enemies.append(enemy)

    def spawn_boss(self):
        boss = arcade.Sprite("/Users/anton/Library/CloudStorage/OneDrive-Persönlich/Python/Games/SpaceShooter/Grafik/ship_boss.png", 2)
        boss.center_x = WINDOW_WIDTH + 50
        boss.center_y = WINDOW_HEIGHT // 2
        boss.change_x = -self.enemy_speed
        self.bosses.append(boss)
        self.boss_hp = 5

    def create_explosion(self, x, y):
        explosion = arcade.Sprite("/Users/anton/Library/CloudStorage/OneDrive-Persönlich/Python/Games/SpaceShooter/Grafik/explosion.png    ", 2)
        explosion.center_x = x
        explosion.center_y = y
        explosion.timer = 10
        self.explosions.append(explosion)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.change_x = -PLAYER_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = PLAYER_SPEED
        elif key in (arcade.key.UP, arcade.key.W):
            self.player.change_y = PLAYER_SPEED
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.SPACE:
            bullet = arcade.SpriteCircle(5, arcade.color.YELLOW)
            bullet.center_x = self.player.center_x + 20
            bullet.center_y = self.player.center_y
            bullet.change_x = BULLET_SPEED
            self.bullets.append(bullet)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = 0
        if key in (arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S):
            self.player.change_y = 0

    def on_update(self, dt):
        self.player_list.update()
        self.bullets.update()
        self.enemies.update()
        self.bosses.update()
        self.enemy_bullets.update()
        self.boss_bullets.update()
        self.explosions.update()

        # Zufällige Gegner spawnen
        if random.random() < 0.02:
            self.spawn_enemy()

        # Spieler schießt Gegner
        for bullet in list(self.bullets):
            hit_enemies = arcade.check_for_collision_with_list(bullet, self.enemies)
            hit_bosses = arcade.check_for_collision_with_list(bullet, self.bosses)

            if hit_enemies or hit_bosses:
                bullet.remove_from_sprite_lists()
                self.score += 20
                for enemy in hit_enemies:
                    self.create_explosion(enemy.center_x, enemy.center_y)
                    enemy.remove_from_sprite_lists()
                for boss in hit_bosses:
                    self.boss_hp -= 1
                    if self.boss_hp <= 0:
                        self.create_explosion(boss.center_x, boss.center_y)
                        boss.remove_from_sprite_lists()
                        self.score += 200
                        self.boss_spawned = False

        # Spieler trifft normale Gegner / Boss
        if arcade.check_for_collision_with_list(self.player, self.enemies) or arcade.check_for_collision_with_list(self.player, self.bosses):
            self.player_lives -= 1
            print("Spieler getroffen! Leben:", self.player_lives)
            if self.player_lives <= 0:
                print("Game over")
                arcade.close_window()

        # Gegner / Boss schießen
        self.enemy_shoot_timer += dt
        self.boss_shoot_timer += dt

        if self.enemy_shoot_timer > 3.0:  # alle 3 Sekunden
            self.enemy_shoot_timer = 0
            for enemy in self.enemies:
                bullet = arcade.SpriteCircle(5, arcade.color.RED)
                bullet.center_x = enemy.center_x
                bullet.center_y = enemy.center_y
                bullet.change_x = self.enemy_bullet_speed #--------------------------------------------------------------------
                self.enemy_bullets.append(bullet)

        if self.boss_shoot_timer > 1.0:  # alle 1 Sekunde
            self.boss_shoot_timer = 0
            for boss in self.bosses:
                bullet = arcade.SpriteCircle(8, arcade.color.RED)
                bullet.center_x = boss.center_x
                bullet.center_y = boss.center_y
                bullet.change_x = -5
                self.boss_bullets.append(bullet)

        # Gegner- und Bosskugeln treffen Spieler
        for bullet in list(self.enemy_bullets) + list(self.boss_bullets):
            if arcade.check_for_collision(self.player, bullet):
                bullet.remove_from_sprite_lists()
                self.player_lives -= 1
                print("Spieler getroffen! Leben:", self.player_lives)
                if self.player_lives <= 0:
                    print("Game over")
                    arcade.close_window()

        # Kugeln entfernen, wenn sie aus dem Bildschirm rausgehen
        for bullet_list in [self.bullets, self.enemy_bullets, self.boss_bullets]:
            for bullet in list(bullet_list):
                if bullet.right < 0 or bullet.left > WINDOW_WIDTH or bullet.bottom > WINDOW_HEIGHT or bullet.top < 0:
                    bullet.remove_from_sprite_lists()

        # Explosionen Timer
        for explosion in list(self.explosions):
            explosion.timer -= 1
            if explosion.timer <= 0:
                explosion.remove_from_sprite_lists()

        # Boss spawn nach Score
        if self.score == 500 and not self.boss_spawned:
            self.spawn_boss()
            self.boss_spawned = True

        ## Gegner schneller machen 
        if self.score == 1000:
            self.enemy_speed = 4
            self.enemy_bullet_speed = -6

        if self.score == 1500:
            self.enemy_speed = 6
            self.enemy_bullet_speed = -8

        if self.score == 2000:
            self.enemy_speed = 8
            self.enemy_bullet_speed = -10  

        if self.score == 2500:
            self.enemy_speed = 10
            self.enemy_bullet_speed = -12

        if self.score == 3000:
            self.enemy_speed = 12
            self.enemy_bullet_speed = -14 



        # GameOver!!
        for enemy in list(self.enemies):
            if enemy.right < 0:
                enemy.remove_from_sprite_lists()
        for boss in list(self.bosses):
            if boss.right <= 0:
                self.create_explosion(boss.center_x, boss.center_y)
                boss.remove_from_sprite_lists()
                self.boss_defeated = True
       
        for enemy in list(self.enemies):
            if enemy.left <= 0:
                arcade.close_window()
        for boss in list(self.bosses):
            if boss.left <= 0:
                arcade.close_window()


    def on_draw(self):
        self.clear()
        self.background_list.draw()   
        self.player_list.draw()
        self.bullets.draw()
        self.enemies.draw()
        self.bosses.draw()
        self.enemy_bullets.draw()
        self.boss_bullets.draw()
        self.explosions.draw()
         

        arcade.draw_text(f"Score: {self.score}", 20, WINDOW_HEIGHT - 40, arcade.color.WHITE, 20)
        arcade.draw_text(f"Leben: {self.player_lives}", 20, WINDOW_HEIGHT - 70, arcade.color.WHITE, 20)


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

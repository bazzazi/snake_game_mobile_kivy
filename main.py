from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint


class SnakePart(Widget):
    pass


class GameScreen(Widget):
    step_size = 40
    snake_part = []
    move_x = 0
    move_y = 0
    score = 0

    def new_game(self):
        remove_list = []
        for child in self.children:
            if isinstance(child, SnakePart):
                remove_list.append(child)
        for child in remove_list:
            self.remove_widget(child)
        self.snake_part = []
        self.score = 0
        self.ids.score_label.text = "Score: " + str(self.score)
        head = SnakePart()
        self.snake_part.append(head)
        self.move_x = 0
        self.move_y = 0
        self.add_widget(head)

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            # move right or left
            self.move_y = 0
            if dx > 0:
                # move right
                self.move_x = self.step_size
            else:
                # move left
                self.move_x = - self.step_size
        else:
            # move up or down
            self.move_x = 0
            if dy > 0:
                # move up
                self.move_y = self.step_size
            else:
                # move down
                self.move_y = - self.step_size

    def check_cliding(self, wid1, wid2):
        if wid1.x >= wid2.right:
            return 0
        if wid2.x >= wid1.right:
            return 0
        if wid1.y >= wid2.top:
            return 0
        if wid2.y >= wid1.top:
            return 0
        return 1

    def frame(self, *args):
        food = self.ids.food
        last_x = self.snake_part[-1].x
        last_y = self.snake_part[-1].y
        # move body
        for i, part in enumerate(self.snake_part):
            if i == 0:
                continue
            part.new_x = self.snake_part[i - 1].x
            part.new_y = self.snake_part[i - 1].y
        for part in self.snake_part[1:]:
            part.x = part.new_x
            part.y = part.new_y
        # move head
        head = self.snake_part[0]
        head.x += self.move_x
        head.y += self.move_y
        # check cliding to food
        if self.check_cliding(head, food):
            self.score += 1
            self.ids.score_label.text = "Score: " + str(self.score)
            food.x = randint(0, Window.width - food.width)
            food.y = randint(0, Window.height - food.height)
            new_part = SnakePart()
            new_part.x = last_x
            new_part.y = last_y
            self.snake_part.append(new_part)
            self.add_widget(new_part)
        # check cliding to wall
        if not self.check_cliding(self, head):
            self.new_game()
        # check cliding to snake
        for part in self.snake_part[1:]:
            if self.check_cliding(head, part):
                self.new_game()


class mainApp(App):
    def on_start(self):
        self.root.new_game()
        Clock.schedule_interval(self.root.frame, 0.25)


if __name__ == "__main__":
    mainApp().run()

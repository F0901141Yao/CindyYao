import tkinter as tk
import random

# 遊戲參數
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SPEED = 150  # 移動速度 (ms)

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("貪食蛇 - Tkinter 版")

        self.canvas = tk.Canvas(master, width=GRID_SIZE * GRID_WIDTH, height=GRID_SIZE * GRID_HEIGHT, bg="black")
        self.canvas.pack()

        self.score = 0
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = self.create_food()
        self.direction = "Right"
        self.running = True

        self.master.bind("<Key>", self.on_key_press)
        self.update()

    def create_food(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def draw(self):
        self.canvas.delete("all")
        # 畫食物
        x, y = self.food
        self.draw_rect(x, y, "red")

        # 畫蛇
        for x, y in self.snake:
            self.draw_rect(x, y, "lime")

        # 顯示分數
        self.canvas.create_text(60, 10, fill="white", font="Arial 14 bold", text=f"分數: {self.score}", anchor="nw")

    def draw_rect(self, x, y, color):
        x1 = x * GRID_SIZE
        y1 = y * GRID_SIZE
        x2 = x1 + GRID_SIZE
        y2 = y1 + GRID_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def move(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1

        new_head = (head_x, head_y)

        # 撞牆或自撞結束遊戲
        if (
            head_x < 0 or head_x >= GRID_WIDTH or
            head_y < 0 or head_y >= GRID_HEIGHT or
            new_head in self.snake
        ):
            self.running = False
            self.canvas.create_text(GRID_SIZE * GRID_WIDTH // 2, GRID_SIZE * GRID_HEIGHT // 2,
                                    text="遊戲結束！", fill="red", font="Arial 24 bold")
            return

        self.snake.insert(0, new_head)

        # 吃到食物
        if new_head == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()  # 沒吃到就移除尾巴

    def update(self):
        if self.running:
            self.move()
            self.draw()
            self.master.after(SPEED, self.update)

    def on_key_press(self, event):
        key = event.keysym
        # 避免 180 度掉頭
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if key in opposites and self.direction != opposites[key]:
            self.direction = key

# 啟動遊戲
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()

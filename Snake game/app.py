import tkinter as tk
from random import randint
from PIL import Image, ImageTk

MOVE_INCREMENT = 20 # move by 20px
moves_per_second = 10
GAME_SPEED = 1000 // moves_per_second


# Create snake class (inherit from canvas)
class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)

        # contains x,y positions of snakes body parts
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = "Right" # starting direction
        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()
        self.create_objects()
        self.after(GAME_SPEED, self.perform_actions)

        self.pack()
    
    # Load images
    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            root.destroy()
            raise
    
    
    
    def create_objects(self):
        self.create_text(100, 12, text=f"Score: {self.score} (speed: {moves_per_second})", tag="score", fill="#fff", font=10)
        # Create snake body elements
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")

        # Create food elem get food position x & y
        self.create_image(*self.food_position, image=self.food, tag="food")
        # Create game board boundary
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")


    def move_snake(self):
        # Set starting position of snake's head (rightmost)
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        # Move snake (add new head and cut last body elements position)
        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        # Find all elements with tag 'snake' and their positions, zip them and use in self.coords() to change image position
        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            # canvas method coords(current coords, new coords)
            self.coords(segment, position)

    
    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]
        # Returns true if head collides with the edge of the board and the rest of a body (snake_positions[1:])
        return (
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snake_positions[1:]
        )


    # Generat new food, update score and game spped and append new elem. to snake's body
    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            # Increase game speed every 10 points
            if self.score % 10 == 0:
                global moves_per_second
                moves_per_second += 1

            # Append new position to the end of snake's body and create image for a new element
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")
            # Update food position variable and and mark new "food" cell 
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)
            # Find and update score cell 
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (speed: {moves_per_second})", tag="score")



    # Generate new food position (different than current positions of snake's body)
    def set_new_food_position(self):
    # Numbers passed to randint are based on dimensions of a a game screen ( * 20(px) : width/height of a snake elements)
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position



    # Change self.direction
    def on_key_press(self, e):
        new_direction = e.keysym
        
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})
        # Set new direction if user pressed one of the arrows keys, and new direction isn't oposite to a current one (u,d) or (l,r)
        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction



    def perform_actions(self):
        if self.check_collisions():
            self.end_game()

        self.check_food_collision()

        self.move_snake()
        # .after calls function after given time (time, callback)
        self.after(GAME_SPEED, self.perform_actions)



    # Clear canvas and display message in the center of a screen
    def end_game(self):
        self.delete(tk.ALL)
        self.create_text( self.winfo_width() / 2,self.winfo_height() / 2,
            text=f"Game over! Your score: {self.score}!", fill="#fff", font=14)



root = tk.Tk()
root.title("Snake")
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)

board = Snake()


root.mainloop()
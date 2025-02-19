# Kivy App for Tetris made in Python
# Step 1: Basic Structure

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

Window.size = (400, 600)

class TetrisGame(Widget):
    pass

class TetrisApp(App):
    def build(self):
        return TetrisGame()

if __name__ == '__main__':
    TetrisApp().run()

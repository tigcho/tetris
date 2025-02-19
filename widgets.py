from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

CELL_SIZE = 20

class BoardWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            for row in range(len(self.game.board)):
                for col in range(len(self.game.board[0])):
                    if self.game.board[row][col]:
                        Color(1, 1, 1)
                    else:
                        Color(0, 0, 0)
                    x = self.x + col * CELL_SIZE
                    y = self.y + row * CELL_SIZE
                    Rectangle(pos=(x, y), size=(CELL_SIZE, CELL_SIZE))

class PiecePreviewWidget(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.piece = piece
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0)
            for (x, y) in self.piece['coords']:
                Rectangle(pos=(self.x + x * CELL_SIZE, self.y + y * CELL_SIZE), size=(CELL_SIZE, CELL_SIZE))

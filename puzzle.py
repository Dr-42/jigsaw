import random
import PIL
import PIL.Image
import PIL.ImageDraw



# PuzzlePieceSide enum
def PuzzlePieceSide(enum):
    switch = {
        0: "in",
        1: "out",
        2: "none",
    }
    return switch.get(enum, "Invalid enum")


# PuzzlePiece class
class PuzzlePiece:
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def __str__(self):
        s = "t: " + PuzzlePieceSide(self.top) + ", right: " + PuzzlePieceSide(self.right) + ", bottom: " + PuzzlePieceSide(self.bottom) + ", left: " + PuzzlePieceSide(self.left)
        return s


# Puzzle class
class Puzzle:
    def __init__(self, width, height, image=None, piece_side_images=None):
        self.width = width
        self.height = height
        self.pieces = []
        self.image = image
        if piece_side_images is None:
            self.piece_side_images = {
                1: "images/top_out.png",
                # 2: "images/right_out.png",
                # 3: "images/bottom_out.png",
                # 4: "images/left_out.png",
                5: "images/none.png",
            }
        else:
            self.piece_side_images = piece_side_images

    def blank(self):
        for _ in range(self.width * self.height):
            self.pieces.append(PuzzlePiece(2, 2, 2, 2))

    def generate(self):
        for i in range(self.width * self.height):
            if (i % self.width == 0):
                self.pieces[i].left = 2
            else:
                is_1_or_0 = random.randint(0, 1)
                self.pieces[i].left = is_1_or_0
                if (is_1_or_0 == 1):
                    self.pieces[i - 1].right = 0
                elif (is_1_or_0 == 0):
                    self.pieces[i - 1].right = 1

            if (i < self.width):
                self.pieces[i].top = 2
            else:
                is_1_or_0 = random.randint(0, 1)
                self.pieces[i].top = is_1_or_0
                if (is_1_or_0 == 1):
                    self.pieces[i - self.width].bottom = 0
                elif (is_1_or_0 == 0):
                    self.pieces[i - self.width].bottom = 1

            if (i % self.width == self.width - 1):
                self.pieces[i].right = 2
            else:
                is_1_or_0 = random.randint(0, 1)
                self.pieces[i].right = is_1_or_0
                if (is_1_or_0 == 1):
                    self.pieces[i + 1].left = 0
                elif (is_1_or_0 == 0):
                    self.pieces[i + 1].left = 1

            if (i >= self.width * (self.height - 1)):
                self.pieces[i].bottom = 2
            else:
                is_1_or_0 = random.randint(0, 1)
                self.pieces[i].bottom = is_1_or_0
                if (is_1_or_0 == 1):
                    self.pieces[i + self.width].top = 0
                elif (is_1_or_0 == 0):
                    self.pieces[i + self.width].top = 1

    def print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.pieces[i * self.width + j], end=" ")
            print()

    def print_image(self):
        # Create a new image

        new_image = PIL.Image.new("RGBA", (self.width * 100, self.height * 100), (0, 0, 0, 0))

        # Add the image to the new image
        if self.image is not None:
            image = PIL.Image.open(self.image)
            image = image.resize((self.width * 100, self.height * 100))
            new_image.paste(image, (0, 0))

        for i in range(self.height):
            for j in range(self.width):

                active = self.pieces[i * self.width + j]
                if active.top == 1:
                    top_image = PIL.Image.open(self.piece_side_images[1])
                else:
                    top_image = PIL.Image.open(self.piece_side_images[5])

                if active.right == 1:
                    right_image = PIL.Image.open(self.piece_side_images[1])
                    right_image = right_image.rotate(270)
                else:
                    right_image = PIL.Image.open(self.piece_side_images[5])

                if active.bottom == 1:
                    bottom_image = PIL.Image.open(self.piece_side_images[1])
                    bottom_image = bottom_image.rotate(180)
                else:
                    bottom_image = PIL.Image.open(self.piece_side_images[5])

                if active.left == 1:
                    left_image = PIL.Image.open(self.piece_side_images[1])
                    left_image = left_image.rotate(90)
                else:
                    left_image = PIL.Image.open(self.piece_side_images[5])


                #   Add the side image to the new image
                new_image.paste(top_image, (j * 100, i * 100), top_image)
                new_image.paste(right_image, (j * 100, i * 100), right_image)
                new_image.paste(bottom_image, (j * 100, i * 100), bottom_image)
                new_image.paste(left_image, (j * 100, i * 100), left_image)

        # Save the image
        new_image.save("images/puzzle.png")


# Main
if __name__ == "__main__":
    print("Puzzle")
    print("------")

    image = input("Image path: ")
    cols = int(input("Columns: "))
    rows = int(input("Rows: "))

    puzzle = Puzzle(cols, rows, image)
    puzzle.blank()
    puzzle.generate()
    puzzle.print_image()

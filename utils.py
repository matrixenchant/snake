import pygame
from os import sep

# Images
_image_library = {}
def get_image(path):
        global _image_library
        img = _image_library.get(path)
        if img == None:
                canonicalized_path = path.replace('/', sep).replace('\\', sep)
                img = pygame.image.load(canonicalized_path).convert_alpha()
                _image_library[path] = img
        return img


def checkInSnake(parts, radius = 15, x = -1, y = -1):
        for p_x, p_y in parts:
                if x != -1:
                        if p_x - radius < x and x < p_x + radius:
                                return True
                if y != -1:
                        if p_y - radius < y and y < p_y + radius:
                                return True
        return False


from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Error")
    return db


COLOR_ACTIVE = (255, 241, 117)
COLOR_INACTIVE = (255, 246, 169)
class InputBox:
    def __init__(self, x, y, w, h, font, fontColor, text='', maxSymbols = 0, outline = True):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = fontColor
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.font = font
        self.maxSymbols = maxSymbols
        self.outline = outline

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            #self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.maxSymbols != 0 and len(self.text) >= self.maxSymbols: return
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        #width = max(200, self.txt_surface.get_width()+10)
        #self.rect.w = width
        pass

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+25, self.rect.y+18))
        # Blit the rect.
        if self.outline:
            pygame.draw.rect(screen, self.color, self.rect, 2)


class AnimatedObject:
    def __init__(self, x, y, path, framesNumber, speed, loop = False):
        self.x = x
        self.y = y
        self.path = path
        self.speed = speed
        self.frames = []
        self.active_frame = 1
        self.loop = loop
        self.isReverse = False

        for i in range(1, framesNumber+1):
            frame = get_image(f"assets/{path}/{i}.png")
            self.frames.append(frame)

    def update(self, screen):

        if self.loop:
            if self.isReverse: self.active_frame -= 1 / self.speed
            else: self.active_frame += 1 / self.speed

            if (int(self.active_frame) < 1):
                self.isReverse = False
                self.active_frame = 1

            if (int(self.active_frame) > len(self.frames)):
                self.isReverse = True
                self.active_frame = len(self.frames)

            print(self.isReverse, int(self.active_frame))

        else:
            self.active_frame += 1 / self.speed
            if (int(self.active_frame) > len(self.frames)):
                self.active_frame = 1

        screen.blit(self.frames[int(self.active_frame) - 1], (self.x, self.y))
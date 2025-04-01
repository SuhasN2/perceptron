import pygame


class Object():
    def __init__(self, screen,rect, color):

        self.screen = screen
        self.color = color

        self.rect = rect
        self.draw

    def draw(self):
        """
        Draw the object on the screen.
        """
        pygame.draw.rect(self.screen, self.color, self.rect)

class Button(Object):
    def __init__(self, screen, rect, text, font_size, font_color, bg_color, hover_bg_color, click_bg_color):
        self.text = text
        self.font_size = font_size
        self.font_color = font_color

        self.bg_colors = [bg_color, hover_bg_color, click_bg_color]
        self.bg_color = bg_color  # default background color when not hovered or clicked

        self.screen = screen
        self.rect = rect
        self.hovered = False
        self.clicked = False

        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.rect.x + self.rect.width// 2, self.rect.y + self.rect.height // 2))

    def DrawAndUpdate(self, func=None):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        mouse_down = pygame.mouse.get_pressed(3)[0]

        if self.hovered and mouse_down and not self.clicked:  # Check for initial click
            self.clicked = True
            self.bg_color = self.bg_colors[2] # set color on click

            if func:
                func()

        elif not mouse_down: # Reset only on release
            self.clicked = False
            if self.hovered:
                self.bg_color = self.bg_colors[1]
            else:
                self.bg_color = self.bg_colors[0]

        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)
            


class Dropdown(Object):
    def __init__(self, screen, rect, options, font_size, font_color, bg_color, hover_bg_color, click_bg_color):
        super().__init__(screen, rect ,bg_color)

        self.options = options

        self.font_size = font_size
        self.font_color = font_color

        self.bg_colors = [bg_color, hover_bg_color, click_bg_color]

        self.rect = rect

        self.hovered = False
        self.clicked = False
        self.open = False  # Initially closed
        self.selected_option = None  # No option selected initially

        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)

        self.option_rects = []
          # Store rects for each option
        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, self.font_color)
            text_rect = text_surface.get_rect(topleft=(self.rect.x, self.rect.y + (i+1) * self.rect.height))  # Position below main rect
            self.option_rects.append(text_rect)

    def DrawAndUpdate(self):
        self.hovered = self.rect.colliderect(pygame.Rect(*pygame.mouse.get_pos(), 1, 1))
        mouse_down = pygame.mouse.get_pressed(3)[0]

        if self.hovered and mouse_down and not self.clicked:
            self.clicked = True
            self.open = not self.open  # Toggle dropdown open/close

        elif not mouse_down:
            self.clicked = False

        self.bg_color = self.bg_colors[1] if self.hovered else self.bg_colors[0]
        self.draw() # Draw the main rect

        text_surface = self.font.render(self.selected_option if self.selected_option else "Select", True, self.font_color) # display selected option or 'select'
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

        if self.open:
            for i, option in enumerate(self.options):
                option_rect = self.option_rects[i]
                option_hovered = option_rect.colliderect(pygame.Rect(*pygame.mouse.get_pos(), 1, 1))

                option_bg_color = self.bg_colors[1] if option_hovered else self.bg_colors[0]
                pygame.draw.rect(self.screen, option_bg_color, option_rect) # draw option rects
                text_surface = self.font.render(option, True, self.font_color)
                text_rect = text_surface.get_rect(center=option_rect.center)
                self.screen.blit(text_surface, text_rect)

                if option_hovered and mouse_down and not self.clicked: # select option
                    self.clicked = True
                    self.selected_option = option
                    self.open = False 

class Text(Object):
    ...

class Toggle(Object):
    def __init__(self, screen, rect, text, font_size, font_color, bg_color, hover_bg_color, click_bg_color, checked_bg_color):
        super().__init__(screen, rect, bg_color)

        self.text = text
        self.font_size = font_size
        self.font_color = font_color

        self.bg_colors = [bg_color, hover_bg_color, click_bg_color, checked_bg_color]

        self.rect = rect

        self.hovered = False
        self.clicked = False
        self.checked = False  # Initially unchecked

        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)

        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.rect.x + self.rect.width// 2, self.rect.y + self.rect.height // 2))
    
    def DrawAndUpdate(self):
        self.hovered = self.rect.colliderect(pygame.Rect(*pygame.mouse.get_pos(), 1, 1))
        mouse_down = pygame.mouse.get_pressed(3)[0]

        if self.hovered and mouse_down and not self.clicked:
            self.clicked = True
            self.checked = not self.checked  # Toggle checkbox

        elif not mouse_down:
            self.clicked = False

        self.bg_color = self.bg_colors[1] if self.hovered else self.bg_colors[0]
        if self.checked:
            self.bg_color = self.bg_colors[3]
        pygame.draw.rect(self.screen, self.bg_color, self.rect)

        text_surface = self.font.render(self.text + (" [X]" if self.checked else " [  ]"), True, self.font_color) # display checkbox text
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)


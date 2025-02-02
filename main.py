# Importing Dependencies
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math
from typing import Callable, List, Tuple


# For making Shapes
class Shape:
    def __init__(self, shape_type: str, color: Tuple[float, float, float], **kwargs):
        self.shape_type = shape_type
        self.color = color
        self.parameters = kwargs

    def draw(self):
        if self.shape_type == "circle":
            self.draw_circle()
        elif self.shape_type == "rectangle":
            self.draw_rectangle()
        elif self.shape_type == "line":
            self.draw_line()
        elif self.shape_type == "ellipse":
            self.draw_ellipse()
        else:
            print(f"Unknown shape type: {self.shape_type}.\n Currently supported: circle, rectangle, line, ellipse")

    def draw_circle(self):
        glColor3f(*self.color)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            theta = 2.0 * math.pi * float(i) / 100.0
            x = self.parameters["radius"] * math.cos(theta) + self.parameters["center_x"]
            y = self.parameters["radius"] * math.sin(theta) + self.parameters["center_y"]
            glVertex2f(x, y)
        glEnd()

    def draw_ellipse(self):
        glColor3f(*self.color)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            theta = 2.0 * math.pi * float(i) / 100.0
            x = self.parameters["radius_x"] * math.cos(theta) + self.parameters["center_x"]
            y = self.parameters["radius_y"] * math.sin(theta) + self.parameters["center_y"]
            glVertex2f(x, y)
        glEnd()

    def draw_rectangle(self):
        glColor3f(*self.color)
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.parameters["x1"], self.parameters["y1"])
        glVertex2f(self.parameters["x2"], self.parameters["y1"])
        glVertex2f(self.parameters["x2"], self.parameters["y2"])
        glVertex2f(self.parameters["x1"], self.parameters["y2"])
        glEnd()

    def draw_line(self):
        glColor3f(*self.color)
        glBegin(GL_LINES)
        glVertex2f(self.parameters["x1"], self.parameters["y1"])
        glVertex2f(self.parameters["x2"], self.parameters["y2"])
        glEnd()


# For Graphing Equations
class EquationGrapher:
    def __init__(self, width=800, height=600):
        # Initialize pygame and OpenGL
        pygame.init()
        display_info = pygame.display.Info()
        self.width = int(display_info.current_w * 0.9)
        self.height = int(display_info.current_h * 0.9)
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL | RESIZABLE)
        pygame.display.set_caption("Dynamic Equation Grapher")
        
        # Initialize Pygame font
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 14)
        
        # View settings
        self.zoom = 10.0
        self.x_offset = 0.0
        self.y_offset = 0.0
        
        # Input box settings
        self.input_text = ""
        self.input_active = True
        self.input_rect = pygame.Rect(10, self.height - 40, 200, 30)
        
        # Equation storage with colors and visibility
        self.equations = []  # List of tuples (function, color, equation_string, visible)
        
        # Shape storage
        self.shapes = []  # List of Shape objects
        
        # Checkbox settings
        self.checkboxes = []  # List of pygame.Rect objects for checkboxes
        
        # Available colors for equations and shapes
        self.colors = [
            (0, 0, 0),      # Black
            (1, 0, 0),      # Red
            (0, 0, 1),      # Blue
            (0, 0.5, 0),    # Green
            (0.5, 0, 0.5),  # Purple
            (1, 0.5, 0),    # Orange
        ]
        
        # Set white background
        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        # Enable line smoothing
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Initialize the coordinate system
        self.setup_viewport(self.width, self.height)

        self.message = ""
        self.message_time = 0
        self.message_duration = 5000  # Default duration for messages

        # Display the message when the code is first run
        self.show_about()
        self.show_help()

    def setup_viewport(self, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        self.reset_projection()
        # Update checkbox positions
        self.update_checkboxes()

    def update_checkboxes(self):
        self.checkboxes = []
        for i in range(len(self.equations)):
            checkbox_rect = pygame.Rect(self.width - 220, 20 + i * 20, 12, 12)
            self.checkboxes.append(checkbox_rect)

    def reset_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = self.width / self.height
        if aspect_ratio > 1:
            gluOrtho2D(-self.zoom * aspect_ratio + self.x_offset, 
                       self.zoom * aspect_ratio + self.x_offset, 
                       -self.zoom + self.y_offset, 
                       self.zoom + self.y_offset)
        else:
            gluOrtho2D(-self.zoom + self.x_offset, 
                       self.zoom + self.x_offset, 
                       -self.zoom / aspect_ratio + self.y_offset, 
                       self.zoom / aspect_ratio + self.y_offset)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw_text_on_screen(self, text, x, y, color=(0, 0, 0, 1)):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.width, self.height, 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        text_surface = self.font.render(str(text), True, color[:3])
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glRasterPos2i(x, y)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def draw_number_on_graph(self, num, x, y):
        aspect_ratio = self.width / self.height
        if aspect_ratio > 1:
            screen_x = self.width * (x - (-self.zoom * aspect_ratio + self.x_offset)) / (2 * self.zoom * aspect_ratio)
            screen_y = self.height * (1 - (y - (-self.zoom + self.y_offset)) / (2 * self.zoom))
        else:
            screen_x = self.width * (x - (-self.zoom + self.x_offset)) / (2 * self.zoom)
            screen_y = self.height * (1 - (y - (-self.zoom / aspect_ratio + self.y_offset)) / (2 * self.zoom / aspect_ratio))
        self.draw_text_on_screen(f"{num:.1f}", int(screen_x), int(screen_y), color=(0.9, 0.9, 0.9, 0.5))  # Very light grey with 50% opacity

    def draw_grid(self):
        # Calculate grid spacing based on zoom level
        grid_spacing = 10 ** math.floor(math.log10(self.zoom / 5))
        
        # Calculate visible range
        aspect_ratio = self.width / self.height
        if aspect_ratio > 1:
            x_min = int((-self.zoom * aspect_ratio + self.x_offset) / grid_spacing) * grid_spacing
            x_max = int((self.zoom * aspect_ratio + self.x_offset) / grid_spacing + 1) * grid_spacing
            y_min = int((-self.zoom + self.y_offset) / grid_spacing) * grid_spacing
            y_max = int((self.zoom + self.y_offset) / grid_spacing + 1) * grid_spacing
        else:
            x_min = int((-self.zoom + self.x_offset) / grid_spacing) * grid_spacing
            x_max = int((self.zoom + self.x_offset) / grid_spacing + 1) * grid_spacing
            y_min = int((-self.zoom / aspect_ratio + self.y_offset) / grid_spacing) * grid_spacing
            y_max = int((self.zoom / aspect_ratio + self.y_offset) / grid_spacing + 1) * grid_spacing
        
        # Draw vertical grid lines
        for x in np.arange(x_min, x_max + grid_spacing, grid_spacing):
            if abs(x) < 1e-10:  # X-axis
                glLineWidth(2.0)
                glColor3f(0.0, 0.0, 0.5)  # Dark blue for main axis
            else:
                glLineWidth(1.0)
                glColor3f(0.8, 0.8, 0.8)  # Light gray for grid
            
            glBegin(GL_LINES)
            glVertex2f(x, y_min)
            glVertex2f(x, y_max)
            glEnd()
            
            if x != 0:
                self.draw_number_on_graph(x, x, 0.3)
        
        # Draw horizontal grid lines
        for y in np.arange(y_min, y_max + grid_spacing, grid_spacing):
            if abs(y) < 1e-10:  # Y-axis
                glLineWidth(2.0)
                glColor3f(0.0, 0.0, 0.5)  # Dark blue for main axis
            else:
                glLineWidth(1.0)
                glColor3f(0.8, 0.8, 0.8)  # Light gray for grid
            
            glBegin(GL_LINES)
            glVertex2f(x_min, y)
            glVertex2f(x_max, y)
            glEnd()
            
            if y != 0:
                self.draw_number_on_graph(y, 0.3, y)

    def create_safe_function(self, expression: str) -> Callable[[float], float]:
        """Creates a safe function from a string expression"""
        # Define safe mathematical functions
        safe_dict = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'pi': math.pi,
            'e': math.e,
            'abs': abs,
            'pow': pow
        }

        def safe_eval(x):
            try:
                # Create a safe local namespace with only x and math functions
                local_dict = safe_dict.copy()
                local_dict['x'] = x
                # Evaluate the expression
                return eval(expression, {"__builtins__": {}}, local_dict)
            except Exception as e:
                return None

        return safe_eval

    def parse_equation(self, equation_str: str) -> Callable[[float], float]:
        """Parse equation string into a safe function"""
        try:
            # Clean up the equation string
            equation_str = equation_str.strip().replace('^', '**')
            if 'y' in equation_str and 'x' in equation_str:
                # Convert equation to y = f(x) form
                lhs, rhs = equation_str.split('=')
                lhs = lhs.strip()
                rhs = rhs.strip()
                if lhs == 'y':
                    return self.create_safe_function(rhs)
                elif rhs == 'y':
                    return self.create_safe_function(lhs)
                else:
                    self.show_message("Failed to process equation, press help for instructions", False)
                    return None
            elif 'x' in equation_str:
                return self.create_safe_function(equation_str)
            else:
                self.show_message("Failed to process equation, press help for instructions", False)
                return None
        except Exception as e:
            print(f"Error parsing equation: {e}")
            self.show_message("Failed to process equation, press help for instructions", False)
            return None

    def plot_equation(self, equation_func: Callable[[float], float], color):
        if equation_func is None:
            return
            
        glLineWidth(2.0)
        glColor3f(*color)
        
        # Adjust number of points based on zoom level
        num_points = max(1000, int(2000 * self.zoom / 10))
        step = (2 * self.zoom) / num_points
        x_start = -self.zoom + self.x_offset
        
        points = []
        current_strip = []
        
        for i in range(num_points + 1):
            x = x_start + (i * step)
            try:
                y = equation_func(x)
                if y is not None and isinstance(y, (int, float)) and abs(y) < self.zoom * 10:
                    current_strip.append((x, y))
                else:
                    if current_strip:
                        points.append(current_strip)
                        current_strip = []
            except Exception:
                if current_strip:
                    points.append(current_strip)
                    current_strip = []
        
        if current_strip:
            points.append(current_strip)
        
        # Draw all collected strips
        for strip in points:
            if len(strip) > 1:
                glBegin(GL_LINE_STRIP)
                for x, y in strip:
                    glVertex2f(x, y)
                glEnd()

    def show_message(self, text, is_success, duration=5000, color=None):
        self.message = text
        self.message_time = pygame.time.get_ticks()
        self.message_duration = duration
        if color:
            self.message_color = color
        else:
            self.message_color = (0, 128, 0) if is_success else (255, 0, 0)  # Darker green for success, red for failure

    def draw_message(self):
        if self.message and pygame.time.get_ticks() - self.message_time < self.message_duration:
            lines = self.message.split('\n')
            for i, line in enumerate(lines):
                self.draw_text_on_screen(line, self.width // 2 - 50, self.height - 30 - (i * 20), self.message_color)
        else:
            self.message = ""

    def show_help(self):
        help_text = (
            "Dynamic Equation Grapher\n"
            "Type equation in the graph window and press Enter to plot\n"
            "Use mouse wheel to zoom, drag to pan\n"
            "Click checkboxes to show/hide equations\n"
            "Press Ctrl+Delete to clear all equations and shapes\n"
            "Example equations: x^2, sin(x), x^3 - 2*x\n"
            "Example shapes: shape:circle:0:0:5, shape:rectangle:-1:-1:1:1, shape:line:-5:0:5:0"
        )
        print(help_text)
        self.show_message(help_text, True, duration=10000, color=(0, 0, 0))  # Black color for help message

    def show_about(self):
        about_text = "Computer Graphics Project by Prabesh Guragain and Phiroj K. Sah"
        print(about_text)
        self.show_message(about_text, True, duration=10000)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.input_text:
                    if self.input_text.lower() == "help":
                        self.show_help()
                    elif self.input_text.lower() == "about":
                        self.show_about()
                    elif self.input_text.startswith("shape:"):
                        self.handle_shape_input(self.input_text)
                        self.show_message("Shape added successfully", True)
                    else:
                        func = self.parse_equation(self.input_text)
                        if func is not None:
                            color = self.colors[len(self.equations) % len(self.colors)]
                            self.equations.append((func, color, self.input_text, True))  # True for visible
                            self.update_checkboxes()
                            self.show_message("Equation added successfully", True)
                        else:
                            self.show_message("Failed to add equation, press help for instructions", False)
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_DELETE and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.equations = []
                    self.shapes = []
                    self.checkboxes = []
                else:
                    if event.unicode.isprintable():
                        self.input_text += event.unicode
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mouse wheel up
                    self.zoom *= 0.9
                    self.reset_projection()
                elif event.button == 5:  # Mouse wheel down
                    self.zoom *= 1.1
                    self.reset_projection()
                elif event.button == 1:  # Left click
                    # Check if click was on a checkbox
                    mouse_pos = pygame.mouse.get_pos()
                    for i, checkbox in enumerate(self.checkboxes):
                        if checkbox.collidepoint(mouse_pos):
                            # Toggle visibility
                            func, color, eq_str, visible = self.equations[i]
                            self.equations[i] = (func, color, eq_str, not visible)
            
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button
                    # Only pan if not clicking checkboxes
                    mouse_pos = pygame.mouse.get_pos()
                    if not any(checkbox.collidepoint(mouse_pos) for checkbox in self.checkboxes):
                        self.x_offset += event.rel[0] * self.zoom / 200
                        self.y_offset -= event.rel[1] * self.zoom / 200
                        self.reset_projection()
            
            elif event.type == pygame.VIDEORESIZE:
                self.setup_viewport(event.w, event.h)
                self.input_rect.y = event.h - 40
        
        return True

    def handle_shape_input(self, shape_input: str):
        try:
            parts = shape_input.split(":")
            shape_type = parts[1]
            color = self.colors[len(self.shapes) % len(self.colors)]
            if shape_type == "circle":
                center_x = float(parts[2])
                center_y = float(parts[3])
                radius = float(parts[4])
                self.shapes.append(Shape("circle", color, center_x=center_x, center_y=center_y, radius=radius))
            elif shape_type == "rectangle":
                x1 = float(parts[2])
                y1 = float(parts[3])
                x2 = float(parts[4])
                y2 = float(parts[5])
                self.shapes.append(Shape("rectangle", color, x1=x1, y1=y1, x2=x2, y2=y2))
            elif shape_type == "line":
                x1 = float(parts[2])
                y1 = float(parts[3])
                x2 = float(parts[4])
                y2 = float(parts[5])
                self.shapes.append(Shape("line", color, x1=x1, y1=y1, x2=x2, y2=y2))
            print(f"Added shape: {shape_input}")
        except Exception as e:
            print(f"Error adding shape: {e}")

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.reset_projection()
        
        # Draw grid and axes
        self.draw_grid()
        
        # Plot visible equations
        for idx, (func, color, eq_str, visible) in enumerate(self.equations):
            if visible:
                self.plot_equation(func, color)
            # Draw equation list and checkboxes
            text_color = tuple(int(c * 255) for c in color)
            self.draw_text_on_screen(f"{eq_str}", 
                                   self.width - 180, 20 + idx * 20, 
                                   text_color)
        
        # Draw shapes
        for shape in self.shapes:
            shape.draw()
        
        # Draw input box and text
        self.draw_text_on_screen("Enter equation: " + self.input_text, 30, self.height - 30)
        
        # Draw message
        self.draw_message()
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.render()
            pygame.time.wait(10)
        
        pygame.quit()

if __name__ == "__main__":
    grapher = EquationGrapher()
    print("Dynamic Equation Grapher")
    print("Type equation in the graph window and press Enter to plot")
    print("Use mouse wheel to zoom, drag to pan")
    print("Click checkboxes to show/hide equations")
    print("Press Ctrl+Delete to clear all equations and shapes")
    print("Example equations: x^2, sin(x), x^3 - 2*x")
    print("Example shapes: shape:circle:0:0:5, shape:rectangle:-1:-1:1:1, shape:line:-5:0:5:0")
    grapher.run()
# Dynamic Equation Grapher

A feature-rich mathematical equation grapher built with Python, PyGame, and OpenGL. This application allows users to visualize mathematical functions, plot basic shapes, and interact with the graph in real-time.

## About

Created by Prabesh Guragain and Phiroj K. Sah as part of a Computer Graphics Project. This grapher combines the power of OpenGL for rendering with PyGame for user interaction to create a responsive and intuitive mathematical visualization tool.

## Features

- **Dynamic Equation Plotting**
  - Plot multiple equations simultaneously
  - Support for basic mathematical functions (sin, cos, tan, exp, sqrt)
  - Real-time visualization
  - Toggle visibility of individual equations

- **Interactive Grid System**
  - Automatic grid scaling based on zoom level
  - Clear axis labeling
  - Dynamic number placement

- **Shape Drawing**
  - Circle
  - Rectangle
  - Line
  - Ellipse

- **Interactive Interface**
  - Zoom in/out with mouse wheel
  - Pan across the graph by dragging
  - Show/hide equations using checkboxes
  - Clear all plots with Ctrl+Delete

- **Multiple Color Support**
  - Automatic color assignment for new equations
  - Different colors for different equations for easy distinction

## Installation Requirements

```bash
pip install pygame
pip install numpy
pip install PyOpenGL
pip install PyOpenGL_accelerate
```

## Usage Instructions

1. **Starting the Application**
   ```python
   python equation_grapher.py
   ```

2. **Plotting Equations**
   - Type your equation in the input box at the bottom
   - Press Enter to plot
   - Equations should be in terms of 'x'
   - Examples:
     ```
     x^2
     sin(x)
     x^3 - 2*x
     2*x + 1
     ```

3. **Drawing Shapes**
   Use the following syntax:
   ```
   shape:type:parameters
   ```
   Examples:
   - Circle: `shape:circle:0:0:5` (center_x:center_y:radius)
   - Rectangle: `shape:rectangle:-1:-1:1:1` (x1:y1:x2:y2)
   - Line: `shape:line:-5:0:5:0` (x1:y1:x2:y2)

4. **Navigation**
   - Zoom: Use mouse wheel
   - Pan: Click and drag with left mouse button
   - Toggle equations: Click checkboxes next to equations
   - Clear all: Press Ctrl+Delete

5. **Special Commands**
   - Type "help" for instructions
   - Type "about" for project information

## Supported Mathematical Functions
- sin(x)
- cos(x)
- tan(x)
- exp(x)
- sqrt(x)
- abs(x)
- pow(x,n)

Constants:
- pi
- e

## Tips
- Use ^ for exponents (e.g., x^2)
- Equations can be written in standard form (y = mx + b)
- For better visibility, equations are plotted with different colors automatically
- Use the checkboxes to compare different equations
- The grid automatically adjusts based on zoom level

## Troubleshooting
1. If an equation doesn't plot:
   - Check syntax (use * for multiplication)
   - Ensure equation is in terms of x
   - Verify mathematical validity

2. If shapes don't appear:
   - Check parameter format
   - Verify coordinates are within visible range
   - Ensure proper syntax with colons

3. If the application runs slowly:
   - Reduce the number of visible equations
   - Close other resource-intensive applications
   - Check if graphics drivers are up to date

## Contributing
Feel free to fork this project and submit pull requests for improvements. Some areas that could be enhanced:
- Additional shape types
- More mathematical functions
- Export/import functionality
- Custom color selection
- Equation history

## License
This project is open source and available under the MIT License.

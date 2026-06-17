# AP Calculus AB Project: Visual Graphing Calculator

## Purpose
The "CALCulator" is a custom graphing calculator designed to visualize the core concepts of AP Calculus AB: the derivative and the definite integral. Instead of just giving the final answer like a standard calculator, it shows the step-by-step geometric limits that define these concepts.

## General Graphing Capabilities
The CALCulator includes several key features designed for ease of use and visual clarity, supported by a surprisingly capable engine under the hood:

*   **Simultaneous Processing:** Instead of calculating a curve one dot at a time, the calculator's math engine evaluates thousands of coordinates simultaneously. This batch processing is what allows the visual sliders to update the graph instantly without lag.
*   **Grid-Based Equation Solving:** For complex equations where $x$ and $y$ are tangled together (like a circle $x^2 + y^2 = 25$), the calculator doesn't attempt to algebraically solve for $y$. Instead, it creates a dense invisible grid across the screen, tests every point, and draws a solid line only where the two sides of the equation perfectly balance each other.
*   **Flexible Equations:** It natively supports standard explicit equations (like $y = \sin(x)$) as well as sideways equations (like $x = y^2$).
*   **Interactive Grid:** You can use your mouse to click and drag the graph to pan around the coordinate plane. You can also use the scroll wheel to zoom in and out. As you move the grid, the calculator instantly redraws the graphs to fit your new viewing window.
*   **Drawing Curves with Points:** A graph on a computer is actually made by connecting many tiny dots. The calculator has a "Points" slider that lets you control how many points are used to draw a curve. If you set it to a low number, the curve will look jagged; if you set it to a high number, it will look perfectly smooth.
*   **Multiple Equations & Virtual Keyboard:** You can graph multiple color-coded equations at once using a built-in virtual keyboard, making it easy to input math symbols without memorizing computer shortcuts.

## Behind the Scenes: Rendering the Graph
The graphing engine acts like a high-speed digital artist, constantly redrawing the screen to keep up with user interactions. Here is how the rendering process works step-by-step:

*   **The Blank Slate:** Every time you type a character, move the graph, or drag a slider, the calculator completely erases the visual canvas. It redraws everything from scratch instantly to reflect the newest changes.
*   **Building the Foundation:** Before any math is drawn, the engine sets up the coordinate system. It takes a standard square chart box, deletes the top and right borders, and moves the left and bottom borders to the center so they cross at zero, creating traditional X and Y axes. A dotted background grid is then drawn over the remaining space.
*   **Dynamic Theming:** The application checks a toggle to see if "Dark Mode" or "Light Mode" is active. It then instantly swaps the background colors (from white to dark gray) and the axis/text colors (from black to white) so the interface is always readable.
*   **Connecting the Dots:** To draw a function like a parabola, the calculator doesn't actually draw a perfect, infinite curve. Instead, it calculates the heights for hundreds of individual points across the screen from left to right. It then draws short, straight lines connecting point A to point B, point B to point C, and so on. Because these points are packed so closely together, the human eye perceives a perfectly smooth curve.

## How it Works: The Derivative
The derivative represents the instantaneous rate of change and the slope of the tangent line. It is defined by the limit of the difference quotient:

$$ f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h} $$

### Secant Line Approximations
When you enter a derivative like `d/dx(f(x))|_a`, the calculator visually demonstrates this limit:
1. It plots your function $f(x)$.
2. It plots a base point at $x = a$.
3. It plots a second point a small distance $h$ away: $x = a + h$.
4. It draws the secant line between these two points and calculates its slope: $\frac{f(a+h) - f(a)}{h}$.

### Interactive Limit Slider
The calculator has a "Deriv Distance (h)" slider. As you slide it to make $h$ smaller (approaching zero), you can watch the secant line pivot closer and closer to the actual tangent line. This physically illustrates the limit $\lim_{h \to 0}$. 

If you want the exact numerical derivative, a "Rounded Numerical Value" toggle switches the calculation to a highly precise formula to give the true analytical answer.

## How it Works: The Integral
The definite integral represents the area under a curve. It is defined by the limit of Riemann sums:

$$ \int_a^b f(x) dx = \lim_{n \to \infty} \sum_{i=1}^{n} f(x_i^*)\Delta x $$

### Riemann Sum Rectangles
When you enter an integral like $\int_a^b(f(x))$, the calculator shows how the area is built:
1. It splits the interval $[a, b]$ into $N$ equal sections.
2. It draws Left Riemann Sum rectangles for each section.
3. It calculates the total area of these rectangles and displays it.

### Interactive Limit Slider
To show the limit definition $\lim_{n \to \infty}$, there is a "Riemann N" slider. You can change the number of rectangles from $N=1$ all the way to $N=1000$. 

As you increase $N$, you see the rectangles become thinner and fit the curve more perfectly. The calculated area gets closer and closer to the true area. 

Turning on the "Rounded Numerical Value" toggle will calculate a massive Riemann sum with 10,000 rectangles in the background, providing an exact area measurement.

## Conclusion
This calculator was built to make calculus visual. By letting users interact with secant lines and Riemann rectangles using sliders, it turns abstract limits into hands-on geometric models.

# MCP (Modular Command Platform) Server

This project implements an MCP server using the `fastmcp` library. It provides a set of tools and resources that can be accessed remotely.

## Overview

The server defines several tools for performing mathematical operations, image manipulation, and interacting with the Microsoft Paint application. It also includes a dynamic greeting resource and example prompts for code review and debugging.

## Requirements

-   Python 3.11
-   `mcp`
-   `PIL` (Pillow)
-   `pywinauto`
-   `pywin32` (if using Windows-specific tools)

You can install the dependencies using pip:

```bash
pip install mcp PIL pywinauto pywin32
```

Or, using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

1.  **Running the Server:**

    To start the MCP server, run the `example_mcp_server.py` script:

    ```bash
    mcp dev example_mcp_server.py
    ```

2.  **Accessing Tools and Resources:**

    Once the server is running, you can access the defined tools and resources remotely using an MCP client.  Refer to the `mcp` documentation for details on how to interact with the server.

## Implemented Tools

The following tools are implemented in the server:

-   **Mathematical Operations:**
    -   `add(a: int, b: int) -> int`: Adds two numbers.
    -   `add_list(l: list) -> int`: Adds all numbers in a list.
    -   `subtract(a: int, b: int) -> int`: Subtracts two numbers.
    -   `multiply(a: int, b: int) -> int`: Multiplies two numbers.
    -   `divide(a: int, b: int) -> float`: Divides two numbers.
    -   `power(a: int, b: int) -> int`: Calculates the power of a number.
    -   `sqrt(a: int) -> float`: Calculates the square root of a number.
    -   `cbrt(a: int) -> float`: Calculates the cube root of a number.
    -   `factorial(a: int) -> int`: Calculates the factorial of a number.
    -   `log(a: int) -> float`: Calculates the logarithm of a number.
    -   `remainder(a: int, b: int) -> int`: Calculates the remainder of a division.
    -   `sin(a: int) -> float`: Calculates the sine of a number.
    -   `cos(a: int) -> float`: Calculates the cosine of a number.
    -   `tan(a: int) -> float`: Calculates the tangent of a number.
    -   `mine(a: int, b: int) -> int`: A special mining tool (a - b - b).
-   **Image Manipulation:**
    -   `create_thumbnail(image_path: str) -> Image`: Creates a thumbnail from an image.
-   **String Manipulation:**
    -   `strings_to_chars_to_int(string: str) -> list[int]`: Returns the ASCII values of characters in a string.
    -   `int_list_to_exponential_sum(int_list: list) -> float`: Returns the sum of exponentials of numbers in a list.
    -   `fibonacci_numbers(n: int) -> list`: Returns the first n Fibonacci numbers.
-   **Microsoft Paint Interaction (Windows Only):**
    -   `draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict`: Draws a rectangle in Paint from (x1, y1) to (x2, y2).
    -   `draw_rectangle_and_text(text: str) -> dict`: Draws a rectangle and adds text in Paint.
    -   `open_paint() -> dict`: Opens Microsoft Paint maximized on the primary monitor.

## Resources

-   `greeting://{name}`: A dynamic greeting resource that returns a personalized greeting.

## Prompts

The following prompts are defined:

-   `review_code(code: str) -> str`: Prompts for a code review.
-   `debug_error(error: str) -> list[base.Message]`: Prompts for debugging an error.

## Microsoft Paint Tool Dependencies

The Paint tools require `pywinauto` and are designed to work on Windows.  Ensure that Microsoft Paint is installed.  The tools are configured to work with a secondary monitor setup; you may need to adjust the coordinates in the `draw_rectangle` and `draw_rectangle_and_text` tools to suit your environment.

## Troubleshooting

-   **"No module named 'mcp'"**:  Make sure you have installed the `mcp` package: `pip install mcp[cli]`.
-   **`pywinauto` issues**: Ensure you have the correct dependencies installed and that you're running the script on Windows.
-   **Paint tool issues**: Double-check the coordinates used for clicking in the Paint window and adjust them as needed for your screen resolution and Paint version. Use `inspect.exe` to inspect the UI elements.

## License


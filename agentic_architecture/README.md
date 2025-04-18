# Agentic Architecture - Chain of Thought Calculator with Paint Integration

This project implements an agentic architecture that combines mathematical reasoning with Windows Paint integration. It uses a chain-of-thought approach to solve mathematical problems and visualize the results.

## Project Structure

### Core Components

1. **main.py**
   - Entry point of the application
   - Initializes the MCP server and client session
   - Manages the conversation flow between components
   - Integrates with Gemini AI for reasoning
   - Handles tool discovery and system prompt creation

2. **perception.py**
   - Handles interaction with the Gemini AI model
   - Implements timeout mechanisms for AI responses
   - Builds structured prompts for the AI
   - Manages the conversation flow with the AI

3. **decision.py**
   - Processes AI responses and determines next actions
   - Parses function calls and arguments
   - Manages different types of operations (calculation, verification, etc.)
   - Handles final answer verification

4. **memory.py**
   - Maintains conversation history
   - Updates prompts with new information
   - Tracks calculation results and verification steps

5. **action.py**
   - Executes tool calls through the MCP server
   - Acts as an interface between the decision system and tools

### MCP Server Tools (mcp_server.py)

The MCP server provides the following tools:

1. **show_reasoning**
   - Displays step-by-step reasoning for mathematical problems
   - Formats and presents reasoning in a structured way

2. **calculate**
   - Evaluates mathematical expressions
   - Handles Python-based mathematical operations
   - Returns calculation results

3. **verify**
   - Verifies calculation results
   - Compares expected and actual results
   - Provides feedback on correctness

4. **check_consistency**
   - Analyzes calculation steps for consistency
   - Performs multiple checks:
     - Basic calculation verification
     - Dependency analysis
     - Magnitude checks
     - Pattern analysis
     - Result range validation
   - Generates detailed consistency reports

5. **Windows Paint Integration**
   - **open_paint**: Opens Microsoft Paint
   - **draw_rectangle**: Draws rectangles with specified coordinates
   - **add_text_to_paint**: Adds text to the Paint canvas

## Usage Guide

### Prerequisites
- Python 3.x

### Setup
1. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

### Running the Application
1. Start the application:
   ```bash
   uv run main.py
   ```

2. The application will:
   - Initialize the MCP server
   - Connect to the Gemini AI model
   - Present a problem to solve
   - Show step-by-step reasoning
   - Perform calculations
   - Verify results
   - Visualize results in Paint

### Example Problem Format
The application can solve problems like:
```
calculate area triangle with sides 10, 8, 6 cms
Open a Microsoft paint window on the right side of screen, draw a 400x400 pixel size rectangle from 300,300 top left co-ordinate, then write the final result in a textbox
```
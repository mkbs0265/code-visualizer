# Code Visualizer

A web-based application that provides step-by-step visualization of Python code execution, helping developers, students, and educators understand code flow, variable changes, and program logic in an interactive way.

## Features

### Core Functionality
- **Code Editor**: Simple textarea for entering Python code with syntax highlighting
- **File Upload**: Support for uploading `.py` files
- **Step-by-Step Execution**: Visualize code execution line by line
- **Variable Tracking**: See variable values change after each execution step
- **Call Stack Visualization**: Track function calls and execution flow
- **Output Display**: Real-time display of print statements and program output
- **Error Handling**: Comprehensive error display with traceback information

### User Interface
- **Responsive Design**: Works seamlessly on desktop and tablet devices
- **Modern UI**: Clean, intuitive interface with smooth animations
- **Execution Controls**: Play, pause, step forward, and reset functionality
- **Code Highlighting**: Current execution line and executed lines are visually highlighted

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Code Execution**: Python's `sys.settrace` for execution monitoring
- **Security**: Sandboxed execution with restricted imports

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd code-visualizer
   
   # Or simply download and extract the project files
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### Basic Usage

1. **Enter Code**: Type or paste Python code in the code editor
2. **Run Code**: Click the "▶ Run" button to start execution
3. **Step Through**: Use "⏭ Step" to move through execution step by step
4. **Auto-Play**: Use "⏸ Pause" to automatically step through execution
5. **Reset**: Use "🔄 Reset" to return to the beginning

### File Upload

1. Click "📁 Upload .py File" to select a Python file
2. The file content will be loaded into the code editor
3. Click "▶ Run" to execute the uploaded code

### Example Code

The application comes with a pre-loaded example:

```python
def example():
    a = 5
    b = a + 3
    print(b)

example()
```

This demonstrates:
- Variable assignment and modification
- Function definition and calls
- Print statements and output

## Security Features

- **Restricted Imports**: Blocks potentially dangerous modules (os, sys, subprocess)
- **Code Size Limits**: Maximum 10,000 characters per execution
- **Sandboxed Execution**: Code runs in isolated environment
- **Input Validation**: Syntax checking before execution

## Supported Python Features

- Variable assignments and operations
- Function definitions and calls
- Control structures (if/else, loops)
- Basic data types (int, float, string, list, dict)
- Print statements
- Basic arithmetic and logical operations

## Limitations

- **No System Access**: Cannot import system modules or access files
- **Limited Libraries**: Only basic Python built-ins available
- **Execution Time**: Long-running loops may cause timeouts
- **Complex Objects**: Some complex Python objects may not display properly

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Development

### Project Structure
```
code-visualizer/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # CSS styles
│   └── script.js         # Frontend JavaScript
└── README.md             # This file
```

### Adding New Features

1. **Backend**: Modify `app.py` to add new API endpoints
2. **Frontend**: Update `templates/index.html` for new UI elements
3. **Styling**: Add CSS rules in `static/style.css`
4. **Functionality**: Extend JavaScript in `static/script.js`

## Troubleshooting

### Common Issues

**"Module not found" error**
- The application restricts certain imports for security
- Use only basic Python built-ins

**"Code too long" error**
- Reduce code size to under 10,000 characters
- Break large programs into smaller functions

**Execution not working**
- Check Python syntax
- Ensure code doesn't contain infinite loops
- Verify all variables are properly defined

**Browser compatibility issues**
- Update to the latest browser version
- Check browser console for JavaScript errors

## Future Enhancements

- Support for multiple programming languages
- Advanced visualization (flowcharts, AST graphs)
- Save and share execution sessions
- Integration with online IDEs
- Performance profiling and analysis
- Custom execution speed controls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


## Support

For issues, questions, or feature requests, please:
1. Check the troubleshooting section above
2. Review existing issues in the repository
3. Create a new issue with detailed information

---

**Happy Coding! 🚀** 

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import traceback
import io
import contextlib
import ast
import re
from typing import Dict, List, Any
import json

app = Flask(__name__)
CORS(app)

class CodeTracer:
    def __init__(self):
        self.execution_steps = []
        self.current_step = 0
        self.variables = {}
        self.call_stack = []
        self.output = []
        self.error = None
        
    def trace_function(self, frame, event, arg):
        if event == 'line':
            line_no = frame.f_lineno
            filename = frame.f_code.co_filename
            
            # Skip if it's not the main file
            if 'code_visualizer' in filename or '<string>' not in filename:
                return self.trace_function
                
            # Get current variables
            current_vars = {}
            for var_name, var_value in frame.f_locals.items():
                if not var_name.startswith('__'):
                    try:
                        current_vars[var_name] = str(var_value)
                    except:
                        current_vars[var_name] = '<unprintable>'
            
            # Get call stack
            stack = []
            current_frame = frame
            while current_frame:
                if current_frame.f_code.co_name != '<module>':
                    stack.append(current_frame.f_code.co_name)
                current_frame = current_frame.f_back
            
            step = {
                'line': line_no,
                'variables': current_vars.copy(),
                'call_stack': stack[::-1] if stack else ['main'],
                'output': self.output.copy()
            }
            
            self.execution_steps.append(step)
            self.variables = current_vars.copy()
            self.call_stack = stack[::-1] if stack else ['main']
            
        elif event == 'call':
            pass
        elif event == 'return':
            pass
            
        return self.trace_function

    def capture_output(self, func):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            result = func()
            output = new_stdout.getvalue()
            self.output = [line.strip() for line in output.split('\n') if line.strip()]
            return result
        except Exception as e:
            self.error = {
                'type': type(e).__name__,
                'message': str(e),
                'traceback': traceback.format_exc()
            }
            return None
        finally:
            sys.stdout = old_stdout

def execute_code_safely(code: str) -> Dict[str, Any]:
    """Execute Python code safely and return execution steps"""
    
    # Basic security checks
    if any(keyword in code.lower() for keyword in ['import os', 'import sys', 'import subprocess', '__import__', 'eval', 'exec']):
        return {
            'error': {
                'type': 'SecurityError',
                'message': 'Import of system modules and dynamic execution are not allowed for security reasons.',
                'traceback': ''
            }
        }
    
    # Parse code to check for basic syntax
    try:
        ast.parse(code)
    except SyntaxError as e:
        return {
            'error': {
                'type': 'SyntaxError',
                'message': str(e),
                'traceback': ''
            }
        }
    
    # Create tracer
    tracer = CodeTracer()
    
    # Set up tracing
    old_trace = sys.gettrace()
    sys.settrace(tracer.trace_function)
    
    try:
        # Create a restricted builtins dictionary with only safe functions
        safe_builtins = {
            '__builtins__': {
                'print': print,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'reversed': reversed,
                'all': all,
                'any': any,
                'isinstance': isinstance,
                'issubclass': issubclass,
                'hasattr': hasattr,
                'getattr': getattr,
                'setattr': setattr,
                'delattr': delattr,
                'dir': dir,
                'type': type,
                'id': id,
                'hash': hash,
                'repr': repr,
                'ascii': ascii,
                'bin': bin,
                'hex': hex,
                'oct': oct,
                'chr': chr,
                'ord': ord,
                'divmod': divmod,
                'pow': pow,
                'complex': complex,
                'frozenset': frozenset,
                'slice': slice,
                'super': super,
                'property': property,
                'staticmethod': staticmethod,
                'classmethod': classmethod,
                'object': object,
                'BaseException': BaseException,
                'Exception': Exception,
                'TypeError': TypeError,
                'ValueError': ValueError,
                'AttributeError': AttributeError,
                'IndexError': IndexError,
                'KeyError': KeyError,
                'NameError': NameError,
                'ZeroDivisionError': ZeroDivisionError,
                'OverflowError': OverflowError,
                'MemoryError': MemoryError,
                'RecursionError': RecursionError,
                'StopIteration': StopIteration,
                'GeneratorExit': GeneratorExit,
                'SystemExit': SystemExit,
                'KeyboardInterrupt': KeyboardInterrupt,
                'EOFError': EOFError,
                'OSError': OSError,
                'FileNotFoundError': FileNotFoundError,
                'PermissionError': PermissionError,
                'TimeoutError': TimeoutError,
                'ConnectionError': ConnectionError,
                'BlockingIOError': BlockingIOError,
                'ChildProcessError': ChildProcessError,
                'BrokenPipeError': BrokenPipeError,
                'ConnectionAbortedError': ConnectionAbortedError,
                'ConnectionRefusedError': ConnectionRefusedError,
                'ConnectionResetError': ConnectionResetError,
                'FileExistsError': FileExistsError,
                'FileNotFoundError': FileNotFoundError,
                'InterruptedError': InterruptedError,
                'IsADirectoryError': IsADirectoryError,
                'NotADirectoryError': NotADirectoryError,
                'PermissionError': PermissionError,
                'ProcessLookupError': ProcessLookupError,
                'TimeoutError': TimeoutError,
                # 'UnsupportedOperation': UnsupportedOperation,
                'ArithmeticError': ArithmeticError,
                'FloatingPointError': FloatingPointError,
                'AssertionError': AssertionError,
                'BufferError': BufferError,
                'ImportError': ImportError,
                'ModuleNotFoundError': ModuleNotFoundError,
                'LookupError': LookupError,
                'UnboundLocalError': UnboundLocalError,
                'UnicodeError': UnicodeError,
                'UnicodeDecodeError': UnicodeDecodeError,
                'UnicodeEncodeError': UnicodeEncodeError,
                'UnicodeTranslateError': UnicodeTranslateError,
                'RuntimeError': RuntimeError,
                'NotImplementedError': NotImplementedError,
                'ReferenceError': ReferenceError,
                'SyntaxError': SyntaxError,
                'IndentationError': IndentationError,
                'TabError': TabError,
                'SystemError': SystemError,
                'Warning': Warning,
                'UserWarning': UserWarning,
                'DeprecationWarning': DeprecationWarning,
                'PendingDeprecationWarning': PendingDeprecationWarning,
                'SyntaxWarning': SyntaxWarning,
                'RuntimeWarning': RuntimeWarning,
                'FutureWarning': FutureWarning,
                'ImportWarning': ImportWarning,
                'UnicodeWarning': UnicodeWarning,
                'BytesWarning': BytesWarning,
                'ResourceWarning': ResourceWarning
            }
        }
        
        # Execute the code with restricted builtins
        tracer.capture_output(lambda: exec(code, safe_builtins, {}))
        
        if tracer.error:
            return {'error': tracer.error}
        
        return {
            'execution_steps': tracer.execution_steps,
            'final_variables': tracer.variables,
            'final_call_stack': tracer.call_stack,
            'output': tracer.output
        }
        
    except Exception as e:
        return {
            'error': {
                'type': type(e).__name__,
                'message': str(e),
                'traceback': traceback.format_exc()
            }
        }
    finally:
        sys.settrace(old_trace)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code.strip():
            return jsonify({'error': 'No code provided'}), 400
        
        # Limit code size
        if len(code) > 10000:
            return jsonify({'error': 'Code too long. Maximum 10,000 characters allowed.'}), 400
        
        result = execute_code_safely(code)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if not file.filename.endswith('.py'):
            return jsonify({'error': 'Only .py files are allowed'}), 400
            
        # Read file content
        content = file.read().decode('utf-8')
        
        # Limit file size
        if len(content) > 10000:
            return jsonify({'error': 'File too large. Maximum 10,000 characters allowed.'}), 400
        
        return jsonify({'code': content})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
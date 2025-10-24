<div align="center">

# 🚀 Kreggscode GPT

### AI-Powered CLI Assistant for Developers

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/kreggscode/Kreggscode-GPT)

**A beautiful, cross-platform command-line AI assistant for coding, writing, and automation.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [Contributing](#-contributing)

</div>

---

## ✨ Features

- 🎨 **Beautiful CLI Interface** - Professional blue color scheme with clean design
- 🤖 **AI-Powered Conversations** - Natural language interactions with advanced AI
- 🌍 **Multi-Language Support** - Automatically detects and responds in 50+ languages
- 📁 **Smart File Generation** - Creates and saves code files automatically
- 💻 **Cross-Platform** - Works seamlessly on Windows, Linux, and macOS
- 🔧 **Customizable** - Adjust AI temperature and switch between models
- 🆓 **100% Free** - No API keys or subscriptions required
- ⚡ **Fast & Lightweight** - Minimal dependencies, maximum performance

---

## 📋 Requirements

- **Python 3.8 or higher**
- **Internet connection** (for AI features)
- **Terminal/Command Prompt**

---

## 🔧 Installation

### Windows

1. **Install Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Download Kreggscode GPT**
   ```cmd
   git clone https://github.com/kreggscode/Kreggscode-GPT.git
   cd Kreggscode-GPT
   ```

3. **Run the installer**
   ```cmd
   install.bat
   ```

4. **Start the application**
   ```cmd
   py -3 main.py
   ```
   or
   ```cmd
   python main.py
   ```

### Linux / macOS

1. **Install Python 3.8+**
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
   
   **macOS (Homebrew):**
   ```bash
   brew install python3
   ```

2. **Download Kreggscode GPT**
   ```bash
   git clone https://github.com/kreggscode/Kreggscode-GPT.git
   cd Kreggscode-GPT
   ```

3. **Run the installer**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

4. **Start the application**
   ```bash
   python3 main.py
   ```
   or
   ```bash
   ./main.py
   ```

### Manual Installation

If you prefer to install dependencies manually:

```bash
pip install rich requests langdetect
```

or

```bash
pip install -r requirements.txt
```

---

## 🎯 Usage

### Starting the Application

Simply run the main script:

**Windows:**
```cmd
python main.py
```

**Linux/macOS:**
```bash
python3 main.py
```

### Available Commands

Once the application is running, you can use these commands:

| Command | Description |
|---------|-------------|
| `help` | Show all available commands |
| `clear` | Clear conversation history |
| `files` | List all generated files |
| `clean` | Delete all generated files |
| `temp <value>` | Set AI temperature (0.0-3.0) |
| `model <name>` | Change AI model |
| `exit` or `quit` | Exit the application |

### AI Temperature Guide

Control the creativity level of AI responses:

- **0.0 - 0.5**: Focused and deterministic (best for factual answers)
- **0.5 - 1.0**: Balanced (default: 1.0)
- **1.0 - 2.0**: More creative and varied
- **2.0 - 3.0**: Very creative (experimental)

**Example:**
```
You: temp 0.5
✓ Temperature set to 0.5
```

---

## 💡 Examples

### 1. Simple Conversation

```
You: What is Python?

Kreggscode GPT:
Python is a high-level, interpreted programming language known for its 
simplicity and readability. It's widely used for web development, data 
science, automation, and more.
```

### 2. Generate Code Files

```
You: Create a Python file called hello.py that prints "Hello World"

Kreggscode GPT:
Here's your Python file:

```python
# hello.py
print("Hello World")
```

✓ File saved: generated/hello.py
```

### 3. Multi-Language Support

```
You: ¿Qué es inteligencia artificial?

Kreggscode GPT:
La inteligencia artificial es una rama de la informática que se centra 
en crear sistemas capaces de realizar tareas que normalmente requieren 
inteligencia humana...
```

### 4. Complex Code Generation

```
You: Create a JavaScript file that implements a simple calculator

Kreggscode GPT:
Here's a calculator implementation:

```javascript
// calculator.js
class Calculator {
    add(a, b) { return a + b; }
    subtract(a, b) { return a - b; }
    multiply(a, b) { return a * b; }
    divide(a, b) { return b !== 0 ? a / b : 'Error: Division by zero'; }
}

module.exports = Calculator;
```

✓ File saved: generated/calculator.js
```

---

## 🛠️ Advanced Features

### Adjusting AI Creativity

```
You: temp 1.5
✓ Temperature set to 1.5

You: Write a creative story about AI
```

### Switching AI Models

```
You: model mistral
✓ Model changed to mistral
```

### Managing Generated Files

```
You: files
Generated Files (3):
  1. generated/hello.py
  2. generated/calculator.js
  3. generated/index.html

You: clean
✓ Deleted 3 file(s)!
```

---

## 📁 Project Structure

```
Kreggscode-GPT/
│
├── main.py              # Main application
├── ai_client.py         # AI integration
├── file_manager.py      # File handling
├── requirements.txt     # Dependencies
├── install.bat          # Windows installer
├── install.sh           # Linux/macOS installer
├── run.bat              # Windows launcher
├── LICENSE              # MIT License
└── generated/           # Auto-created files
```

---

## 🐛 Troubleshooting

### "Python not found"

**Solution:**
- Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- On Windows, reinstall and check "Add Python to PATH"

### "Module not found" error

**Solution:**
```bash
pip install rich requests langdetect
```

### Connection errors

**Solution:**
- Check your internet connection
- Wait 15 seconds and try again (rate limit)
- The service may be experiencing high traffic

### Unicode/encoding errors on Windows

**Solution:**
Use Windows Terminal or set encoding:
```cmd
chcp 65001
python main.py
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [Requests](https://requests.readthedocs.io/) - HTTP library
- [LangDetect](https://github.com/Mimino666/langdetect) - Language detection

---

## 📧 Support

If you encounter any issues or have questions:

- 🐛 [Report a bug](https://github.com/kreggscode/Kreggscode-GPT/issues)
- 💡 [Request a feature](https://github.com/kreggscode/Kreggscode-GPT/issues)
- ⭐ Star this repo if you find it useful!

---

<div align="center">

**Made with ❤️ for developers worldwide**

[⬆ Back to Top](#-kreggscode-gpt)

</div>

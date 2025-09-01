# ConvertX 🦅
A flexible and polished batch file converter with logging, error handling, and a sleek CLI design.

## ✨ Features
- ✅ Batch conversion of files between any two extensions.
- ✅ Special handling for `.ipynb → .py` (extracts only code cells).
- ✅ Progress bar (powered by `tqdm`) for smooth feedback.
- ✅ Colored output with `rich` (green = success, red = errors).
- ✅ Preview matching files before conversion (safety first).
- ✅ Option to delete or keep original files.
- ✅ Conversion logs saved in `conversion_log.txt`.
- ✅ Errors logged separately in `error_log.txt`.
- ✅ Skips duplicate conversions automatically.

## 🚀 Installation
Clone this repo and install dependencies:
```bash
git clone https://github.com/your-username/FlexiConvert.git
cd FlexiConvert
pip install -r requirements.txt


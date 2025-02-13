# Document Splitter App

A Streamlit-based web application for splitting text documents into manageable chunks with customizable size limits.

![App Preview](screenshot.png) <!-- Add a screenshot here if available -->

## Features

- **Multi-format Support**: Process TXT, PDF, and DOCX files
- **Custom Chunk Sizes**: Set maximum characters per chunk (100-10,000)
- **Real-time Preview**: See first two chunks before downloading
- **Easy Export**: Download results as formatted TXT file
- **Simple Interface**: User-friendly web-based GUI

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required packages:
```bash
pip install streamlit PyPDF2 python-docx

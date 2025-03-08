# CreaterAE Story: Tour Finder and Instagram Story Creator

## Overview
This project is a **PC-based application** developed using **PyQt5** in Python. The application serves two primary purposes:
1. **Tour Finder**: Utilizes a web parser to search for affordable tours from the **Tbank website** based on user-specified parameters.
2. **Instagram Story Creator**: Integrates with **Adobe After Effects (AE)** to generate customizable Instagram, Telegram, or WhatsApp story templates for promotional purposes. 

**Note**: This application is designed solely for **educational purposes** to explore Python libraries and is not intended for commercial use. Adobe After Effects must be pre-installed on the user's computer, and templates for creating commercials must already be created in AE.

Below is a video demonstration showcasing the functionality and design of the application:

[**Video Demonstration**](https://github.com/samedimanche/CreaterAEstory/assets/152053503/773b11a3-c4ad-43fc-b028-00c81f448e74)

---

## Features

### 1. **Tour Finder**
   - **Web Parser**: Extracts tour data from the Tbank website.
   - **Customizable Search**: Users can specify parameters such as destination, budget, and travel dates.
   - **Affordable Tours**: Displays a list of cheap tours matching the user's criteria.

### 2. **Instagram Story Creator**
   - **Adobe After Effects Integration**: Generates promotional story templates for Instagram, Telegram, or WhatsApp.
   - **Customizable Templates**: Uses pre-created AE templates to produce dynamic and engaging stories.
   - **Educational Focus**: Demonstrates the integration of Python with AE for creative purposes.

---

## Technologies Used
- **Programming Language**: Python
- **GUI Framework**: PyQt5
- **Web Parsing**: BeautifulSoup, Requests (or similar libraries)
- **Adobe After Effects**: Integration via scripting or pre-configured templates.
- **Platform**: Windows, macOS, Linux (any platform supporting Python and PyQt5)

---

## Prerequisites
- **Python 3.x**
- **PyQt5** library
- **Adobe After Effects** (pre-installed on the user's computer)
- **Pre-created AE templates** for story generation.

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/samedimanche/CreaterAEstory.git
   cd CreaterAEstory
   ```

2. **Install Dependencies**:
   - Install the required Python libraries:
     ```bash
     pip install PyQt5 beautifulsoup4 requests
     ```

3. **Run the Application**:
   - Navigate to the project directory and run the following command:
     ```bash
     python main.py
     ```

4. **Configure Adobe After Effects**:
   - Ensure AE is installed and the templates are placed in the correct directory as specified in the application.

---

## Usage
1. **Tour Finder**:
   - Input your desired tour parameters (e.g., destination, budget, dates).
   - View a list of affordable tours extracted from the Tbank website.

2. **Instagram Story Creator**:
   - Select a tour from the results or input custom data.
   - Use the integrated AE templates to generate promotional stories for Instagram, Telegram, or WhatsApp.

---

## Acknowledgments
- **Python** and **PyQt5** for providing the tools to create this application.
- **Adobe After Effects** for enabling dynamic story creation.
- Open-source community for continuous support and inspiration.

---

For more details, visit the [GitHub repository](https://github.com/samedimanche/CreaterAEstory).

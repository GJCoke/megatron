# Visual Automation Platform

## Overview
This repository contains a visualized automation platform built on top of **Appium** and **Selenium**. It is designed to streamline the automation of web and mobile application testing, providing a user-friendly interface for managing and executing test cases.

## Features

- **Cross-platform Support**:
  - Web automation using Selenium.
  - Mobile automation for iOS and Android using Appium.

- **Visualized Test Management**:
  - Intuitive UI for creating, managing, and running test cases.
  - Real-time test execution monitoring and detailed reports.

- **Extensible Framework**:
  - Easily integrate with additional tools and libraries.
  - Modular design to support custom workflows.

- **Reporting and Analytics**:
  - Generate comprehensive test reports.
  - Visualize test performance metrics and trends.

## Prerequisites

### System Requirements
- **Operating System**: Windows, macOS, or Linux.
- **Python**: Version 3.8 or above.
- **Node.js**: Version 14 or above (for UI components).
- **Java**: Required for Appium and Selenium.

### Dependencies
Install the following tools before proceeding:

- Appium Server
- Selenium WebDriver
- Browser Drivers (e.g., ChromeDriver, GeckoDriver)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/GJCoke/megatron.git
   cd megatron
   ```

2. **Set Up the Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python manage.py runserver
   ```

3. **Set Up the Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Start Appium Server**:
   ```bash
   appium
   ```

5. **Configure Environment Variables**:
   Create a `.env` file in the root directory with the following content:
   ```env
   APP_PORT=3000
   BACKEND_URL=http://localhost:8000
   ```

## Usage

1. **Access the Platform**:
   Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

2. **Add Test Cases**:
   - Use the UI to define test cases for web or mobile applications.
   - Assign drivers and specify test parameters.

3. **Execute Tests**:
   - Run individual or batch test cases.
   - Monitor real-time test execution.

4. **View Reports**:
   - Access detailed execution reports.
   - Analyze results using built-in charts and metrics.

## Contributing

We welcome contributions! Follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request on GitHub.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Support

For questions or issues, please open an issue in this repository or contact the maintainers directly.

## Acknowledgments

This platform leverages the power of:
- [Appium](https://appium.io)
- [Selenium](https://www.selenium.dev)
- [SoybeanAdmin](https://docs.soybeanjs.cn)
- [FastAPI](https://fastapi.tiangolo.com)

Thank you to the open-source community for providing these fantastic tools.


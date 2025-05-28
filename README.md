# SwapSpectra 0.3.1

**SwapSpectra** is a modern, minimalistic GUI tool for managing NVIDIA G-SYNC and DLSS Overlay settings, with advanced features for power users and enthusiasts.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [DLSS DLL Swap](#dlss-dll-swap)
- [System Tray & Settings](#system-tray--settings)
- [Configuration](#configuration)
- [Technical Architecture](#technical-architecture)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

SwapSpectra provides a fast, user-friendly way to toggle NVIDIA G-SYNC and DLSS Overlay on or off, swap DLSS DLLs, and manage related settings. It is built with PyQt5 for the interface and leverages .NET interop for advanced NVIDIA NGX operations.

---

## Features

- **One-click G-SYNC Toggle:** Instantly enable or disable G-SYNC.
- **DLSS Overlay Control:** Toggle the NVIDIA DLSS overlay for supported games.
- **DLSS DLL Swap:** Swap or update your DLSS DLLs with a simple file dialog.
- **Status Display:** Real-time display of G-SYNC, DLSS Overlay, and DLSS Swap status.
- **System Tray Integration:** Minimize to tray, with quick access to main actions.
- **Dark Mode:** Stylish, minimalistic dark UI.
- **Admin Mode:** Option to restart the app with administrator privileges for advanced operations.
- **Persistent Settings:** All preferences are saved in an XML config file.
- **Logging:** Built-in log viewer for troubleshooting and transparency.
- **.NET Interop:** Uses a C# library for NGX DLL management and presence detection.
- **Lightweight:** Minimal dependencies, fast startup, and low resource usage.

---

## Screenshots

<!-- Add screenshots here if available -->
<!-- ![Main Window](screenshots/main_window.png) -->

---

## Installation

1. **Requirements:**
   - Windows 10/11 with NVIDIA GPU and drivers.
   - Python 3.8+ (64-bit recommended)
   - [PyQt5](https://pypi.org/project/PyQt5/)
   - .NET Framework (for NGX DLL management features)
   - Administrator rights for some features (DLSS swap, registry changes).

2. **Install Python dependencies:**

3. **Run the application:**

---

## Usage

### Main Window

- **G-SYNC Status:** Shows current G-SYNC state.
- **DLSS Overlay Status:** Shows if DLSS overlay is enabled.
- **DLSS Swap Status:** Shows result of last DLSS DLL swap.
- **Buttons:** Toggle G-SYNC, DLSS Overlay, refresh status, and open DLSS swap dialog.

### System Tray

- Minimize to tray for background operation.
- Right-click tray icon for quick actions: Show, Settings, About, Exit.

### Settings

- Configure "Keep running in system tray" and "Run as administrator".
- All settings are saved to `config.xml`.

---

## DLSS DLL Swap

- Click the **DLSS Swap** button to open a file dialog.
- Select a compatible `nvngx_dlss*.dll` file.
- The app will copy and register the DLL using the built-in .NET library.
- Status and errors are shown in the log viewer.

**Note:** Some swap operations require administrator rights.

---

## Configuration

- All settings are stored in `config.xml` in the application directory.
- The app also updates NVIDIA NGX configuration files as needed for DLL swaps.

---

## Technical Architecture

- **Frontend:** PyQt5 (Python)
- **Backend:** Python core modules for registry, logging, and hardware detection.
- **Interop:** Uses a C# .NET library (`idsw-gvlib`) for NGX DLL management and presence detection.
- **Logging:** All actions and errors are logged in the built-in viewer and to a log file.
- **Admin Elevation:** Uses `pyuac` for privilege escalation when required.

---

## Troubleshooting

- **No NVIDIA Hardware Detected:** Ensure you have a supported NVIDIA GPU and drivers installed.
- **Admin Rights Required:** Some features (DLSS swap, registry changes) require running as administrator.
- **DLL Swap Fails:** Check the log viewer for detailed error messages.
- **Missing Dependencies:** Install all required Python packages and ensure .NET is available.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) for the GUI framework.
- [pyuac](https://pypi.org/project/pyuac/) for UAC elevation.
- .NET / C# for NGX DLL management.
- NVIDIA for G-SYNC and DLSS technologies.

---

*SwapSpectra is not affiliated with or endorsed by NVIDIA Corporation. Use at your own risk.*

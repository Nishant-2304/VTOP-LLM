# VTOP-LLM

VTOP-LLM is a long-term automation initiative designed to create a VTOP copilot that can operate the VTOP portal for students without manual intervention.

## Vision

The goal is to build a system that understands the VTOP interface and can perform the most common student workflows automatically. Instead of logging into VTOP and clicking through menus manually, students should be able to ask the copilot for results and have it perform the required actions in the background.

## What this project aims to achieve

- Automate VTOP navigation and interaction across frequently used tabs
- Capture academic data and workflow state in structured formats
- Enable a higher-level layer that interprets natural language and maps it to actionable VTOP operations
- Support the student use cases that matter most, such as assignment tracking, marks retrieval, course information, academic status checks, etc.

## Core concepts

- Ghost-mode browsing: interact with VTOP behind the scenes using browser automation
- Data extraction: gather important academic data into CSV and structured outputs
- Navigation mapping: represent VTOP menu paths and actions so they can be driven programmatically
- LLM orchestration: use intelligence to convert user instructions into VTOP tasks

## Why it matters

VTOP is essential for students, but its UI is not always optimized for fast access. By automating the interface and centralizing the logic, this project aims to make the system more usable, faster, and less error-prone for students.

## Project structure

- `main.py` — high-level orchestration and automation runner
- `blocks/login.py` — login and authentication handling
- `blocks/navigation/router.py` — VTOP menu navigation abstraction
- `blocks/assignments/router.py` — assignment-related actions and data extraction
- `blocks/marks/router.py` — marks-related actions and data extraction
- `utils/dom.py` — DOM selectors and portal-specific constants
- `utils/navigation.py` — mapping for VTOP navigation routes

## Authors

This project is made by Nishant and Rakshit.

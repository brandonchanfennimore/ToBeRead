# ToBeRead – Media Tracker

ToBeRead is a modular command-line application designed to track books, manga, TV shows, and other media using structured CSV-based storage.

## Overview

The project was built to streamline media tracking across devices through a lightweight terminal interface. It enables users to quickly add, view, and manage media entries without relying on third-party platforms.

## Features

- Command-line interface for rapid media entry
- CSV-based persistent storage
- Duplicate detection to maintain data integrity
- Indexed media enumeration for easy reference
- Modular architecture separating user interaction and storage logic

## Architecture

The application follows a modular design:

- Core logic handles menu routing and user input
- Storage module manages CSV read/write operations
- Helper functions perform validation and duplicate checks

This separation improves maintainability and allows for future feature expansion.

## Future Improvements

- Cross-platform GUI implementation
- Cloud synchronization support
- Enhanced filtering and search functionality
- User configuration settings

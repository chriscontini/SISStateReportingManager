# CLAUDE.md - AI Assistant Guide for SISStateReportingManager

This document provides guidance for AI assistants working with the SISStateReportingManager codebase.

## Project Overview

**SISStateReportingManager** is a Student Information System (SIS) state reporting management application. The project is designed to handle state-level educational reporting requirements, managing student data submissions, compliance tracking, and report generation.

### Current Status

This project is in the **initial development stage**. The repository has been initialized but does not yet contain implementation code.

## Repository Structure

```
SISStateReportingManager/
├── README.md           # Project overview
├── CLAUDE.md           # This file - AI assistant guidance
└── .git/               # Git version control
```

### Planned Structure (to be implemented)

As the project develops, expect the following structure:

```
SISStateReportingManager/
├── src/                # Source code
│   ├── models/         # Data models
│   ├── services/       # Business logic
│   ├── controllers/    # Request handlers
│   ├── utils/          # Utility functions
│   └── config/         # Configuration
├── tests/              # Test files
├── docs/               # Documentation
├── scripts/            # Build/deployment scripts
└── config/             # Environment configurations
```

## Development Guidelines

### Code Style Conventions

When contributing code to this project:

1. **Naming Conventions**
   - Use `camelCase` for variables and functions
   - Use `PascalCase` for classes and components
   - Use `SCREAMING_SNAKE_CASE` for constants
   - Use descriptive, meaningful names

2. **File Organization**
   - One class/component per file
   - Group related functionality in directories
   - Keep files focused and manageable in size

3. **Documentation**
   - Add JSDoc/docstrings for public APIs
   - Include inline comments for complex logic
   - Keep README files updated

### Git Workflow

1. **Branch Naming**
   - Feature branches: `feature/<description>`
   - Bug fixes: `fix/<description>`
   - AI assistant branches: `claude/<session-id>`

2. **Commit Messages**
   - Use clear, descriptive commit messages
   - Start with a verb (Add, Fix, Update, Remove, Refactor)
   - Keep the first line under 72 characters

3. **Pull Requests**
   - Provide clear description of changes
   - Reference any related issues
   - Ensure tests pass before merging

## Working with This Codebase

### For AI Assistants

When working on this project, follow these guidelines:

1. **Before Making Changes**
   - Read existing files before modifying them
   - Understand the context and purpose of the code
   - Check for existing patterns and conventions

2. **When Implementing Features**
   - Follow existing code patterns
   - Write clean, maintainable code
   - Avoid over-engineering solutions
   - Keep security best practices in mind

3. **Testing**
   - Write tests for new functionality
   - Ensure existing tests pass
   - Test edge cases and error conditions

4. **Security Considerations**
   - Never commit sensitive data (credentials, API keys)
   - Validate all user inputs
   - Follow OWASP security guidelines
   - Be mindful of data privacy requirements (FERPA for student data)

### Domain Context: State Reporting

This application deals with educational state reporting, which typically includes:

- **Student Demographics** - Personal information, enrollment data
- **Attendance Records** - Daily attendance tracking
- **Course Information** - Classes, grades, credits
- **Special Programs** - Special education, gifted, etc.
- **Compliance Data** - Required state submissions

**Important**: Student data is protected under FERPA (Family Educational Rights and Privacy Act). Any implementation must consider data privacy and security requirements.

## Common Tasks

### Setting Up the Project

```bash
# Clone the repository
git clone <repository-url>
cd SISStateReportingManager

# Install dependencies (once package.json exists)
npm install  # or yarn install

# Run development server (once configured)
npm run dev
```

### Running Tests

```bash
# Run all tests (once test framework is configured)
npm test

# Run tests with coverage
npm run test:coverage
```

### Building for Production

```bash
# Build the project (once build system is configured)
npm run build
```

## Technology Stack

*To be determined* - The technology stack has not yet been selected. When choosing technologies, consider:

- **Backend**: Node.js/Express, Python/FastAPI, or similar
- **Database**: PostgreSQL, MySQL, or similar for relational data
- **Frontend**: React, Vue, or similar (if applicable)
- **Testing**: Jest, Pytest, or similar

## Environment Variables

When environment variables are needed, document them here:

```env
# Example (to be updated when implemented)
DATABASE_URL=postgresql://user:password@localhost:5432/sis_reporting
API_KEY=your-api-key
NODE_ENV=development
```

**Never commit actual credentials to version control.**

## API Documentation

*To be added* - API documentation will be added as endpoints are implemented.

## Troubleshooting

### Common Issues

*To be added* - Document common issues and solutions as they arise.

## Resources

- [FERPA Overview](https://www2.ed.gov/policy/gen/guid/fpco/ferpa/index.html) - Student data privacy requirements
- [CEDS (Common Education Data Standards)](https://ceds.ed.gov/) - Education data standards reference

---

*Last updated: 2026-01-29*

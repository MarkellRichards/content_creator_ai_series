# Part 4: User Interface

See related blog post: https://www.markellrichards.com/ai-content-creation-assistant-part-4-user-interface/

## Table of Contents

- Overview
- What to expect
- Installation and Setup
- Environment Variables
- Contributing
- License

## Overview

In this part, we will expand our solution by building a user interface using React. With this interface, users can browse their workflows and related artifacts.

## What to expect

- Scaffolding a React application with Rspack
- How to use TanStack Router and Query
- Learn the WebSocket WebAPI
- Styling a website using Tailwind CSS
- Setting up CRUD endpoints using FastAPI
- How to perform joins using SqlAlchemy ORM

## Installation and Setup

Clone the Repository:

`git clone https://github.com/MarkellRichards/content_creator_ai_series`

`cd content_creator_ai_series/part4/content_assistant_server `

Create a Virtual Environment:

`python -m venv venv`
`source venv/bin/activate`

Setup Dependencies:

```bash
pip-compile --generate-hashes -o requirements/requirements.txt pyproject.toml
pip-compile --extra dev -o requirements/requirements-dev.txt pyproject.toml
pip-sync requirements/requirements.txt requirements/requirements-dev.txt
pip install -r requirements.txt
```

Run the FastAPI Server:

`uvicorn src.main:app --reload`

`cd contentent_creator_ai_series/part4/content_assistant_web`

Install dependencies:

`npm install`

Start development server:

`npm run dev`

## Environment Variables

Review .env.example and setup the necessary ENV variables.

## Contributing

Contributions are welcome to enhance the functionality of this project. Please follow these steps for contributing:

1. Fork the repository.
2. Create a new feature branch (git checkout -b feature-branch).
3. Implement your changes and commit them (git commit -m 'Add feature').
4. Push your branch to the forked repository (git push origin feature-branch).
5. Open a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. For more details, refer to the LICENSE file.

Thank you for exploring the FastAPI implementation of our Generative AI Content Creation Assistant. If you encounter any issues or have questions, feel free to open an issue or contact the maintainers.

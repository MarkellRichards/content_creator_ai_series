# Part 3: FastAPI, Websockets, Persistent Storage

## Table of Contents

- Overview
- API Endpoints
- Installation and Setup
- Workflow Explanation
- Environment Variables
- Contributing
- License

## Overview

In Part 3, we expand the FastAPI implementation from part 2. I noted quite a few limitations from the previous approach. Primarily the user was waiting for feedback and we were storing artifacts from the workflows local to the server. In this implementation we add websockets to stream events to the user throughout the workflows lifecycle. We create workflow, blog_posts, social_media_posts, and images entities in Postgres for later retrieval. We also upload image files generated from OpenAI's Dall-e-3 in Minio object storage.

Furthermore, the code is structured around domains, consiting of core and content. Core domain holds global files that impact the server hollistacilly (middleware) or contains logic to be used in other domains such as database session, logging function, and lastly a health check for later k8s deployment. The content domain uses DDD tactical patterns: Repostiory and Service to cleanly abstract code. Each domain (next up will be users) will follow the same general structure:

- Models: SQLAlchemy models
- Schema: Pydantic models
- Repositories: Interface and Repository class responsible for data access
- Services: Services files that contain businessl logic

Content specifically has:

- Prompts: central place to store prompts. For now, other tools later in the series will address prompt versioning and a more robust approach.
- Workflows: contains workflows.

## API Endpoints

## `ws://<address>/content`

- Description: Creates a websocket connection with server.
- websocket paylod (JSON):
  topic: The subject for which content needs to be generated.
  research: A boolean indicating whether research should be included in the content creation process.
- Response: Returns json structue `{"type": results | progress_event, "payload": "msg"}`.

## Installation and Setup

Clone the Repository:

`git clone https://github.com/MarkellRichards/content_creator_ai_series`

`cd content_creator_ai_series/part3 `

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

## Workflow Explanation

1. ContentCreationWorkflow: This is the core workflow that orchestrates content generation:
2. start: Determines the workflow path based on whether additional research is requested.
3. step_research: Conducts research to gather additional content.
4. step_blog: Generates a blog post, with or without additional research.
5. step_social_media: Formats the blog post for social media platforms like LinkedIn.
6. step_illustrator: Generates an image based on the blog content.
7. step_workflow_success: Collects the outputs and updates workflow status, as well as blog_posts, and social_media entities with image url.
8. step_workflow_failed: Updates workflow status to failed and returns status back of failed to user.

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

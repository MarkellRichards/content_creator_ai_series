# Part 2: FastAPI Implementation for Generative AI Content Creation

This part of the project focuses on transitioning our content creation prototype into a deployable application using FastAPI. The goal is to provide a robust server-side solution for generating both text and image content through a request-response mechanism.

## Table of Contents

- Overview
- API Endpoints
- Installation and Setup
- Workflow Explanation
- Environment Variables
- Contributing
- License

## Overview

In Part 2, we introduce a FastAPI server that handles content creation requests. The application uses OpenAI's GPT models for text generation and DALL·E 3 for image production, enabling the dynamic creation of blog posts and corresponding illustrations. Additionally, the project supports linking the generated content to social media platforms like LinkedIn.

## API Endpoints

## POST `/basic`

- Description: Initiates the content creation workflow based on a given topic.
- Request Body:
  topic: The subject for which content needs to be generated.
  research: A boolean indicating whether research should be included in the content creation process.
- Response: Returns a message indicating the completion of the workflow.

## Installation and Setup

Clone the Repository:

git clone https://github.com/yourusername/generative-ai-content-assistant.git
cd generative-ai-content-assistant/part2

Create a Virtual Environment:

python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`

Install Dependencies:

pip install -r requirements.txt

Environment Variables: Create a .env file in the project root with your API keys as shown below:

TAVILY_SEARCH_API_KEY=your_tavily_api_key
OPENAI_API_KEY=your_openai_api_key

Run the FastAPI Server:

uvicorn app.main:app --reload

## Workflow Explanation

1. ContentCreationWorkflow: This is the core workflow that orchestrates content generation:
2. start: Determines the workflow path based on whether additional research is requested.
3. step_research: Conducts research to gather additional content.
4. step_blog_without_research & step_blog: Generates a blog post, with or without additional research.
5. step_social_media: Formats the blog post for social media platforms like LinkedIn.
6. step_illustrator: Generates an image based on the blog content.
7. step_collection: Collects the outputs and finalizes the workflow.

## Environment Variables

Ensure that the following environment variables are set appropriately in your .env file:

- TAVILY_SEARCH_API_KEY: The API key for Tavily Search.
- OPENAI_API_KEY: The API key for accessing OpenAI services.

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

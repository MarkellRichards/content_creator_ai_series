# Generative AI Content Creation Assistant

Welcome to the Generative AI Content Creation Assistant series! This series aims to develop an intelligent content creation system capable of generating images and writing posts for blogs and various social media platforms using advanced generative AI models. The series is divided into sevaral parts that build upon themselves.

## Project Overview (updating per part until finished)

The Generative AI Content Creation Assistant is designed to leverage state-of-the-art AI models to automate the creation of engaging content. Throughout this series we will build upon our solution. We start off with a simple jupyter notebook for quick iteration and testing. Then we transition that code into a FastAPI server. In series to come (as of 28Mar2025) we will be adding various technologies and techniques to expand this solution:

- Websockets
- Human in the loop
- Rate limiting
- Postgres
- Docker
- Minio
- Kubernetes
- Observability
- Users
- User interface using React

and more!

After this series, you will know how to build:

- Generative AI patterns and techniques such as: Retrieval Augmented Generation (RAG) and Agentic Workflows
- A full stack GenAI application
- Create web interfaces using React
- Building servers using FastAPI
- Use docker to package applications into deployable assets
- Orchestrate our docker images using kubernetes
- Observe our suite of applications and llm interactions using observability tools to track metrics, logs, traces, and usage of various models
- How to use various state-of-the-art models for various use cases (text and image generation)

Stay tuned as this progressively updates.

### Part 1: Prototype Development

In Part 1, we develop a prototype version of our content creation assistant. This part primarily focuses on experimenting with generative models and developing a functional baseline system using:

- GPT-4o for generating textual content suitable for blogs and social media posts.
- DALL·E 3 for generating images to accompany the written content.
- LlamaIndex to create workflows.

All code for Part 1 is enclosed within a Jupyter notebook, allowing for easy iteration and testing of the generated content.

### Part 2: Transition to FastAPI Server

Part 2 represents the transition of our prototype into a deployable application by implementing a FastAPI server. This part includes:

- Running the content generation workflow through a request-response architecture.
- Covering various aspects of FastAPI, such as creating endpoints, handling asynchronous requests, and integrating AI models within a server context.
- Demonstrating how to deploy and scale the application in a production environment.

The goal of Part 2 is to build a robust server-side solution that maintains the functionalities of the prototype while being ready for live usage.

### Part 3: FastAPI, Websockets, Persistent Storage

Part 3 builds upon our initial FastAPI implementation and adds a suite of enhancements:

- Websockets to stream updates to user throughout workflow
- Postgres to store workflows, blog posts, social media posts, and images url
- Minio to store the image file - url saved in postgres for later retrieval
- DDD tactical patterns and domain oriented folder structure
- Alembic for database migrations

### Part 4: React. User Interface

Part 4 adds a user interface to our solution. Here's what to expect:

- Scaffolding a React application with Rspack
- How to use TanStack Router and Query
- Learn the WebSocket WebAPI
- Styling a website using Tailwind CSS
- Setting up CRUD endpoints using FastAPI
- How to perform joins using SqlAlchemy ORM
- How to do pagination

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to contribute new features, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes and commit them (git commit -m 'Feature addition').
4. Push to the branch (git push origin feature-branch).
5. Open a pull request with a detailed description of the changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Thank you for checking out the Generative AI Content Creation Assistant! I hope this project inspires you to explore the exciting possibilities of AI and use the techniques learned here for other endeavors. If you have any questions or need further assistance, feel free to open an issue or reach out.

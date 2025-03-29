# Content Creation Assistant

Welcome to the Content Creation Assistant project! This Jupyter Notebook project leverages state-of-the-art AI models and APIs to assist in creating compelling content. From generating blog and social media posts to crafting unique images, this assistant is designed to streamline the content creation process.

## Project Overview

This project centers around an intelligent content creation assistant that uses:

- LlamaIndex Framework: To structure and organize workflows effectively.
- Tavily Search API: To provide real-time information and enhance the capabilities of LLMs.
- OpenAI GPT: For generating high-quality and coherent text suitable for blogs and social media.
- OpenAI Dall-e 3: For creating unique and relevant images based on the generated text content.

## Features

- Blog Post Generation: Automatically generate informative and engaging blog posts using real-time data and advanced language models.
- Social Media Post Creation: Craft eye-catching social media updates tailored for various platforms to boost engagement.
- Image Generation: Create unique images that align with the content of the blog posts, enhancing the visual appeal of your work.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker
- An API key for the Tavily Search API
- An API key for the OpenAI GPT and Dall-e models

#### Alternative

Can create a requirements.txt and virtual environment. Modify notebook as needed.

### Installation

1. Clone the Repository:

```bash
git clone https://github.com/yourusername/content-creation-assistant.git
cd content-creation-assistant
```

2. Review .env.example and set environment variables

3. Start docker

```bash
docker-compose up -d
```

## Usage

1. View the docker logs for a URL with a token to access the notebook.

2. Open the Notebook:

Navigate to the project directory and open the main Jupyter Notebook file.

3. Run the Notebook:

Follow the instructions within the notebook to generate blog posts, social media updates, and accompanying images.

## Customization

The project is highly customizable:

- Templates: Modify the text templates to better fit your tone and style.
- Image Settings: Adjust image generation parameters to suit your visual content needs.
- Subclass Workflows or include nested workflows to modify blog and social media generation (For example, add additional steps for other platforms)

## Contributing

Contributions are welcome! If you have suggestions for improvements, please fork the repository and create a pull request. You can also open an issue to describe any bugs or feature requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

- The developers of the LlamaIndex framework for facilitating efficient workflow creation.
- Tavily for providing an excellent real-time search API.
- OpenAI for the powerful GPT and Dall-e models that make this project possible.

I hope you find this Content Creation Assistant useful and that it enhances your content creation process. For any questions or support, feel free to reach out. Happy creating!

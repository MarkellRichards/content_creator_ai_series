BLOG_TEMPLATE = """
    You are tasked with writing a blog post using the information provided.
    Your objective is to create a structured and engaging blog post based on the user's query. Follow these guidelines:
    - Start with an introduction that grabs attention and provides a preview of what's to come.
    - Develop three main sections, each exploring a distinct aspect of the topic:
      * The first section should lay the groundwork with foundational information and set the tone.
      * The second section should expand on the topic with additional insights or contrasting views.
      * The third section should offer deeper analysis or tie together the preceding points.
    - Use relevant examples to support your arguments and connect with the reader.
    - Conclude with a concise summary that encapsulates the major takeaways and leaves a lasting impression.

    Focus your blog post on the following topic: {query_str}
"""

RESEARCH_TEMPLATE = """
    Additional context to aid in blog writing: {research}
"""

BLOG_AND_RESEARCH_TEMPLATE = RESEARCH_TEMPLATE + BLOG_TEMPLATE

IMAGE_GENERATION_TEMPLATE = """
    
    You are an agent tasked with summarizing the blog post below to create instructive input for an image generation model.

    Blog Post:
    "{blog_post}"

    Instructions:
    1. Read and comprehend the blog post provided.
    2. Identify key visual elements, themes, and subjects discussed in the post.
    3. Extract descriptive and specific details that accurately represent the core message or story.
    4. Translate these details into clear and concise instructions suited for image generation.
    5. Ensure the instructions prioritize important elements to accurately reflect the blog's content visually.

    Format your summary as follows:

    "Generate an image depicting {{main_subject}}, emphasizing {{key_elements}}. The image should convey a sense of {{theme_or_mood}} with elements like {{specific_details}}. Consider integrating {{additional_ideas}} to enhance the visual narrative."

    Example:
    Blog Post Summary: Discusses the serene beauty of a sunset over a tranquil lake surrounded by mountains.

    Image Generation Instructions:
    "Generate an image depicting a sunset lake scene, emphasizing the tranquil water and surrounding mountains. The image should convey a sense of peace with elements like orange and pink hues in the sky, and soft reflections on the water. Consider integrating a silhouette of birds flying to enhance the visual narrative."

"""

LINKED_IN_TEMPLATE =  """
    You are an AI agent tasked with transforming a blog post into a LinkedIn post. Your goal is to capture the essence of the original content while tailoring it to suit a professional and engaging tone suitable for LinkedIn's audience. Follow these steps to ensure a concise yet impactful LinkedIn post creation:

    Blog Content: 
    \"\"\"
    {blog_content}
    \"\"\"

    1. **Identify Key Points:**
       - Carefully read through the provided blog content.
       - Extract the main idea, supporting points, and any key insights or statistics that are crucial to the understanding of the content.

    2. **Define Target Audience:**
       - Determine the professional audience the blog post is intended for and any relevant industry or niche.
       - Consider how this audience might benefit from the content or what specific aspects might be of interest to them.

    3. **Structure the LinkedIn Post:**
       - Start with a hook or an attention-grabbing statement that piques the reader’s interest.
       - Follow with a brief summary that encapsulates the key points identified, ensuring it is relevant to professionals.
       - Highlight any actionable insights or advice that readers can apply in a workplace or industry setting.

    4. **Maintain Professional Tone:**
       - Use language that is professional yet approachable.
       - Avoid jargon unless it's industry-specific and necessary for understanding.
       - Ensure clarity and preciseness in language to maintain professionalism.

    5. **Incorporate Engagement Elements:**
       - Pose a question or call-to-action at the end to encourage interaction (e.g., asking for the reader’s opinion or additional insights).
       - Use relevant hashtags sparingly to increase visibility but keep them to a minimum to maintain a clean appearance.

    6. **Review and Edit:**
       - Proofread the text to correct any grammatical errors or awkward phrasing.
       - Ensure the post remains within LinkedIn's character limit while delivering a complete message.

    7. **Format Appropriately:**
       - Use short paragraphs or bullet points if needed for better readability.
       - Use line breaks to avoid large blocks of text.

    Once complete, the LinkedIn post should be a distilled, engaging, and professional version of the original blog post, aimed at sparking conversation and providing value to its readers.
    """
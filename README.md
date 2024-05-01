# UWP ChatBot

Hello and welcome to our project! This project aims to add a large language model chatbot/agent to the UWP Website for basic question answering and navigation for new and existing users. This chatbot or agent would make navigating the Parkside website easier for both new and existing users as they could ask the agent for the link they are looking for and/or the agent could directly answer the question(s) they have. This would simplify their interaction with the information-dense website.

### Custom Settings
<video width="640" height="360" controls>
  <source src="https://raw.githubusercontent.com/uwp-se/ChatBot/main/Documents/VideosOfProject/Custom%20Settings.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Regular Use
https://user-images.githubusercontent.com/uwp-se/ChatBot/Documents/VideosOfProject/regular%20use.mp4

## Repo Navigation

- [Fall 2023 Timeline](/Documents/Fall%202023/Semester-Timeline.md): Detailed timeline breakdown with expected hours for each sprint in the Fall 2023 semester.
- [Spring 2024 Timeline](/Documents/Spring%202024/Semester-Timeline.md): Detailed timeline breakdown with expected hours for each sprint in the Fall 2023 semester.
- [Documents](/Documents): Contains our presentations for each sprint we have done and useful images.
- [Mock Website](/Frontend%20Website): Contains the Front-End for our proposed ChatBot.
- [Dataset_Scripts](/Dataset_Scripts): Python scripts for scraping/generating and cleaning the dataset.
- [Datasets](/Datasets): JSON files the scripts produced.
- [Documents](/Documents): Powerpoints and images for said powerpoints.
- [EmbeddedAgent](/EmbeddedAgent): WebLLM implementation for serving LLM to be processed client-side.
- [FirebaseFunctions](/FirebaseFunctions): Helper Firebase deployment scripts.
- [Frontend Website](/Frontend%20Website): School website clone for displaying WebLLM implementation.
- [RAG](/RAG): Giving the ChatBot long-term memory.
- [Training_Scripts](/Training_Scripts): Using the dataset to finetune a local LLM.


## What is needed for the project

### Software:
- IDE (Choices include [VS Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/), [Notepad++](https://notepad-plus-plus.org/), etc; we primarily use VS Code)
- [LM Studio](https://lmstudio.ai/) (At the time of writing, no Apple Intel Silicon version available)
- [Oogabooga](https://github.com/oobabooga/text-generation-webui) (Supports Apple Intel Silicon and advanced features like fine-tuning)
- [Google CoLab](https://colab.research.google.com/) (Free version available; paid version recommended if funding is available for more robust capabilities)

### API/Libraries:
- Langchain: [Langchain Documentation](https://python.langchain.com/docs/get_started/introduction)
- Qdrant: [Qdrant](https://qdrant.tech/)
- Kobold: [KoboldAI](https://github.com/KoboldAI/KoboldAI-Client)
- OpenAI: [OpenAI for Developers](https://openai.com/product#made-for-developers)
- Huggingface: [HF Models](https://https://huggingface.co/models)
- Huggingface: [HF Docs](https://huggingface.co/docs)
- llama.cpp: [llama.cpp GitHub](https://https://github.com/ggerganov/llama.cpp) (Popular LLM inference in C/C++)

### Languages:
- Python
- HTML/CSS/JavaScript
- TypeScript
- Shell

### Language Model (LLM)
Our project leverages a series of specialized language models to facilitate user engagement with the UWP website. These models are part of our Huggingface repository at [ByteSized](https://huggingface.co/ByteSized) and  [Aaron616](https://huggingface.co/Aaron616), each tailored to different aspects of the user experience:

- **Augmented UWP Instruct**: This model is the final version of the first run
made using our improved dataset. The scripts for geberating and augmenting can
be found in the Important_Scripts folder. [View Model Here](https://huggingface.co/datasets/Aaron616/Augmented-UWP-Instruct)

- **UWP-Instruct-Validate**: This model is the final validation set for the second run on our dataset, the changes made are mainly in the category section so the main content is largely the same. [View Model Here](https://huggingface.co/datasets/Aaron616/UWP-Instruct-Validate)

- **UWP-Instruct-Train**: This model is the final training set for the second
run on our dataset, the changes made are mainly in the category section so
the main content is largely the same. [View Model Here](https://huggingface.co/datasets/Aaron616/UWP-Instruct-Train)

- **UWP Instruct**: This primary model is trained on the Parkside website dataset, focusing on providing navigational guidance. It is praised for its accurate and professional interactions. [View UWP Instruct Model](https://huggingface.co/ByteSized/Mistral-7B-OpenOrca-UWPInstruct) | [View Dataset](https://huggingface.co/datasets/ByteSized/Parkside-Instruct)

- **UWP Instruct-Security Instruct**: Developed through a sequential fine-tuning process, this model begins with website navigation and incorporates security-related prompts, aiming to offer a more rounded assistance. [View UWP Instruct-Security Model](https://huggingface.co/ByteSized/Mistral-7B-OpenOrca-UWPInstructUWPSecurity) | [View Dataset](https://huggingface.co/datasets/ByteSized/Parkside-SecurityInstruct)

- **UWP Instruct with Security**: This comprehensive model merges the instruction and security datasets, striving for a balanced training approach to handle both instructional and security inquiries equally. [View UWP Instruct with Security Model](https://huggingface.co/ByteSized/Mistral-7B-OpenOrca-UWPInstructWSecurity) | [View Dataset](https://huggingface.co/datasets/ByteSized/Parkside-Instruct-W-Security)

The **UWP Instruct** model excels in its domain, having been intensively trained to respond to instructional queries. While it does not specifically address prompt-poisoning, it still delivers high-quality assistance. It's important to note that the security aspect was a secondary consideration in this phase of development. We believe that further tuning with a primary focus on security could be a valuable direction for enhancing the model's capabilities. The current scope concentrated on instructional tuning due to time constraints, offering a solid foundation for future enhancements.

## Installation/Initiation Steps

For detailed installation and initiation instructions, please refer to the README.md file within each specific folder. For example, you can find specific setup instructions in the [EmbeddedAgent README](EmbeddedAgent/README.md) and other relevant directories.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`OPENAI_API_KEY`

`QDRANT_COLLECTION_NAME` this qdrant collection is "UWParkside_vectorDB" but you can name it anything you like, just keep it consistent because its a pointer to main memory location


## HTTP request reference

### Note
LMStudio uses an API URL that mimics OpenAIs file structure. This is intentional to be compatiable with projects that query OpenAI's API.

#### POST to LM Studio or server running LM Studio

For localhost
```http
  POST http://localhost:1234/v1/completions?
```

For server, replace the dummy IP with the actual IP
```http
  POST 123.456.78.901/1234/v1/completions? 
```

| Parameter     | Type     | Description                               |
|---------------|----------|-------------------------------------------|
| `message`     | `string` | **Required**. User message                |
| `response`    | `string` | **Required**. The same as message, it is required by kobold |
| `temperature` | `double` | **Required**. Sets the creativeness of the LLM |


#### Get item

For localhost
```http
  GET http://localhost:1234/v1/models
```

For server, replace the dummy IP with the actual IP
```http
  GET 123.456.78.901/1234/v1/models? 
```

| Parameter | Type  | Description                        |
|-----------|-------|------------------------------------|
| `none`    | `none`| Fetches the model meta-data the LLMs available. |


## Potential Future Work!

The roadmap for the UWP ChatBot project is both ambitious and methodical, requiring a step-by-step approach that starts from concrete deployment to blue-sky thinking. Future teams are encouraged to:

- **Model Deployment and Real-World Application**: Prioritize the deployment of the ChatBot into a live, production environment. Tackle the real-world challenges of deployment head-on, such as scalability, robustness, and continuous integration/delivery. Understanding the nuances of deploying models in a user-facing context is the first critical step.

- **Generalized API Integration**: After successful deployment, work on crafting a generalized API that can be easily adopted by other software engineering projects. This should be designed to simplify the integration process, making the ChatBot a plug-and-play solution for various applications.

- **Comprehensive Dataset Creation**: As the foundation strengthens, shift focus to expanding the dataset. A comprehensive dataset that encompasses a full range of user interactions will refine the ChatBot’s accuracy and reliability in handling queries.

- **Advanced Model Training**: With a robust dataset, move on to enhancing the model through advanced training techniques. Stay abreast of the latest developments in training methodologies to ensure the ChatBot's responses are precise and contextually relevant.

- **Mixture of Experts and LoRA**: Investigate cutting-edge architectures such as Mixture of Experts (MoE) and techniques like LoRA to augment the model's capabilities. These advancements could significantly improve efficiency and adaptability without the need for extensive retraining.

- **Interdisciplinary Collaboration**: Encourage cross-disciplinary cooperation to expand the ChatBot’s utility. Collaborate with educators, IT professionals, and other domain experts to tailor the ChatBot's functionalities to a wide array of academic and administrative needs.

- **Educational Assistant Development**: Dream big by transforming the ChatBot into a full-fledged educational assistant. Envision a tool that not only answers questions but also assists with summarizing texts, tracking academic schedules, and providing personalized learning support, thereby revolutionizing the educational landscape.

- **AI Evolution Adaptation**: Lastly, maintain a culture of innovation by continually adapting to the rapid evolution of AI. Stay on the cutting edge by incorporating the latest AI research and technologies, ensuring that the ChatBot remains a state-of-the-art tool for the University of Wisconsin-Parkside community.

The path ahead for the UWP ChatBot is both challenging and exhilarating. We pass this endeavor to the next generation of innovators, trusting in your creativity and commitment to carry this project forward into new realms of possibility.

## Contributors
We acknowledge and thank the developers who have contributed to this project. If you have contributed, please add your profile in the format "Role: [Your Name](GitHub Profile Link)" to the list below.

### Founders & Initial Team
- Project Founder, Scrum Master, Lead Training Engineer: [Elijah Kulpinski](https://github.com/elijah-kulpinski)
- Lead Backend Developer, Web Developer, UI, Server Manager: [Christopher Mata](https://github.com/Christopher-Mata)
- Lead Data Engineer: [Aaron Antreassian](https://www.github.com/Antreassian616)

### Additional Contributors
- Firebase Deploying & Hosting: [Jose Giles](https://github.com/JoalChat2024)
- Lead Database and RAG Developer: [Brandon Padjen](https://github.com/)

This section is a living document reflecting the ongoing contributions and evolving expertise within our team. As the project grows, so does our team and the collective skill set that powers the UWP ChatBot forward.

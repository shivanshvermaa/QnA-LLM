# QnA-LLM
# QnA Chat Bot using Chainlit and OpenAI

This repository contains code for implementing a QnA chat using Chainlit and OpenAI. The application is designed to answer questions based on the given input and provide relevant responses using GPT-3.5-Turbo.

It internally uses ChromaDB as it's vector database store for RAG applications.

## Getting Started

To get started with using the QnA chat, follow these steps:

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/your_username/qna-chat-bot.git
   ```
2.**Run the application**:
   ```bash
   chainlit document_qa.py -w
   ```

Additionally you will have to create a YAML file named **config.yml** that contains your OpenAI api key.The format of the YAML fill should be:
  ```YAML
  openai:
    api-key: YOUR-API-KEY-HERE
   ```

  
## Features
- QnA chat bot powered by Chainlit and OpenAI.
- Provides responses based on natural language processing.
- Easy to use and integrate into existing projects.

## Usage

The QnA chat bot can be used in various scenarios such as:

- Seeking answers to general questions.
- Retrieving information from documents or texts.
- Assisting investors and fundamental researchers with queries related to public filings of companies to the SEC.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Chainlit for providing the framework for building conversational AI.
- OpenAI for their powerful natural language processing capabilities.

## Work in Progress

This project is a work in progress with more features coming soon. The bot will be primarily focused on using the bot to answer investor/fundamental researcher's questions of a public filing of any company to the SEC board.

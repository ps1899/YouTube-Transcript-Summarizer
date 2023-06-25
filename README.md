# YouTube-Transcript-Summarizer
**Youtube Transcript Summarizer** is a Chrome Extension that allows users to get a **summarized** version of the transcripts of YouTube videos with a **single click**. It utilizes Natural Language Processing (NLP) algorithms such as **Latent Semantic Analysis** (LSA) and **state-of-the-art Huggingface Transformer models** to efficiently summarize the transcripts of YouTube videos with a single click. It is built on a **Flask Backend REST API** to expose the summarization service to the client.


## Project Stages
![alt text](/extention/images/stages.png?raw=true)


## Features  
- Summarizes YouTube video transcripts employing advanced NLP techniques.
- Utilizes Latent Semantic Analysis (LSA) for extractive summarization of very long transcripts.
- Leverages Transformer models for abstractive summarization of shorter transcripts.
- Allows the user to adjust the maximum length of the summarized text through dynamic truncation.
- Adopts a language-agnostic approach and supports transcript summarization even for videos without subtitles.
- Employs an asynchronous XMLHttpRequest to ensure non-blocking communication with the Flask Backend.


## Output Screenshot
![alt text](/extention/images/output.png?raw=true)

## Installation
- Clone this repository to your local machine:
- 
  ```
  git clone https://github.com/yourusername/YouTube-Transcript-Summarizer.git
  cd YouTube-Transcript-Summarizer
  ```
- Next, install the dependencies:
- 
  ```
  pip install -r Requirements.txt
  ```
- To execute the Application locally:
  - Start the Flask backend on the terminal using the following command:
    
    ```
    python TranscriptApp.py
    ```
    This will start a local server at ```http://127.0.0.1:5000/```. You may see a couple of warnings but it's all good and you may ignore it!
  - Load the extension into Google Chrome:
    - Open Google Chrome and go to ```chrome://extensions/```.
    - Enable the ```Developer mode``` toggle in the top right corner.
    - Click on ```Load unpacked``` and select the directory where you cloned this repository.
  - You should now see the extension loaded in the Chrome toolbar. Navigate to any YouTube video, click on the extension icon, and click "Summarize" to see the summary of the video   transcript.
  - All Done..!!


## Contribution
Contributions to this project are *welcome!* If you wish to contribute, please follow these steps:
- Fork the repository.
- Create a new branch for your features or fixes.
- Make your changes and commit them.
- Push your changes to your fork.
- Create a Pull Request from your fork to this repository.
- Make sure to update the ```Requirements.txt``` file if you've added any new dependencies.

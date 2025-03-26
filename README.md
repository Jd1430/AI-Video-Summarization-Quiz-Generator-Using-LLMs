# AI Video Summarization & Quiz Generator

## 📌 Overview
This project is an AI-powered web application that allows users to upload a video file or paste a YouTube link. The system extracts the audio, transcribes it into text using Whisper AI, translates it into a selected language, and generates a detailed summary using Groq LLM. Additionally, an AI-powered quiz generator creates questions based on the transcript and summary, allowing users to test their understanding interactively. The quiz provides multiple difficulty levels, instant feedback, and a final score. It supports both YouTube videos and uploaded files.

## 🎥 Project Demo  
[ Watch the Video](https://github.com/user-attachments/assets/7848d276-bfa4-4f28-b53a-619e6af8edb0)

## 🚀 Features
- **YouTube Video Processing**: Extracts audio from YouTube videos.
- **Local Video Processing**: Upload and extract audio from video files.
- **Speech-to-Text Transcription**: Uses Whisper AI to transcribe audio.
- **Multilingual Support**: Translates transcripts into multiple languages.
- **AI-Generated Summaries**: Provides a detailed summary using Groq's LLM.
- **AI-Powered Quiz Generation**: Creates quizzes with different difficulty levels.
- **Interactive Quiz Interface**: Users can take quizzes and get instant feedback.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **AI Models**:
  - Whisper AI for speech-to-text
  - Groq LLM for summarization and quiz generation
  - Google Translator for text translation
- **Video Processing**: MoviePy
- **YouTube Downloading**: yt-dlp

## 📥 Installation
### Prerequisites
Ensure you have Python installed. Then, install dependencies:
```bash
pip install requirements.txt
```
or
```bash
pip install streamlit whisper moviepy deep-translator yt-dlp groq
```

### Clone the Repository
```bash
git clone https://github.com/yourusername/ai-video-summarization.git
cd ai-video-summarization
```

### Set Up API Keys
Create a `.streamlit/secrets.toml` file and add your Groq API key:
```toml
GROQ_API_KEY = "your_api_key_here"
```

Alternatively, you can set it as an environment variable:
 **Open comand prompt and set your API key**
```bash
set GROQ_API_KEY=your_actual_groq_api_key_here
```
```bash
export GROQ_API_KEY="your_api_key_here"
```

### Run the Application
```bash
streamlit run app.py
```

## 🎥 How to Use
1. **Upload a Video File** or **Paste a YouTube Link** in the sidebar.
2. **Select a Language** for transcription.
3. Click **Process Video** to extract, transcribe, and summarize content.
4. **Review the generated transcript and summary**.
5. Select a **Quiz Difficulty** and generate a quiz.
6. **Take the quiz** and get instant feedback.



## 🔗 Contact
For any questions or collaborations, feel free to reach out:
- **GitHub**: [Jd1430](https://github.com/Jd1430)
- **Email**: jayanthdevarajgowda@gmail.com

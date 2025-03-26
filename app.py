import streamlit as st
import os
import tempfile
import whisper
import moviepy.editor as mp
from deep_translator import GoogleTranslator
import yt_dlp  
import groq  

# Load API key from Streamlit Secrets or Environment Variable
groq_api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
groq_client = groq.Client(api_key=groq_api_key)

# Function to download YouTube video
def download_youtube_video(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tempfile.gettempdir() + '/youtube_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        audio_path = ydl.prepare_filename(info).replace('.webm', '.wav').replace('.m4a', '.wav')
    return audio_path

# Function to extract audio from uploaded video
def extract_audio(video_path, audio_path="extracted_audio.wav"):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path

# Function to transcribe audio
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"], result["language"]

# Function to translate transcript
def translate_transcript(text, source_lang, target_lang):
    if source_lang != target_lang:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    return text  

# Function to generate detailed summary using Groq LLM
def generate_summary_groq(transcript):
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert at summarizing transcripts into detailed summaries."},
            {"role": "user", "content": f"Summarize the following transcript in a detailed manner:\n\n{transcript}"}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content if response.choices else "Error generating summary."

# Function to generate quiz questions using Groq LLM
def generate_quiz(transcript, summary, difficulty):
    prompt = f"""
    Generate a quiz based on the transcript and summary provided. 
    Difficulty level: {difficulty}
    - Beginner: Easy questions based on the content.
    - Intermediate: Slightly tougher questions that require deeper understanding.
    - Advanced: Questions related to the content but not explicitly stated.

    Transcript: {transcript}
    Summary: {summary}

    Generate 5 quiz questions with 4 options each.
    Format:
    Question: <question>
    Options: A) <option1>, B) <option2>, C) <option3>, D) <option4>
    Answer: <correct_option>
    """

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "You are an expert quiz generator."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return response.choices[0].message.content if response.choices else "Error generating quiz."

# Initialize session state
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False
if "score" not in st.session_state:
    st.session_state.score = 0

# ---- SIDEBAR ----
st.sidebar.title("🎬 AI Video Processing")

# Option to upload a file or paste a YouTube link
uploaded_file = st.sidebar.file_uploader("📂 Upload a video file", type=["mp4", "avi", "mov", "mkv"])
youtube_url = st.sidebar.text_input("📺 Paste YouTube Video Link")

# User selects output transcript language
language_options = {
    "English": "en", "kannada": "kn","Spanish": "es", "French": "fr", "German": "de",
    "Italian": "it", "Portuguese": "pt", "Russian": "ru", "Hindi": "hi"
}
target_lang = st.sidebar.selectbox("🌍 Select transcript language", list(language_options.keys()))
target_lang_code = language_options[target_lang]

if st.sidebar.button("▶ Process Video"):
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.read())
            video_path = temp_file.name
        st.sidebar.info("⏳ Extracting Audio...")
        audio_path = extract_audio(video_path)
    elif youtube_url:
        st.sidebar.info("⏳ Downloading YouTube Audio...")
        audio_path = download_youtube_video(youtube_url)
    else:
        st.sidebar.error("⚠️ Please upload a video file or enter a YouTube link.")
        st.stop()

    st.sidebar.info("⏳ Transcribing Audio...")
    transcript, detected_language = transcribe_audio(audio_path)
    st.session_state.transcript = translate_transcript(transcript, detected_language, target_lang_code)

    st.sidebar.success(f"✅ Detected Language: {detected_language.upper()}")

    st.sidebar.info("⏳ Generating Detailed Summary...")
    st.session_state.summary = generate_summary_groq(st.session_state.transcript)

    # Cleanup temp files
    os.unlink(audio_path)

# ---- MAIN CONTENT ----
st.subheader(" AI Video Summarization & Quiz")

if uploaded_file or youtube_url:
    if uploaded_file:
        st.video(uploaded_file)
    elif youtube_url:
        st.video(youtube_url)

    # Display transcript
    if st.session_state.transcript:
        st.subheader("📜 Final Transcript")
        st.text_area("", st.session_state.transcript, height=200)

    # Display summary
    if st.session_state.summary:
        st.subheader("📌 Detailed Summary")
        st.text_area("", st.session_state.summary, height=200)

    # Quiz Difficulty Selection
    difficulty_level = st.selectbox("🎯 Select Quiz Difficulty", ["Beginner", "Intermediate", "Advanced"])

    if st.button("📝 Take Quiz"):
        st.info("⏳ Generating Quiz...")
        quiz_text = generate_quiz(st.session_state.transcript, st.session_state.summary, difficulty_level)

        # Parse the quiz into structured format
        quiz_questions = []
        quiz_answers = []

        for block in quiz_text.split("\n\n"):
            lines = block.split("\n")
            if len(lines) >= 3:
                question = lines[0].replace("Question: ", "").strip()
                options = lines[1].replace("Options: ", "").split(", ")
                answer = lines[2].replace("Answer: ", "").strip()

                quiz_questions.append({"question": question, "options": options})
                quiz_answers.append(answer)

        st.session_state.quiz = quiz_questions
        st.session_state.quiz_answers = quiz_answers
        st.session_state.user_answers = [None] * len(quiz_questions)
        st.session_state.quiz_completed = False

    # Display quiz
    # Display quiz only if available
    if st.session_state.quiz:
        st.subheader("🧠 Take the Quiz")

        for i, q in enumerate(st.session_state.quiz):
            st.write(f"**Q{i+1}: {q['question']}**")
            selected_answer = st.radio("", q["options"], key=f"q{i}")

            st.session_state.user_answers[i] = selected_answer

            # Show feedback below the question after submission
            if st.session_state.quiz_completed:
                correct_answer = st.session_state.quiz_answers[i]
                if selected_answer == correct_answer:
                    st.success(f"✅ Correct! The answer is **{correct_answer}**.")
                else:
                    st.error(f"❌ Incorrect. The correct answer is **{correct_answer}**.")

        if st.button("✅ Submit Answers"):
            st.session_state.quiz_completed = True
            st.session_state.score = sum(
                1 for i in range(len(st.session_state.quiz)) if st.session_state.user_answers[i] == st.session_state.quiz_answers[i]
            )

        if st.session_state.quiz_completed:
            st.subheader(f"🏆 Your Final Score: {st.session_state.score} / {len(st.session_state.quiz)}")


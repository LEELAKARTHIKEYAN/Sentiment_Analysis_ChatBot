import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download necessary NLTK data
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to detect sentiment
def analyze_sentiment(user_message):
    sentiment_score = sia.polarity_scores(user_message)
    if sentiment_score['compound'] >= 0.05:
        return "positive", sentiment_score['compound']
    elif sentiment_score['compound'] <= -0.05:
        return "negative", sentiment_score['compound']
    else:
        return "neutral", sentiment_score['compound']

# Function to generate appropriate responses
def generate_response(sentiment):
    responses = {
        "positive": "I'm glad to hear that! 😊 How can I assist you further?",
        "negative": "I'm sorry to hear that. 😔 How can I help improve things?",
        "neutral": "Got it! 😊 Let me know if there's anything I can help you with."
    }
    return responses[sentiment]

# Function to evaluate customer satisfaction
def evaluate_response(user_feedback, sentiment):
    feedback_map = {
        "positive": {"happy": 1, "unhappy": 0},
        "negative": {"happy": 0, "unhappy": 1},
        "neutral": {"happy": 0.5, "unhappy": 0.5},
    }
    return feedback_map.get(sentiment, {}).get(user_feedback, 0)

# Streamlit UI
st.title("Sentiment-Aware Chatbot")
st.subheader("Detects user emotions and responds appropriately!")

# Chat Interface
user_message = st.text_input("You: ", placeholder="Type your message here...")

if user_message:
    with st.spinner("Analyzing sentiment..."):
        sentiment, score = analyze_sentiment(user_message)
        bot_response = generate_response(sentiment)
        
    st.write(f"**Sentiment Detected:** {sentiment.capitalize()} (Score: {score:.2f})")
    st.text_area("Chatbot Response:", bot_response)

    # Feedback for evaluation
    st.markdown("### Feedback on Chatbot's Response")
    user_feedback = st.radio("Was the chatbot's response appropriate?", ("happy", "unhappy"))
    if st.button("Submit Feedback"):
        satisfaction_score = evaluate_response(user_feedback, sentiment)
        if satisfaction_score == 1:
            st.success("Thank you for your feedback! 😊")
        elif satisfaction_score == 0:
            st.error("We're sorry the response wasn't helpful. 😔")
        else:
            st.warning("Thank you! We'll continue improving. 🙂")

# Evaluation Criteria Section
st.sidebar.subheader("Evaluation Criteria")
st.sidebar.markdown("""
1. **Accuracy of Sentiment Detection:**
   - Measures how well the chatbot detects user sentiment.
   - Based on the compound score thresholding logic.

2. **Appropriateness of Responses:**
   - Evaluates if the chatbot's responses match user sentiment.
   - Feedback mechanism ensures appropriate response assessment.

3. **Impact on Customer Satisfaction:**
   - Feedback from users (happy/unhappy) directly influences satisfaction scoring.
   - Higher satisfaction indicates better chatbot performance.
""")

# Instructions for running
st.sidebar.subheader("Instructions")
st.sidebar.write("""
- Enter a message in the chat input to interact with the chatbot.
- The chatbot will detect sentiment and respond accordingly.
- Provide feedback to help evaluate its effectiveness.
""")

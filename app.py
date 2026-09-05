import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ AI Content Assistant")
st.caption("Create platform-ready social media content with Groq AI.")

# Get API key from Streamlit Secrets
# Get API key from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY", "").strip()

# Safe diagnostic information
api_key = st.secrets.get("GROQ_API_KEY", "").strip()

if not api_key:
    st.error("GROQ_API_KEY is missing from Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

if not api_key:
    st.error("GROQ_API_KEY is missing from Streamlit Secrets.")
    st.stop()

if not api_key:
    st.error("GROQ_API_KEY is not configured. Add it to Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=api_key)

content_type = st.selectbox(
    "Content Type",
    ["Social Media Post", "Promotional Post", "Educational Post", "Announcement", "Tips / Listicle"],
)

platform = st.selectbox(
    "Platform",
    ["Instagram", "LinkedIn", "Facebook", "X (Twitter)", "TikTok"],
)

topic = st.text_input(
    "Topic",
    placeholder="Example: Benefits of using AI for small businesses",
)

audience = st.text_input(
    "Target Audience",
    placeholder="Example: Small business owners",
)

tone = st.selectbox(
    "Tone",
    ["Professional", "Friendly", "Casual", "Inspirational", "Educational", "Persuasive", "Witty"],
)

generate = st.button("✨ Generate Content", type="primary", use_container_width=True)

if generate:
    if not topic.strip() or not audience.strip():
        st.warning("Please enter both a topic and target audience.")
        st.stop()

    prompt = f"""
You are an expert social media content writer.

Create a complete, ready-to-publish {content_type.lower()} for {platform}.

Topic: {topic}
Target audience: {audience}
Tone: {tone}

Return the response using exactly this structure:

POST:
[The complete post text. Make it engaging and appropriate for the selected platform.]

CAPTION:
[A concise caption suitable for the platform.]

HASHTAGS:
[8-12 relevant hashtags, separated by spaces.]

Requirements:
- Do not mention that you are an AI.
- Do not add explanations outside the requested structure.
- Keep the content original, useful, and natural.
- Match the selected tone and audience.
- Make the post platform-appropriate.
"""

    try:
        with st.spinner("Creating your content..."):
            response = client.chat.completions.create(
               model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional social media content writer.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1200,
            )

        result = response.choices[0].message.content

        st.success("Content generated successfully!")
        st.markdown("### Your Content")
        st.text_area("Copy your generated content:", result, height=450)

    except Exception as e:
        st.error(f"Generation failed: {e}")

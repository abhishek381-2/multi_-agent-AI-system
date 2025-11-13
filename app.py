import streamlit as st
from reader import extract_and_clean_text
from ai_agents import generate_flashcards, generate_quizzes, generate_summary, answer_doubt
from planner import create_revision_plan
from localization import TEXTS  # Import the texts
import firestore_db  # Import the new Firestore logic
from gtts import gTTS
import json
import base64
import io

# --- Page Config ---
# 'localization.py' se text load karein
# Default language 'en' (English) set karein
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'

# Function to get text based on language
def get_text(key):
    return TEXTS[st.session_state.lang].get(key, f"Missing key: {key}")

# Set page config
st.set_page_config(
    layout="wide",
    page_title=get_text("page_title"),
    page_icon=get_text("page_icon") # 🎓
)

# --- Zoned UI Styling (CSS) - DARK MODE THEME ---
st.markdown(f"""
<style>
    /* --- Dark Mode Palette --- */
    /* Background: #1E293B (Slate-800) */
    /* Surface/Card: #334155 (Slate-700) */
    /* Primary Color: #22D3EE (Cyan-400) */
    /* Text Color: #F8FAFC (Slate-50) */

    /* --- Main Canvas (Background) --- */
    [data-testid="stAppViewContainer"] {{
        background-color: #1E293B; /* Dark Blue/Slate-800 */
        color: #F8FAFC; /* Light Text */
    }}
    
    /* --- Sidebar --- */
    [data-testid="stSidebar"] {{
        background-color: #0F172A; /* Slate-900 (Darker) */
        border-right: 1px solid #334155; /* Slate-700 */
        padding: 1.5rem;
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {{
        color: #FFFFFF; /* White */
        font-size: 1.75rem;
        font-weight: 700;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
    [data-testid="stSidebar"] .st-emotion-cache-1jicfl2, 
    [data-testid="stSidebar"] .st-emotion-cache-nahz7x,
    [data-testid="stSidebar"] label {{
        color: #94A3B8; /* Slate-400 */
    }}
    
    /* --- Main Content Area --- */
    .main .block-container {{
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}
    
    /* --- Custom "Card" Container --- */
    .card {{
        background-color: #334155; /* Dark Slate-700 */
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.5); /* Stronger dark shadow */
        border: 1px solid #475569; /* Slate-600 */
        margin-bottom: 1.5rem;
    }}
    
    /* --- Headings --- */
    h1, h2, h3 {{
        color: #FFFFFF; /* White Text */
        font-weight: 600;
    }}
    
    /* --- Buttons --- */
    .stButton > button {{
        font-weight: 600;
        border-radius: 0.5rem;
        padding: 0.5em 1em;
        transition: all 0.2s ease;
        border: none;
    }}
    .stButton > button[kind="primary"] {{
        background-color: #22D3EE; /* Cyan-400 (Primary Action) */
        color: #0F172A; /* Dark Text on Primary */
    }}
    .stButton > button[kind="primary"]:hover {{
        background-color: #06B6D4; /* Cyan-500 */
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
    }}
    .stButton > button[kind="secondary"] {{
        background-color: #475569; /* Slate-600 */
        color: #F8FAFC; /* Light Text */
        border: 1px solid #64748B; /* Slate-500 */
    }}
    .stButton > button[kind="secondary"]:hover {{
        background-color: #64748B; /* Slate-500 */
        color: #FFFFFF;
    }}

    /* --- Input Fields (Text/Uploader/Selectbox) --- */
    .stTextInput>div>div>input, 
    .stFileUploader>section,
    .stSelectbox>div>div {{
        background-color: #475569; /* Slate-600 input background */
        color: #F8FAFC; 
        border: 1px solid #64748B;
    }}
    
    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        border-bottom: 2px solid #475569; /* Slate-600 */
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        color: #94A3B8; /* Slate-400 (Inactive tab text) */
        font-weight: 500;
        border-bottom: 2px solid transparent;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        color: #22D3EE; /* Cyan-400 (Active tab text) */
        border-bottom: 2px solid #22D3EE;
    }}
    
    /* --- Expander (Flashcards) --- */
    [data-testid="stExpander"] {{
        background-color: #475569; /* Slate-600 */
        border: 1px solid #64748B; /* Slate-500 */
        border-radius: 0.5rem;
    }}
    [data-testid="stExpander"] summary {{
        color: #FFFFFF; /* White */
        font-size: 1.1em;
        font-weight: 500;
    }}
    
    /* --- Metrics (Dashboard) --- */
    [data-testid="stMetric"] {{
        background-color: #475569; /* Slate-600 */
        border: 1px solid #64748B; /* Slate-500 */
        border-radius: 0.75rem;
        padding: 1rem;
    }}
    [data-testid="stMetricLabel"] {{
        color: #94A3B8; /* Slate-400 */
        font-size: 0.9rem;
    }}
    [data-testid="stMetricValue"] {{
        color: #22D3EE; /* Cyan-400 */
        font-size: 2rem;
        font-weight: 700;
    }}

    /* Ensure other text/info boxes look good */
    .stAlert, .stNotification {{
        color: #0F172A !important;
    }}
    .stAlert-success, .stAlert-info {{
        background-color: #E0F2F1 !important; /* Lighter background for alerts */
    }}
</style>
""", unsafe_allow_html=True)

# --- Audio Generation Function ---
def text_to_audio_b64(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        audio_b64 = base64.b64encode(audio_fp.read()).decode('utf-8')
        return f"data:audio/mp3;base64,{audio_b64}"
    except Exception as e:
        st.error(get_text("flashcards_audio_error").format(error=e))
        return None

# --- Session State Initialization ---
def init_session_state():
    keys = [
        'chunks', 'full_text', 'flashcards', 'quizzes', 'summary', 
        'plan', 'quiz_score', 'total_questions', 'current_set_name'
    ]
    for key in keys:
        if key not in st.session_state:
            if key.endswith('s') or key == 'plan':
                st.session_state[key] = []
            elif key.endswith('score') or key == 'total_questions':
                st.session_state[key] = 0
            else:
                st.session_state[key] = None

init_session_state()

# --- Sidebar UI ---
with st.sidebar:
    st.title(f"{get_text('page_icon')} {get_text('sidebar_title')}")
    st.markdown(get_text('sidebar_subtitle'))
    
    # Language Selector
    lang_choice = st.radio(
        get_text("select_language"), 
        options=['en', 'hi'], 
        format_func=lambda x: "English (US)" if x == 'en' else "हिन्दी (Hindi)",
        horizontal=True,
    )
    if st.session_state.lang != lang_choice:
        st.session_state.lang = lang_choice
        st.rerun() # Rerun to apply new language
    
    st.divider()

    st.header(get_text("upload_header"))
    uploaded_file = st.file_uploader(
        get_text("upload_label"),
        type="pdf",
        on_change=init_session_state # Reset on new file
    )
    
    if uploaded_file:
        st.session_state.current_set_name = uploaded_file.name.replace('.pdf', '')
        st.success(get_text("upload_success").format(filename=uploaded_file.name))

        if st.button(get_text("generate_button"), type="primary", use_container_width=True):
            with st.spinner(get_text("spinner_generating")):
                
                # Step 1: Reader Agent
                st.session_state.chunks = extract_and_clean_text(uploaded_file)
                st.session_state.full_text = "\n\n".join(st.session_state.chunks)
                
                if not st.session_state.chunks:
                    st.error(get_text("error_no_text"))
                else:
                    st.info(f"{len(st.session_state.chunks)} {get_text('metric_topics')}")
                    
                    all_flashcards = []
                    all_quizzes = []
                    all_summaries = []
                    topic_names = []
                    
                    # Process each chunk
                    progress_bar = st.progress(0, text=get_text("spinner_processing_chunk").format(i=0, total=len(st.session_state.chunks)))
                    for i, chunk in enumerate(st.session_state.chunks):
                        progress_bar.progress((i+1)/len(st.session_state.chunks), text=get_text("spinner_processing_chunk").format(i=i+1, total=len(st.session_state.chunks)))
                        all_flashcards.extend(generate_flashcards(chunk))
                        all_quizzes.extend(generate_quizzes(chunk))
                        all_summaries.append(generate_summary(chunk))
                        topic_names.append(f"Topic Chunk {i+1}")
                    
                    st.session_state.flashcards = all_flashcards
                    st.session_state.quizzes = all_quizzes
                    st.session_state.summary = "\n\n---\n\n".join(all_summaries)
                    
                    # Step 4: Planner Agent
                    st.session_state.plan = create_revision_plan(topic_names)
                    
                    # Reset Quiz Score
                    st.session_state.quiz_score = 0
                    st.session_state.total_questions = len(st.session_state.quizzes)
            
            if not st.session_state.flashcards and not st.session_state.quizzes:
                st.error(get_text("error_no_generation"))
            else:
                st.success(f"✨ {get_text('upload_success').format(filename=st.session_state.current_set_name)}")
                
    st.divider()
    
    # --- My Library (Sidebar) ---
    st.header(get_text("library_header"))
    st.markdown(get_text("library_subheader"))
    
    try:
        saved_sets = firestore_db.load_all_study_sets()
        
        if not saved_sets:
            st.info(get_text("library_empty"))
        else:
            set_options = {s['name']: s['id'] for s in saved_sets}
            selected_set_name = st.selectbox(get_text("library_select"), options=set_options.keys())
            
            if st.button(get_text("library_load_button"), use_container_width=True):
                with st.spinner(f"Loading '{selected_set_name}'..."):
                    set_id_to_load = set_options[selected_set_name]
                    loaded_data = firestore_db.load_set_by_id(set_id_to_load)
                    
                    if loaded_data:
                        st.session_state.current_set_name = loaded_data["set_name"]
                        st.session_state.flashcards = loaded_data["flashcards"]
                        st.session_state.quizzes = loaded_data["quizzes"]
                        st.session_state.summary = loaded_data["summary"]
                        st.session_state.plan = create_revision_plan([f"Topic {i+1}" for i in range(len(loaded_data.get("flashcards", [])))]) # Simple plan
                        st.session_state.quiz_score = 0
                        st.session_state.total_questions = len(loaded_data.get("quizzes", []))
                        st.session_state.full_text = loaded_data.get("summary", "") # Use summary as context for loaded sets
                        st.session_state.chunks = [loaded_data.get("summary", "")]
                        st.success(get_text("library_load_success").format(set_name=loaded_data['set_name']))
                    else:
                        st.error(get_text("library_load_error"))

    except Exception as e:
        st.error(f"Error connecting to Firebase: {e}. Is 'serviceAccountKey.json' correct?")


# --- Main Content Area ---
if not st.session_state.flashcards and not st.session_state.chunks:
    # --- Welcome Screen ---
    st.markdown(f"""
    <div class="card" style="text-align: center; padding: 3rem;">
        <h1>{get_text("welcome_header")}</h1>
        <p style="font-size: 1.1rem; color: #94A3B8;">{get_text("welcome_subheader")}</p>
    </div>
    """, unsafe_allow_html=True)

else:
    # --- Dashboard Card ---
    with st.container():
        st.markdown(f"<h3>{get_text('dashboard_header').format(set_name=st.session_state.current_set_name)}</h3>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(get_text("metric_topics"), len(st.session_state.chunks) if st.session_state.chunks else "N/A")
        col2.metric(get_text("metric_flashcards"), len(st.session_state.flashcards))
        col3.metric(get_text("metric_quizzes"), len(st.session_state.quizzes))
        col4.metric(get_text("metric_score"), f"{st.session_state.quiz_score}/{st.session_state.total_questions}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Main Tabs Card ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    tab_names = [
        get_text("tab_plan"),
        get_text("tab_flashcards"),
        get_text("tab_quiz"),
        get_text("tab_summary"),
        get_text("tab_doubt"),
        get_text("tab_library")
    ]
    tabs = st.tabs(tab_names)
    
    # --- Tab 1: Revision Plan ---
    with tabs[0]:
        st.header(get_text("plan_header"))
        if st.session_state.plan:
            edited_plan = st.data_editor(
                st.session_state.plan,
                num_rows="dynamic",
                column_config={
                    "topic": st.column_config.TextColumn(get_text("plan_col_topic"), disabled=True),
                    "revise_on": st.column_config.TextColumn(get_text("plan_col_date"), disabled=True),
                    "status": st.column_config.CheckboxColumn(get_text("plan_col_status"), default=False)
                },
                use_container_width=True
            )
            st.session_state.plan = edited_plan
        else:
            st.info(get_text("plan_no_plan"))
    
    # --- Tab 2: Flashcards ---
    with tabs[1]:
        st.header(get_text("flashcards_header"))
        if st.session_state.flashcards:
            st.download_button(
                label=get_text("flashcards_download"),
                data=json.dumps(st.session_state.flashcards, indent=2),
                file_name=f"{st.session_state.current_set_name}_flashcards.json",
                mime="application/json",
            )
            st.markdown("---")
            
            for i, card in enumerate(st.session_state.flashcards):
                if isinstance(card, dict) and 'question' in card and 'answer' in card:
                    with st.expander(f"**Q: {card['question']}**"):
                        st.markdown(f"**A:** {card['answer']}")
                        
                        if st.button(get_text("flashcards_play_audio"), key=f"play_q_{i}"):
                            # Note: The audio player will show up below the button in the expander
                            audio_b64 = text_to_audio_b64(f"{card['question']}. {card['answer']}", st.session_state.lang)
                            if audio_b64:
                                st.audio(audio_b64, format="audio/mp3")
                else:
                    st.warning(get_text("flashcards_invalid").format(card=card))
        else:
            st.info(get_text("flashcards_no_cards"))

    # --- Tab 3: Quiz Time ---
    with tabs[2]:
        st.header(get_text("quiz_header"))
        if st.session_state.quizzes:
            st.download_button(
                label=get_text("quiz_download"),
                data=json.dumps(st.session_state.quizzes, indent=2),
                file_name=f"{st.session_state.current_set_name}_quiz.json",
                mime="application/json",
            )
            
            if st.button(get_text("quiz_reset_score")):
                st.session_state.quiz_score = 0
                for key in list(st.session_state.keys()):
                    # Reset all quiz related session keys
                    if key.startswith("scored_") or key.startswith("check_") or key.startswith("quiz_"):
                        del st.session_state[key]
                st.rerun()
            
            st.markdown("---")
            
            for i, quiz in enumerate(st.session_state.quizzes):
                if isinstance(quiz, dict) and 'question' in quiz and 'options' in quiz and 'answer' in quiz:
                    st.subheader(f"Q{i+1}: {quiz['question']}")
                    
                    options = quiz['options']
                    if not isinstance(options, list):
                        options = [str(opt) for opt in options]
                    
                    # Ensure radio button index state is maintained or reset correctly
                    user_choice_key = f"quiz_{i}"
                    
                    user_choice = st.radio(
                        get_text("quiz_options_for").format(i=i+1), 
                        options, 
                        key=user_choice_key,
                        index=None # Important: Start with no selection
                    )
                    
                    answer = quiz['answer']
                    
                    if f"check_{i}" not in st.session_state:
                        st.session_state[f"check_{i}"] = False
                    
                    # Define current score state
                    scored_key = f"scored_{i}"
                    
                    if st.button(get_text("quiz_check_answer").format(i=i+1), key=f"btn_{i}"):
                        st.session_state[f"check_{i}"] = True
                        if user_choice == answer:
                            st.success(get_text("quiz_correct").format(answer=answer))
                            if scored_key not in st.session_state:
                                st.session_state.quiz_score += 1
                                st.session_state[scored_key] = True # Mark as checked/scored
                        else:
                            st.error(get_text("quiz_incorrect").format(answer=answer))
                            # Only mark as scored if we want to prevent future scoring attempts
                            if scored_key not in st.session_state:
                                st.session_state[scored_key] = True
                    
                    # Display feedback if the user has already checked the answer
                    elif st.session_state[f"check_{i}"]:
                        if user_choice is not None:
                            if user_choice == answer:
                                st.success(get_text("quiz_correct").format(answer=answer))
                            else:
                                st.error(get_text("quiz_incorrect").format(answer=answer))
                        else:
                            # Show correct answer if checked but no option selected
                            st.info(f"The correct answer was: **{answer}**")
                    
                    st.divider()
                else:
                    st.warning(get_text("quiz_invalid").format(quiz=quiz))
        else:
            st.info(get_text("quiz_no_quiz"))

    # --- Tab 4: Summary ---
    with tabs[3]:
        st.header(get_text("summary_header"))
        if st.session_state.summary:
            st.markdown(st.session_state.summary)
        else:
            st.info(get_text("summary_no_summary"))

    # --- Tab 5: Doubt Agent ---
    with tabs[4]:
        st.header(get_text("doubt_header"))
        if st.session_state.full_text:
            user_question = st.text_input(get_text("doubt_prompt"))
            if st.button(get_text("doubt_button"), key="doubt_ask"):
                if user_question:
                    with st.spinner(get_text("doubt_spinner")):
                        answer = answer_doubt(st.session_state.full_text, user_question)
                        st.markdown(answer)
                else:
                    st.warning(get_text("doubt_no_question"))
        else:
            st.info(get_text("doubt_no_context"))

    # --- Tab 6: My Library (Main Tab) ---
    with tabs[5]:
        st.header(get_text("library_main_header"))
        st.markdown(get_text("library_main_subheader"))
        
        # Check if saved_sets is available from the sidebar logic
        if 'saved_sets' not in locals():
            try:
                saved_sets = firestore_db.load_all_study_sets()
            except Exception:
                saved_sets = []
                
        if st.session_state.flashcards or st.session_state.quizzes:
            if st.button(get_text("library_save_button"), type="primary"):
                try:
                    with st.spinner(get_text("spinner_saving")):
                        firestore_db.save_study_set(
                            st.session_state.current_set_name,
                            st.session_state.flashcards,
                            st.session_state.quizzes,
                            st.session_state.summary
                        )
                    st.success(get_text("library_save_success").format(set_name=st.session_state.current_set_name))
                    saved_sets = firestore_db.load_all_study_sets() # Refresh the list
                except Exception as e:
                    st.error(get_text("library_save_error").format(error=e))
        else:
            st.warning(get_text("library_no_data"))
            
        st.divider()
        st.subheader(get_text("library_view_sets"))
        
        if not saved_sets:
            st.info(get_text("library_empty"))
        else:
            for s in saved_sets:
                # Add a visually distinct container for saved sets
                with st.container(border=True):
                    col_name, col_id = st.columns([3, 1])
                    col_name.markdown(f"**{s['name']}**")
                    col_id.markdown(f"*(ID: {s['id']})*")
                
    st.markdown('</div>', unsafe_allow_html=True) # Close the main tabs card
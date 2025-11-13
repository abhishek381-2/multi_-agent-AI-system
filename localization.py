# localization.py

# Is file mein app ka saara text (UI labels) store hai taaki hum language badal sakein.
# Hum yahan icons bhi store kar rahe hain taaki unhe ek jagah se badla ja sake.

TEXTS = {
    "en": {
        # --- Sidebar ---
        "page_title": "AI Study Assistant",
        "page_icon": "🎓",
        "sidebar_title": "AI Co-Pilot",
        "sidebar_subtitle": "Offline Mode using Ollama",
        "select_language": "Choose Language",
        "upload_header": "1. Upload Your Notes",
        "upload_label": "Upload your study notes (PDF)",
        "upload_success": "File '{filename}' loaded!",
        "generate_button": "✨ Generate Study Material",
        "library_header": "2. My Study Library",
        "library_subheader": "Load previously saved study sets.",
        "library_empty": "Your library is empty. Generate and save some study material!",
        "library_select": "Select a study set to load",
        "library_load_button": "Load Set",
        "library_load_success": "Loaded '{set_name}'!",
        "library_load_error": "Could not load the selected set.",

        # --- Welcome Screen ---
        "welcome_header": "🎓 Welcome to your AI Study Co-Pilot",
        "welcome_subheader": "Upload a PDF using the sidebar on the left to get started.",

        # --- Dashboard ---
        "dashboard_header": "Dashboard: {set_name}",
        "metric_topics": "Total Topics (Chunks)",
        "metric_flashcards": "Generated Flashcards",
        "metric_quizzes": "Generated Quizzes",
        "metric_score": "Your Quiz Score",

        # --- Tabs ---
        "tab_plan": "📅 Revision Plan",
        "tab_flashcards": "🃏 Flashcards",
        "tab_quiz": "❓ Quiz Time",
        "tab_summary": "📝 Summary",
        "tab_doubt": "💬 Doubt Agent",
        "tab_library": "📚 My Library",

        # --- Plan Tab ---
        "plan_header": "Your Smart Revision Plan",
        "plan_col_topic": "Topic",
        "plan_col_date": "Revise On",
        "plan_col_status": "Status",
        "plan_no_plan": "No revision plan generated. Upload a PDF and click 'Generate'.",

        # --- Flashcards Tab ---
        "flashcards_header": "Generated Flashcards",
        "flashcards_download": "📥 Download Flashcards (JSON)",
        "flashcards_play_audio": "🔊 Play Audio",
        "flashcards_no_cards": "No flashcards generated. Upload a PDF and click 'Generate'.",
        "flashcards_invalid": "An invalid flashcard format was received: {card}",
        "flashcards_audio_error": "Could not generate audio: {error}",

        # --- Quiz Tab ---
        "quiz_header": "Quiz Time",
        "quiz_download": "📥 Download Quiz (JSON)",
        "quiz_reset_score": "Reset Score",
        "quiz_options_for": "Options for Q{i}",
        "quiz_check_answer": "Check Answer Q{i}",
        "quiz_correct": "Correct! The answer is: {answer}",
        "quiz_incorrect": "Incorrect. The correct answer is: {answer}",
        "quiz_no_quiz": "No quiz generated. Upload a PDF and click 'Generate'.",
        "quiz_invalid": "An invalid quiz format was received: {quiz}",

        # --- Summary Tab ---
        "summary_header": "Generated Summary",
        "summary_no_summary": "No summary generated. Upload a PDF and click 'Generate'.",

        # --- Doubt Tab ---
        "doubt_header": "💬 Doubt Agent: Ask Your Notes",
        "doubt_prompt": "What is your question about the document?",
        "doubt_button": "Ask Question",
        "doubt_spinner": "Finding answer in your document...",
        "doubt_no_question": "Please enter a question.",
        "doubt_no_context": "Please upload and process a PDF first to ask questions about it.",

        # --- Library Tab (Main) ---
        "library_main_header": "📚 My Study Library",
        "library_main_subheader": "Save your currently generated material to your persistent cloud library.",
        "library_save_button": "Save Current Set to Library",
        "library_save_success": "'{set_name}' saved to your library!",
        "library_save_error": "Could not save set: {error}",
        "library_no_data": "No study material generated yet. Click 'Generate' first.",
        "library_view_sets": "View Saved Study Sets",

        # --- Spinners / Loaders ---
        "spinner_generating": "Offline AI Agents are working... (This may take a moment)",
        "spinner_processing_chunk": "Processing chunk {i}/{total}...",
        "spinner_saving": "Saving to Firebase...",
        
        # --- Errors ---
        "error_no_text": "Could not extract any readable text from the PDF.",
        "error_no_generation": "Processing complete, but no Flashcards or Quizzes were generated. Please check your Ollama server connection and the PDF content.",
    },
    
    # =================================================================================
    # --- HINDI TRANSLATIONS ---
    # =================================================================================
    
    "hi": {
        # --- Sidebar ---
        "page_title": "एआई स्टडी असिस्टेंट",
        "page_icon": "🎓",
        "sidebar_title": "एआई को-पायलट",
        "sidebar_subtitle": "ऑफलाइन मोड (Ollama)",
        "select_language": "भाषा चुनें",
        "upload_header": "1. अपने नोट्स अपलोड करें",
        "upload_label": "अपने स्टडी नोट्स (PDF) यहां अपलोड करें",
        "upload_success": "फ़ाइल '{filename}' लोड हो गई!",
        "generate_button": "✨ स्टडी मटेरियल जेनरेट करें",
        "library_header": "2. मेरी स्टडी लाइब्रेरी",
        "library_subheader": "पहले से सहेजे गए स्टडी सेट लोड करें।",
        "library_empty": "आपकी लाइब्रेरी खाली है। कुछ स्टडी मटेरियल जेनरेट करें और सहेजें!",
        "library_select": "लोड करने के लिए एक स्टडी सेट चुनें",
        "library_load_button": "सेट लोड करें",
        "library_load_success": "'{set_name}' लोड हो गया!",
        "library_load_error": "चुना हुआ सेट लोड नहीं किया जा सका।",

        # --- Welcome Screen ---
        "welcome_header": "🎓 आपके एआई स्टडी को-पायलट में आपका स्वागत है",
        "welcome_subheader": "शुरू करने के लिए बाईं ओर दिए गए साइडबार का उपयोग करके एक PDF अपलोड करें।",

        # --- Dashboard ---
        "dashboard_header": "डैशबोर्ड: {set_name}",
        "metric_topics": "कुल विषय (Chunks)",
        "metric_flashcards": "जेनरेटेड फ्लैशकार्ड",
        "metric_quizzes": "जेनरेटेड क्विज़",
        "metric_score": "आपका क्विज़ स्कोर",

        # --- Tabs ---
        "tab_plan": "📅 रिवीज़न प्लान",
        "tab_flashcards": "🃏 फ्लैशकार्ड",
        "tab_quiz": "❓ क्विज़ टाइम",
        "tab_summary": "📝 सारांश",
        "tab_doubt": "💬 डाउट एजेंट",
        "tab_library": "📚 मेरी लाइब्रेरी",

        # --- Plan Tab ---
        "plan_header": "आपका स्मार्ट रिवीज़न प्लान",
        "plan_col_topic": "विषय",
        "plan_col_date": "रिवीज़न तिथि",
        "plan_col_status": "स्थिति",
        "plan_no_plan": "कोई रिवीज़न प्लान जेनरेट नहीं हुआ। PDF अपलोड करें और 'जेनरेट करें' पर क्लिक करें।",

        # --- Flashcards Tab ---
        "flashcards_header": "जेनरेटेड फ्लैशकार्ड",
        "flashcards_download": "📥 फ्लैशकार्ड डाउनलोड करें (JSON)",
        "flashcards_play_audio": "🔊 ऑडियो चलाएं",
        "flashcards_no_cards": "कोई फ्लैशकार्ड जेनरेट नहीं हुआ। PDF अपलोड करें और 'जेनरेट करें' पर क्लिक करें।",
        "flashcards_invalid": "एक अमान्य फ्लैशकार्ड प्रारूप प्राप्त हुआ: {card}",
        "flashcards_audio_error": "ऑडियो जेनरेट नहीं किया जा सका: {error}",

        # --- Quiz Tab ---
        "quiz_header": "क्विज़ टाइम",
        "quiz_download": "📥 क्विज़ डाउनलोड करें (JSON)",
        "quiz_reset_score": "स्कोर रीसेट करें",
        "quiz_options_for": "Q{i} के लिए विकल्प",
        "quiz_check_answer": "उत्तर जांचें Q{i}",
        "quiz_correct": "सही! सही उत्तर है: {answer}",
        "quiz_incorrect": "गलत। सही उत्तर है: {answer}",
        "quiz_no_quiz": "कोई क्विज़ जेनरेट नहीं हुआ। PDF अपलोड करें और 'जेनरेट करें' पर क्लिक करें।",
        "quiz_invalid": "एक अमान्य क्विज़ प्रारूप प्राप्त हुआ: {quiz}",

        # --- Summary Tab ---
        "summary_header": "जेनरेटेड सारांश",
        "summary_no_summary": "कोई सारांश जेनरेट नहीं हुआ। PDF अपलोड करें और 'जेनरेट करें' पर क्लिक करें।",

        # --- Doubt Tab ---
        "doubt_header": "💬 डाउट एजेंट: अपने नोट्स से सवाल पूछें",
        "doubt_prompt": "दस्तावेज़ के बारे में आपका क्या सवाल है?",
        "doubt_button": "सवाल पूछें",
        "doubt_spinner": "आपके दस्तावेज़ में जवाब ढूंढा जा रहा है...",
        "doubt_no_question": "कृपया एक सवाल दर्ज करें।",
        "doubt_no_context": "सवाल पूछने के लिए कृपया पहले एक PDF अपलोड और प्रोसेस करें।",

        # --- Library Tab (Main) ---
        "library_main_header": "📚 मेरी स्टडी लाइब्रेरी",
        "library_main_subheader": "अपने वर्तमान में जेनरेट किए गए मटेरियल को अपनी स्थायी क्लाउड लाइब्रेरी में सहेजें।",
        "library_save_button": "वर्तमान सेट को लाइब्रेरी में सहेजें",
        "library_save_success": "'{set_name}' आपकी लाइब्रेरी में सहेजा गया!",
        "library_save_error": "सेट सहेजा नहीं जा सका: {error}",
        "library_no_data": "अभी तक कोई स्टडी मटेरियल जेनरेट नहीं हुआ है। पहले 'जेनरेट करें' पर क्लिक करें।",
        "library_view_sets": "सहेजे गए स्टडी सेट देखें",
        
        # --- Spinners / Loaders ---
        "spinner_generating": "ऑफलाइन एआई एजेंट्स काम कर रहे हैं... (इसमें थोड़ा समय लग सकता है)",
        "spinner_processing_chunk": "प्रोसेसिंग चंक {i}/{total}...",
        "spinner_saving": "फायरबेस में सहेजा जा रहा है...",
        
        # --- Errors ---
        "error_no_text": "PDF से कोई भी पढ़ने योग्य टेक्स्ट नहीं निकाला जा सका।",
        "error_no_generation": "प्रोसेसिंग पूरी हुई, लेकिन कोई फ्लैशकार्ड या क्विज़ जेनरेट नहीं हुआ। कृपया अपने Ollama सर्वर कनेक्शन और PDF कंटेंट की जांच करें।",
    }
}
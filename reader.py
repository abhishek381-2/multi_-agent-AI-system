import fitz  # PyMuPDF

def extract_and_clean_text(pdf_file):
    """
    Ek PDF file se text extract karta hai aur use clean chunks mein return karta hai.
    """
    # PDF ko stream se open karein
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    doc.close()
    
    # Text ko paragraphs ya sections mein split karein
    chunks = full_text.split("\n\n")
    cleaned_chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 100] 
    
    if not cleaned_chunks or len(cleaned_chunks) < 2:
        # Agar splitting se kuch na mile (ya sirf 1 hi chunk bane), 
        # to text ko 1500 characters ke chhote hisso mein zabardasti baantein
        split_size = 1500
        force_split = [full_text[i:i+split_size] for i in range(0, len(full_text), split_size)]
        
        # In naye chunks ko bhi clean karein
        cleaned_chunks = [chunk.strip() for chunk in force_split if len(chunk.strip()) > 100]
        
    return cleaned_chunks
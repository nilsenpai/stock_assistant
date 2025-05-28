def clean_response(text: str) -> str:
    """
    Cleans Gemini response by removing markdown, bullet points, and formatting for voice output.
    """
    import re

    # Remove markdown formatting
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)      # italics
    text = re.sub(r"`(.*?)`", r"\1", text)        # code
    text = re.sub(r"#+", "", text)                # headers
    text = re.sub(r"\n{2,}", "\n", text)          # extra line breaks
    text = re.sub(r"[-*•]\s+", "", text)          # bullet points
    text = text.strip()

    return text

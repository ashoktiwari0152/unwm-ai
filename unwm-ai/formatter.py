# ============================================
# UNWM Formatter
# ============================================

def format_response(ai_text, topic):

    final_output = f"""
# Universal Narrative Wisdom Model © UNWM

## Topic:
{topic}

---

{ai_text}
"""

    return final_output
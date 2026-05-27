def recursive_analysis(user_input):

    text = user_input.lower()

    recursive_keywords = [
        "recursive",
        "collapse",
        "instability",
        "meta",
        "anti",
        "non",
        "self",
        "origin",
        "generative",
        "construct",
        "formal",
        "axiom",
        "system",
        "cogniz",
        "knowability"
    ]

    detected_patterns = []

    score = 0

    for keyword in recursive_keywords:

        count = text.count(keyword)

        if count > 0:

            detected_patterns.append(
                f"{keyword} detected ({count})"
            )

            score += count

    recursion_density = min(score / 10, 1.0)

    collapse_risk = min(
        recursion_density * 1.4,
        1.0
    )

    stability_index = max(
        1.0 - collapse_risk,
        0.0
    )

    if collapse_risk > 0.7:
        state = "recursive destabilization"

    elif collapse_risk > 0.4:
        state = "recursive escalation"

    else:
        state = "recursive stability"

    result = {

        "recursive_state": state,

        "collapse_risk": round(
            collapse_risk,
            3
        ),

        "stability_index": round(
            stability_index,
            3
        ),

        "recursive_density": round(
            recursion_density,
            3
        ),

        "patterns_detected": detected_patterns,

        "meta_analysis": {

            "self_reference_detected":
            "self" in text,

            "anti_recursive_detected":
            "anti" in text,

            "non_recursive_detected":
            "non" in text,

            "collapse_dynamics_detected":
            "collapse" in text
        }
    }

    return result

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
        "formula",
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

    recursive_density = round(score / 10, 2)

    collapse_risk = round(
        min(score / 10, 1),
        2
    )

    stability_index = round(
        max(1 - collapse_risk, 0),
        2
    )

    if collapse_risk > 0.7:

        recursive_state =
        "recursive destabilization"

    elif collapse_risk > 0.4:

        recursive_state =
        "recursive fluctuation"

    else:

        recursive_state =
        "active"

    return {

        "recursive_state":
        recursive_state,

        "collapse_risk":
        collapse_risk,

        "stability_index":
        stability_index,

        "recursive_density":
        recursive_density,

        "patterns_detected":
        detected_patterns,

        "meta_analysis": {

            "self_reference_detected":
            "self" in text,

            "meta_layer_detected":
            "meta" in text,

            "anti_structure_detected":
            "anti" in text
        }
    }

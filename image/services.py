from collections import Counter
import re


def generate_placeholder_tags(image):
    text_parts = [image.name, image.alt_text, image.prn]
    if image.partner_id:
        text_parts.append(image.partner_id)
    source = " ".join(part for part in text_parts if part).lower()
    tokens = re.findall(r"[a-z0-9]+", source)

    stop_words = {
        "jpg",
        "jpeg",
        "png",
        "webp",
        "prn",
        "campsite",
        "motorhome",
        "image",
    }
    filtered = [token for token in tokens if len(token) > 2 and token not in stop_words]
    counter = Counter(filtered)

    tags = []
    for index, (token, _) in enumerate(counter.most_common(5)):
        confidence = max(0.5, round(0.95 - (index * 0.08), 2))
        tags.append({"key": token, "confidence": confidence})
    return tags

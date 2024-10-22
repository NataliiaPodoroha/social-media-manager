from better_profanity import profanity


profanity.load_censor_words()


def moderate_text(text: str) -> bool:
    return not profanity.contains_profanity(text)

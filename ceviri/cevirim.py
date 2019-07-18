def try_to_guess(attr, possible_words, language):
    if language == "tr":
        pass
    
def cevirim(obj, attr, language):
    attrs = attr.split("_")
    possible_words = [*attr.split("_") for attr in dir(obj)]
    
    new_attrs = []
    for attr in attrs:
        new_attrs.append(try_to_guess(attr, possible_words, language) or attr)
    
    return levenshtein(dir(obj), attr)

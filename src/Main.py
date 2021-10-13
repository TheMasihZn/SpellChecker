import pyttsx3

engine = pyttsx3.init()

txt = '''centuries innovative puzzles transmission until correlation current immediately syndromes seizures migraines 
trigger concurrent unnecessary encouraged infancy eager innovative Transactions characteristics fundamentals 
reinforcing curriculum Realizing skimming entry maintenance '''

signs = [',', '.', '\'', '\"', '/', '\n', '"', '‘',  '“', '’', '?', '(', ')', '°C', '°F', '°', '%', '$', '#', '', '[',
         ']', ';']


def filter_and_get_word_list(text, _signs):
    for sign in _signs:
        text = text.replace(sign, "")
    _words = [_word for _word in text.lower().strip().split(' ') if len(_word) > 3 and not _word.isnumeric()]
    return _words


def get_good_words(_words):
    counts = {}
    for _word in _words:
        if _word not in counts:
            counts[_word] = 0
        counts[_word] += 1

    threshold_value = max(counts.values()) * 0.5

    _results = [_word for _word in counts.keys() if counts[_word] < threshold_value]
    return _results


def _say(_word):
    engine.say(_word)
    engine.runAndWait()


def _spell(_word, error: list, short=False):
    if short:
        _say(f'you missed {[_word[l] for l in error]}')
        return
    _say(f'{_word} is spelled {[l for l in _word]}')


def get_and_check(_word, first_time=False):
    is_correct = False
    _say(_word)
    stroke = input('')

    _mistakes = []
    for i, letter in enumerate(_word):
        if len(stroke) >= i + 1:
            if letter == stroke[i]:
                continue
        _mistakes.append(i)

    if len(_mistakes) == 0:
        is_correct = True
    else:
        print(_word)
        _spell(_word, _mistakes, not first_time)
    return is_correct


def loop_till_fixed(_word):
    while True:
        errors = []
        for i in range(3):
            error = get_and_check(_word)
            errors.append(0 if error else 1)

        error_rate = sum(errors) / len(errors)
        if error_rate < 0.4:
            break


def filter_history(history, mistakes, new_words):
    tmp = []
    for _word in new_words:
        if history.count(_word) == 0 and mistakes.count(_word) == 0:
            tmp.append(_word)
    return tmp


def write_to_dictionary(_word):
    writable_dictionary = open("dictionary.text", "a")
    writable_dictionary.write('\n' + _word)
    writable_dictionary.close()


def write_to_mistakes(_word):
    record = open('mistakes.text', "a")
    record.write('\n' + _word)
    record.close()


def init():
    raw_word_list = filter_and_get_word_list(txt, signs)
    good_words = get_good_words(raw_word_list)
    history = open("dictionary.text", 'r').read()
    mistakes = open('mistakes.text', 'r').read()

    history = history.split('\n')
    mistakes = mistakes.split('\n')
    return good_words, history, mistakes


def main():
    good_words, history, mistakes = init()
    new_words = filter_history(history, mistakes, good_words)
    for word in new_words:
        is_correct = get_and_check(word, first_time=True)
        if is_correct:
            write_to_dictionary(word)

        else:
            write_to_mistakes(word)
            loop_till_fixed(word)


main()
_say("that's all for today, bye")

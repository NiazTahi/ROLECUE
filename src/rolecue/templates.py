from __future__ import annotations

from dataclasses import dataclass


COLORS = ("red", "blue")
ORDERS = ("agent_first", "patient_first")
CASE_RICH_LANGUAGES = ("bn", "de", "ja", "tr")

COLOR_WORDS = {
    "en": {"red": "red", "blue": "blue"},
    "de": {"red": "rot", "blue": "blau"},
    "bn": {"red": "লাল", "blue": "নীল"},
    "tr": {"red": "kırmızı", "blue": "mavi"},
    "ja": {"red": "赤い", "blue": "青い"},
}

VERBS = {
    "de": {
        "kicking": "tritt",
        "pushing": "schubst",
        "chasing": "verfolgt",
        "dragging": "schleift",
    },
    "bn": {
        "kicking": "লাথি মারছেন",
        "pushing": "ধাক্কা দিচ্ছেন",
        "chasing": "তাড়া করছেন",
        "dragging": "টেনে নিয়ে যাচ্ছেন",
    },
    "tr": {
        "kicking": "tekmeliyor",
        "pushing": "itiyor",
        "chasing": "kovalıyor",
        "dragging": "sürüklüyor",
    },
    "ja": {
        "kicking": "蹴っている",
        "pushing": "押している",
        "chasing": "追いかけている",
        "dragging": "引きずっている",
    },
}

ENGLISH_ACTIONS = {
    "kicking": "kicking",
    "pushing": "pushing",
    "chasing": "chasing",
    "dragging": "dragging",
}


@dataclass(frozen=True)
class OptionMap:
    true_label: str
    false_label: str

    def label_for(self, value: bool) -> str:
        return self.true_label if value else self.false_label


def make_option_map(true_is_a: bool) -> OptionMap:
    return OptionMap(true_label="A" if true_is_a else "B", false_label="B" if true_is_a else "A")


def _noun_phrase(language: str, color: str, grammatical_role: str) -> str:
    word = COLOR_WORDS[language][color]
    if language == "de":
        if grammatical_role == "agent":
            return f"der {word} umrandete Mensch"
        return f"den {word} umrandeten Menschen"
    if language == "bn":
        base = f"{word} বাক্স দিয়ে চিহ্নিত ব্যক্তি"
        return base if grammatical_role == "agent" else f"{base}কে"
    if language == "tr":
        base = f"{word.capitalize()} kutuyla işaretlenmiş kişi"
        return base if grammatical_role == "agent" else f"{base}yi"
    if language == "ja":
        particle = "が" if grammatical_role == "agent" else "を"
        return f"{word}枠で囲まれた人{particle}"
    raise KeyError(f"Unsupported case-rich language: {language}")


def make_sentence(language: str, verb: str, case_agent_color: str, order: str) -> str:
    if language not in CASE_RICH_LANGUAGES:
        raise KeyError(f"Unsupported case-rich language: {language}")
    if case_agent_color not in COLORS:
        raise ValueError(case_agent_color)
    if order not in ORDERS:
        raise ValueError(order)
    patient_color = "blue" if case_agent_color == "red" else "red"
    agent = _noun_phrase(language, case_agent_color, "agent")
    patient = _noun_phrase(language, patient_color, "patient")
    first, second = (agent, patient) if order == "agent_first" else (patient, agent)
    action = VERBS[language][verb]
    if language == "de":
        sentence_initial = first[:1].upper() + first[1:]
        return f"{sentence_initial} {action} {second}."
    if language in {"bn", "tr"}:
        punctuation = "।" if language == "bn" else "."
        return f"{first} {second} {action}{punctuation}"
    return f"{first}{second}{action}。"


def make_joint_prompt(
    language: str, sentence: str, options: OptionMap, instruction_style: str
) -> str:
    if instruction_style == "english":
        instruction = (
            "Does the sentence correctly describe who is doing the action to whom in the image? "
            f"{options.true_label}: Yes. {options.false_label}: No. "
            "Answer with only A or B."
        )
        return f'{instruction}\nSentence: "{sentence}"'
    if instruction_style != "native":
        raise ValueError(instruction_style)
    native = {
        "de": (
            "Beschreibt der Satz korrekt, wer im Bild die Handlung an wem ausführt? "
            f"{options.true_label}: Ja. {options.false_label}: Nein. "
            "Antworte nur mit A oder B."
        ),
        "bn": (
            "বাক্যটি কি ছবিতে কে কার ওপর কাজটি করছে তা সঠিকভাবে বর্ণনা করে? "
            f"{options.true_label}: হ্যাঁ। {options.false_label}: না। "
            "শুধু A অথবা B দিয়ে উত্তর দিন।"
        ),
        "tr": (
            "Cümle, görselde eylemi kimin kime yaptığını doğru açıklıyor mu? "
            f"{options.true_label}: Evet. {options.false_label}: Hayır. "
            "Yalnızca A veya B ile yanıtlayın."
        ),
        "ja": (
            "文は、画像内で誰が誰にその動作をしているかを正しく説明していますか。"
            f"{options.true_label}：はい。{options.false_label}：いいえ。"
            "AかBだけで答えてください。"
        ),
    }
    return f'{native[language]}\n"{sentence}"'


def make_text_prompt(
    language: str, sentence: str, options: OptionMap, instruction_style: str
) -> str:
    red_label = options.true_label
    blue_label = options.false_label
    if instruction_style == "english":
        instruction = (
            "According to the sentence, which marked person is performing the action? "
            f"{red_label}: Red. {blue_label}: Blue. Answer with only A or B."
        )
        return f'{instruction}\nSentence: "{sentence}"'
    if instruction_style != "native":
        raise ValueError(instruction_style)
    native = {
        "de": (
            "Welche markierte Person führt laut Satz die Handlung aus? "
            f"{red_label}: Rot. {blue_label}: Blau. Antworte nur mit A oder B."
        ),
        "bn": (
            "বাক্য অনুযায়ী কোন চিহ্নিত ব্যক্তি কাজটি করছেন? "
            f"{red_label}: লাল। {blue_label}: নীল। শুধু A অথবা B দিয়ে উত্তর দিন।"
        ),
        "tr": (
            "Cümleye göre eylemi hangi işaretli kişi yapıyor? "
            f"{red_label}: Kırmızı. {blue_label}: Mavi. Yalnızca A veya B ile yanıtlayın."
        ),
        "ja": (
            "文によると、どちらの枠で囲まれた人が動作をしていますか。"
            f"{red_label}：赤。{blue_label}：青。AかBだけで答えてください。"
        ),
    }
    return f'{native[language]}\n"{sentence}"'


def make_image_prompt(verb: str, options: OptionMap) -> str:
    return (
        f"Which marked person is {ENGLISH_ACTIONS[verb]} the other person? "
        f"{options.true_label}: Red. {options.false_label}: Blue. "
        "Answer with only A or B."
    )

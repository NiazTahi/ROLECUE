"""Draft German and Turkish templates for the controlled robot stimuli.

These strings are deliberately kept separate from the completed v0 experiment.
They must be approved by native speakers before multilingual inference.
"""

from __future__ import annotations

from rolecue.templates import OptionMap


ACTION_FORMS = {
    "de": {
        "photographing": "fotografiert",
        "pushing": "schiebt",
        "kicking": "tritt",
        "pulling": "zieht",
    },
    "tr": {
        "photographing": "fotoğraflıyor",
        "pushing": "itiyor",
        "kicking": "tekmeliyor",
        "pulling": "çekiyor",
    },
}

COLOR_FORMS = {
    "de": {"red": "rot", "blue": "blau"},
    "tr": {"red": "kırmızı", "blue": "mavi"},
}


def _other(color: str) -> str:
    return "blue" if color == "red" else "red"


def make_controlled_sentence(language: str, action: str, agent_color: str, order: str) -> str:
    patient_color = _other(agent_color)
    if language == "de":
        agent = f"der {COLOR_FORMS['de'][agent_color]}e Roboter"
        patient = f"den {COLOR_FORMS['de'][patient_color]}en Roboter"
        first, second = (agent, patient) if order == "agent_first" else (patient, agent)
        first = first[:1].upper() + first[1:]
        return f"{first} {ACTION_FORMS['de'][action]} {second}."
    if language == "tr":
        agent = f"{COLOR_FORMS['tr'][agent_color].capitalize()} robot"
        patient = f"{COLOR_FORMS['tr'][patient_color]} robotu"
        first, second = (agent, patient) if order == "agent_first" else (patient.capitalize(), agent.lower())
        return f"{first} {second} {ACTION_FORMS['tr'][action]}."
    raise KeyError(language)


def make_controlled_image_prompt(action: str, options: OptionMap) -> str:
    return (
        f"Which robot is {action} the other robot? "
        f"{options.true_label}: Red robot. {options.false_label}: Blue robot. "
        "Answer with only A or B."
    )


def make_controlled_text_prompt(
    language: str, sentence: str, options: OptionMap, instruction_style: str
) -> str:
    if instruction_style == "english":
        instruction = (
            "According to the sentence, which robot is performing the action? "
            f"{options.true_label}: Red robot. {options.false_label}: Blue robot. "
            "Answer with only A or B."
        )
        return f'{instruction}\nSentence: "{sentence}"'
    if language == "de":
        instruction = (
            "Welcher Roboter führt laut Satz die Handlung aus? "
            f"{options.true_label}: Der rote Roboter. "
            f"{options.false_label}: Der blaue Roboter. Antworte nur mit A oder B."
        )
    elif language == "tr":
        instruction = (
            "Cümleye göre eylemi hangi robot yapıyor? "
            f"{options.true_label}: Kırmızı robot. {options.false_label}: Mavi robot. "
            "Yalnızca A veya B ile yanıtlayın."
        )
    else:
        raise KeyError(language)
    return f'{instruction}\n"{sentence}"'


def make_controlled_joint_prompt(
    language: str, sentence: str, options: OptionMap, instruction_style: str
) -> str:
    if instruction_style == "english":
        instruction = (
            "Does the sentence correctly describe which robot is doing the action to the other "
            "robot in the image? "
            f"{options.true_label}: Yes. {options.false_label}: No. Answer with only A or B."
        )
        return f'{instruction}\nSentence: "{sentence}"'
    if language == "de":
        instruction = (
            "Beschreibt der Satz korrekt, welcher Roboter im Bild die Handlung am anderen "
            "Roboter ausführt? "
            f"{options.true_label}: Ja. {options.false_label}: Nein. Antworte nur mit A oder B."
        )
    elif language == "tr":
        instruction = (
            "Cümle, görselde eylemi hangi robotun diğer robota yaptığını doğru anlatıyor mu? "
            f"{options.true_label}: Evet. {options.false_label}: Hayır. "
            "Yalnızca A veya B ile yanıtlayın."
        )
    else:
        raise KeyError(language)
    return f'{instruction}\n"{sentence}"'

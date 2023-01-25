from dataclasses import dataclass

from patterns.behavioral_patterns import TemplateView
from view import View
# для тайпхинтинга для того чтобы pycharm нормально дополнял, а что я не понимаю
from typing import Type


@dataclass
class Url:
    url: str
    view: Type[View] | Type[TemplateView]

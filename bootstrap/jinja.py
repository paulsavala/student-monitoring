from jinja2 import Environment, FileSystemLoader, select_autoescape


def prep_jinja():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html'])
    )
    return env
from tech_news.assets.utilities import labels, options

# Requisito 12


def menu(option):
    if option not in options:
        return "Opção inválida!"
    return options[option]


def analyzer_menu():
    option = input(labels)
    print(menu(option))

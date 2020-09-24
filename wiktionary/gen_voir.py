import mwparserfromhell as mwp
import pywikibot as pwb
import unidecode

pwb.config.put_throttle = 0


def create_or_update_subtemplate(name, words):
    def create_subtemplate():
        template_page.text = "{{voir|" + "|".join(
            words) + "}}" + f"<noinclude>\n[[Catégorie:Modèles de désambiguïsation|{name}]]\n</noinclude>"
        template_page.save("Création du sous-modèle.")

    def update_subtemplate():
        parsed = mwp.parse(template_page.text)
        template = parsed.filter_templates()[0]
        if name not in list(map(str, template.params)):
            template.params.append(name)
            template.params.sort()
            if str(parsed) != template_page.text:
                template_page.text = str(parsed)
                template_page.save("Mise à jour du sous-modèle.")

    template_page = pwb.Page(site, f"Modèle:voir/{name}")
    if not template_page.text:
        create_subtemplate()
    else:
        update_subtemplate()


def treat_page(page):
    parsed = mwp.parse(page.text)
    templates = parsed.filter_templates()
    voir_templates = [t for t in templates if t.name == "voir"]
    if len(voir_templates) > 1:
        print("Présence de plusieurs modèles dans ", page.title())
    elif len(voir_templates) == 1:
        template = voir_templates[0]
        template_name = unidecode.unidecode(page.title().lower())

        words = sorted(list(map(str, template.params)) + [page.title()])
        create_or_update_subtemplate(template_name, words)

        template.params.clear()
        template.name = f"voir/{template_name}"

        if page.text != str(parsed):
            page.text = str(parsed)
            page.save("Factorisation du modèle voir.")


site = pwb.Site(code="fr", fam="wiktionary")

with open("dump.txt", "r", encoding="utf8") as file:
    for line in file.readlines():
        treat_page(pwb.Page(site, line))

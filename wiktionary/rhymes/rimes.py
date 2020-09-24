import mwparserfromhell as mwp
import pywikibot as pwb

pwb.config.put_throttle = 0

site = pwb.Site()

try:
    for page in pwb.Category(site, "Formes de verbes en français").articles():
        page_text = page.text
        if "pron-rimes" not in page_text:
            parsed_text = mwp.parse(page_text)
            templates = parsed_text.filter_templates()
            fr_pron_templates = list(filter(lambda t: t.name == "pron" and t.params[1] == "fr", templates))
            if not fr_pron_templates or not fr_pron_templates[0].params:
                continue
            fr_pron = fr_pron_templates[0].params[0]

            lang_sections = parsed_text.get_sections(levels=[2])
            if page_text.count("{{langue|") != len(lang_sections):
                print("Mauvais nombre de sections : " + page.title())
                continue
            fr_section = \
                list(
                    filter(lambda s: s.filter_headings()[0].title.filter_templates()[0] == "{{langue|fr}}",
                           lang_sections))[
                    0]
            if "{{S|prononciation}}" in fr_section:
                level_3_sections = fr_section.get_sections(levels=[3])
                if len(level_3_sections) == 1:
                    print("Erreur de format sur " + page.title())
                    continue
                pron_sections = list(
                    filter(lambda s: s.filter_headings()[0].title.filter_templates() and
                                     s.filter_headings()[0].title.filter_templates()[0] == "{{S|prononciation}}",
                           level_3_sections))
                if len(pron_sections) != 1:
                    print("Mauvais nombre de sections de prononciation : " + page.title())
                    continue
                pron_section = pron_sections[0]
                pron_section.insert(2, f"* {{{{pron-rimes|{fr_pron}|fr}}}}\n")
                page.text = str(parsed_text)
                page.save("Ajout du modèle pron-rimes")
except IndexError as e:
    print(page)
    raise e

import re

import pywikibot as pwb

pwb.config.put_throttle = 0

site = pwb.Site(code="fr", fam="wiktionary", user="LeptiBot")

ending = "ik"
appendix = pwb.Page(site, f"Rime:français/-{ending}")
cat = pwb.Category(site, f"Rimes en français en \\{ending}\\")




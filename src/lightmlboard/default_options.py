# -*- coding: utf-8 -*-
"""
@file
@brief Default options for the application.
"""


class LightMLBoardDefaultOptions:
    """
    Default options for the web application.
    """

    lang = "fr"

    debug = True

    logging = True

    title = "Compétition de Machine Learning"

    subtitle = "ENSAE"

    cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="

    description = """Tableaux de résultats pour la compétition
        de machine learning organisé dans le cadre du cours
        <a href="http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/index.html">Python pour un data scientist économiste</a>.
        """.replace("        ", "")

    description2 = """Détails de la compétition :
        <a href="http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/questions/competition_2A.html#l-competition-2017-2a">
        Compétition 2017 - additifs alimentaires</a>.
        """.replace("        ", "")

    title_main = "Principe"
    description_main = """..."""

    allowed_users = None

    competitions = []

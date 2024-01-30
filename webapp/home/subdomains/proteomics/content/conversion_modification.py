"""Content for data section - tools, workflows and help tabs."""

galaxy_au_support_item = {
    "title_html": 'Galaxy Australia support',
    "description_html": """<p>
            Any user of Galaxy Australia can request support through an
            online form.
        </p>""",
    "button_link": "/request/support",
    "button_html": "Request support",
}

tools = [
    # {   # Accordion item schema:
    #     "title_html": '',
    #     "description_html": """""",
    #     "inputs": [
    #         {
    #             'datatypes': [''],
    #             'label': '',
    #         },
    #     ],
    #     "button_link": "",
    #     "button_html": "",
    #     "button_tip": "",
    #     "view_link": "",
    #     "view_html": "",
    #     "view_tip": "",
    # },
    {
        "title_html": '<code>msconvert</code>',
        "description_html": '<p>Convert and/or filter mass spectrometry files.</p>',
        "inputs": [
            {
                'datatypes': ['thermo.raw', 'mzML', 'mzXML', 'raw', 'wiff', 'wiff.tar', 'agilentbrukeryep.d.tar', 'agilentmasshunter.d.tar', 'brukerbaf.d.tar', 'brukertdf.d.tar', 'watersmasslynx.raw.tar'],
                'label': 'Input unrefined MS data',
            },
        ],
        "button_link": "$GALAXY_URL/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/msconvert/msconvert/",
    },
    {
        "title_html": '<code>Thermo</code>',
        "description_html": '<p>RAW file converter.</p>',
        "inputs": [
            {
                'datatypes': ['thermo.raw'],
                'label': 'Thermo RAW file',
            }
        ],
        "button_link": "$GALAXY_URL/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/thermo_raw_file_converter/thermo_raw_file_converter/",
    }
]

help = []  # Todo

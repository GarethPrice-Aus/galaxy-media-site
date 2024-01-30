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
        "title_html": '<code>LFQ Analyst</code>',
        "description_html": '<p>Analyze and Visualize Label-Free Proteomics output from MaxQuant.</p>',
        "inputs": [
            {
                'datatypes': ['txt'],
                'label': 'Protein groups (MaxQuant output)',
            },
            {
                'datatypes': ['txt'],
                'label': 'Experimental Design Matrix (MaxQuant output)',
            }
        ],
        "button_link": "$GALAXY_URL/root?tool_id=interactive_tool_lfqanalyst",
        "view_link": "Shah AD, Goode RJA, Huang C, Powell DR, Schittenhelm RB. LFQ-Analyst: An easy-to-use interactive web-platform to analyze and visualize proteomics data preprocessed with MaxQuant. https://doi.org/10.1021/acs.jproteome.9b00496",
    },
    {
        "title_html": '<code>MSstats</code>',
        "description_html": '<p>Statistical relative protein significance analysis in DDA, SRM and DIA Mass Spectrometry.</p>',
        "inputs": [
            {
                'datatypes': ['tabular', 'csv'],
                'label': 'Either the 10-column MSstats format or the outputs of spectral processing tools such as MaxQuant, OpenSWATH.',
            }
        ],
        "button_link": "$GALAXY_URL/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/msstats/msstats/",
    }
]


help = [
    {
        "title_html": 'LFQ-Analyst: Manual',
        "description_html": """
            <p>
              A detailed user manual for LFQ-Analyst.
            </p>""",
        "button_link": "https://analyst-suite.monash-proteomics.cloud.edu.au/apps/lfq-analyst/LFQ-Analyst_manual.pdf",
        "button_html": "Manual",
        "view_link": "Shah AD, Goode RJA, Huang C, Powell DR, Schittenhelm RB. LFQ-Analyst: An easy-to-use interactive web-platform to analyze and visualize proteomics data preprocessed with MaxQuant. https://doi.org/10.1021/acs.jproteome.9b00496",
    },
    {
        "title_html": 'MaxQuant and MSstats for the analysis of label-free data',
        "description_html": """
        <p>
          Learn how to use MaxQuant and MSstats for the analysis of label-free shotgun (DDA) data.
        </p>""",
        "button_link": "https://training.galaxyproject.org/training-material/topics/proteomics/tutorials/maxquant-msstats-dda-lfq/tutorial.html",
        "button_html": "Tutorial",
    },
    galaxy_au_support_item,
]

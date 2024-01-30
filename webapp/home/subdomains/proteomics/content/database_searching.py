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
        "title_html": '<code>DecoyDatabase</code>',
        "description_html": '<p>Create decoy sequence database from forward sequence database.</p>',
        "inputs": [
            {
                'datatypes': ['fasta'],
                'label': 'Input FASTA file(s), each containing a database',
            }
        ],
        "button_link": "$GALAXY_URL/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/openms_decoydatabase/DecoyDatabase/",
    },
    {
        "title_html": '<code>MaxQuant</code>',
        "description_html": '<p>MaxQuant is a quantitative proteomics software package designed for analyzing large mass-spectrometric data sets.</p>',
        "inputs": [
            {
                'datatypes': ['thermo.raw', 'mzML', 'mzXML'],
                'label': 'Mass spectrometry data sets'
            },
            {
                'datatypes': ['tabular'],
                'label': 'Experimental design template',
            },
        ],
        "button_link": "$GALAXY_URL/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/maxquant/maxquant/",
    },
    {
        "title_html": '<code>Morpheus</code>',
        "description_html": '<p>Database search algorithm for high-resolution tandem mass spectra.</p>',
        "inputs": [
            {
                'datatypes': ['mzML'],
                'label': 'Indexed mzML',
            },
            {
                'datatypes': ['fasta', 'uniprotxml'],
                'label': 'MS Protein Search Database: UniProt Xml or Fasta',
            },
        ],
        "button_link": "$GALAXY_URL/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/morpheus/morpheus/",
    },
    {
        "title_html": '<code>MSFraggerAdapter</code>',
        "description_html": '<p>Peptide Identification with MSFragger.</p>',
        "inputs": [
            {
                'datatypes': ['mzML', 'mzXML'],
                'label': 'Input File with spectra for MSFragger',
            },
            {
                'datatypes': ['fasta'],
                'label': 'Protein FASTA database file path',
            },
        ],
        "button_link": "$GALAXY_URL/root?tool_id=toolshed.g2.bx.psu.edu/repos/galaxyp/openms_msfraggeradapter/MSFraggerAdapter/",
    }
]

help = []  # Todo

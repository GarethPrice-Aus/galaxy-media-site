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
        "title_html": "Import data to Galaxy",
        "description_html": "<p>Standard upload of data to Galaxy, from your computer or from the web.</p>",
        "button_link": '$GALAXY_URL/tool_runner?tool_id=upload1',
    }
]


help = [
    {
        "title_html": 'Can I upload sensitive data?',
        "description_html": """
            <p>
              No, do not upload personal or sensitive, such as human health or clinical data.
              Please see our
              <a href="/about#data-privacy">Data Privacy</a>
              page for definitions of sensitive and health-related information.
            </p>
            <p>
              Please also make sure you have read our
              <a href="/about#terms-of-service">Terms of Service</a>,
              which covers hosting and analysis of research data.
            </p>""",
    },
    {
        "title_html": 'Is my data private?',
        "description_html": """
            <p>
              Please read our
              <a href="/about#data-privacy">Privacy Policy</a>
              for information on your personal data and any data that you upload.
            </p>""",
    },
    {
        "title_html": 'How can I increase my storage quota?',
        "description_html": """
            <p>
                Please submit a quota request if your Galaxy Australia account reaches its data storage limit. Requests are usually provisioned quickly if you provide a reasonable use case for your request.
            </p>""",
        "button_link": "/request/quota",
        "button_html": "Request",
    },
    {
        "title_html": 'Tutorial: Introduction to proteomics, protein identification, quantification and statistical modelling',
        "description_html": """
            <p>
              This practical aims to familiarize you with Galaxy for Proteomics, including theory, methods and software examples.
            </p>""",
        "button_link": "https://training.galaxyproject.org/training-material/topics/proteomics/tutorials/introduction/slides.html#1",
        "button_html": "Tutorial",
    },
    galaxy_au_support_item,
]

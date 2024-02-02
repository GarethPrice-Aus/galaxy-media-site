"""Exported landing pages to be requested by external Galaxy servers."""

import logging
import requests
import yaml
from django.core.exceptions import SuspiciousOperation
from django.contrib import messages

logger = logging.getLogger('django')


class ExportSubsiteContext(dict):
    """Build and validate render context for exported subsite landing page.

    These page are intended to be displayed externally to the host Galaxy
    (i.e. on a different Galaxy server).

    The context can be built from GET params or from an externally hosted YAML
    context specified by a ``yaml_context_url`` GET param.
    """

    REQUIRED_PARAMS = (
        'site_name',
        'nationality',
        'galaxy_base_url',
    )
    HTML_SNIPPETS = (
        'intro_html',
        'header_image',
        'footer_html',
    )

    def __init__(self, request):
        """Init context from dict."""
        super().__init__(self)
        self['snippets'] = {}
        self.request = request
        self.params = request.GET
        self.update({
            'export': True,
            'extend_template': 'home/header-export.html',
        })
        if self.params.get('yaml_context_url'):
            self._fetch_yaml_context()
        self.update({
            # GET params override the YAML context if they exist
            k: v for k, v in
            {
                'site_name': self.params.get('site_name'),
                'lab_name': self.params.get('lab_name'),
                'nationality': self.params.get('nationality', ''),
                'galaxy_base_url': self.params.get('galaxy_base_url'),
            }.items()
            if v
        })

    def _clean(self):
        """Format params for rendering."""
        self['nationality'].capitalize()
        self['galaxy_base_url'].strip('/')

    def validate(self):
        """Validate against required params."""
        for k in self.REQUIRED_PARAMS:
            if not self.get(k):
                msg = f"GET parameter '{k}' is required for webpage export."
                # ! TODO: messages are not rendering in 400 template
                messages.add_message(self.request, messages.ERROR, msg)
                logger.warning('Error validating exported subsite request:'
                               + msg)
                raise SuspiciousOperation(msg)
        self._clean()

    def _fetch_yaml_context(self):
        """Fetch params from remote YAML file."""
        url = self.params.get('yaml_context_url')
        if url:
            yaml_bytes = requests.get(url).content
            params = yaml.load(yaml_bytes, Loader=yaml.Loader)
            self.update(params)
            self._fetch_snippets()

    def _fetch_snippets(self):
        """Fetch HTML snippets and add to context.snippets."""
        for name in self.HTML_SNIPPETS:
            if relpath := self.get(name):
                self['snippets'][name] = self._fetch_snippet(relpath)

    def _fetch_snippet(self, relpath):
        """Fetch HTML snippet from remote URL."""
        yaml_url = self.params.get('yaml_context_url')
        if yaml_url:
            url = yaml_url.rsplit('/', 1)[0] + '/' + relpath.lstrip('./')
            response = requests.get(url)
            if response.status_code >= 300:
                raise SuspiciousOperation(
                    f'HTTP {response.status_code} fetching file: {url}')
            return response.content.decode('utf-8')

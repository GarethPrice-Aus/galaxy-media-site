"""Views for home app."""

import os
import logging
import pprint
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import TemplateDoesNotExist, loader
from django.template.loader import get_template

from events.models import Event
from news.models import News
from utils import aaf
from utils import unsubscribe
from utils.exceptions import ResourceAccessError
from utils.institution import get_institution_list
from .export import ExportSubsiteContext
from .models import CoverImage, Notice
from .forms import (
    ResourceRequestForm,
    QuotaRequestForm,
    SupportRequestForm,
    ACCESS_FORMS,
)
from . import subdomains

logger = logging.getLogger('django')


def index(request, landing=False):
    """Show homepage/landing page."""
    news_items = News.objects.filter(is_tool_update=False)
    events = Event.objects.all()
    tool_updates = News.objects.filter(is_tool_update=True)

    if not request.user.is_staff:
        news_items = news_items.filter(is_published=True)
        events = events.filter(is_published=True)
        tool_updates = tool_updates.filter(is_published=True)

    return render(request, 'home/index.html', {
        'landing': landing,
        'notices': Notice.get_notices_by_type(request),
        'cover_image': CoverImage.get_random(request),
        'news_items': news_items.order_by('-datetime_created')[:6],
        'events': events.order_by('-datetime_created')[:6],
        'tool_updates': tool_updates.order_by('-datetime_created')[:6],
    })


def landing(request, subdomain):
    """Show landing pages for *.usegalaxy.org.au subsites.

    A support request form is passed to the template which can be submitted
    with AJAX and processed by an API handler.
    """
    template = f'home/subdomains/{subdomain}.html'
    try:
        get_template(template)
    except TemplateDoesNotExist:
        raise Http404

    try:
        sections = getattr(subdomains, subdomain).sections
    except AttributeError as exc:
        raise AttributeError(
            f"{exc}\n\n"
            f"No content files found for subdomain '{subdomain}'"
            " at 'webapp/home/subdomains/{subdomain}/'")

    context = {
        'extend_template': 'home/header.html',
        'export': False,
        'name': subdomain,
        'site_name': settings.GALAXY_SITE_NAME,
        'nationality': 'Australian',
        'galaxy_base_url': settings.GALAXY_URL,
    }
    if request.GET.get('export'):
        context = ExportSubsiteContext(request)
        context.validate()
        context.update({
            'sections': sections,
            'name': subdomain,
            'title': f'Galaxy - {subdomain.title()} Lab',
        })

    else:
        context.update({
            'sections': sections,
            'notices': Notice.get_notices_by_type(request, subsite=subdomain),
            'cover_image': CoverImage.get_random(request, subsite=subdomain),
            'form': SupportRequestForm(),
        })

    response = render(request, template, context)
    response.content = response.content.replace(
        b'$GALAXY_URL',
        context['galaxy_base_url'].encode('utf-8'))
    return response


def notice(request, notice_id):
    """Display notice body page."""
    return render(request, 'home/notice.html', {
        'notice': get_object_or_404(Notice, id=notice_id),
    })


def about(request):
    """Show about page."""
    return render(request, 'home/about.html')


def user_request(request):
    """Show user request menu."""
    return render(request, 'home/requests/menu.html')


def user_request_tool(request):
    """Handle user tool requests."""
    form = ResourceRequestForm()
    if request.POST:
        form = ResourceRequestForm(request.POST)
        if form.is_valid():
            logger.info('Form valid. Dispatch content as email.')
            form.dispatch()
            return render(request, 'home/requests/success.html')
        logger.info("Form was invalid. Returning invalid feedback.")
    return render(request, 'home/requests/tool.html', {'form': form})


def user_request_quota(request):
    """Handle user data quota requests."""
    form = QuotaRequestForm()
    if request.POST:
        form = QuotaRequestForm(request.POST)
        if form.is_valid():
            logger.info('Form valid. Dispatch content as email.')
            form.dispatch()
            return render(request, 'home/requests/success.html')
        logger.info("Form was invalid. Returning invalid feedback.")
    return render(request, 'home/requests/quota.html', {'form': form})


def user_request_support(request):
    """Handle user support requests."""
    form = SupportRequestForm()
    if request.POST:
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            form.dispatch()
            return render(request, 'home/requests/success.html')
        logger.info("Form was invalid. Returning invalid feedback.")
    return render(request, 'home/requests/support.html', {'form': form})


def user_request_resource_access(request, resource):
    """Handle resource (e.g. tool) access requests.

    The galaxy group name must match the <resource> string encoded in the URL.
    """
    if resource not in ACCESS_FORMS:
        raise Http404
    Form = ACCESS_FORMS[resource]
    form = Form()
    if request.POST:
        form = Form(request.POST)
        if form.is_valid():
            try:
                actioned = form.action(request, resource)
            except ResourceAccessError as exc:
                logger.error(
                    f"ResourceAccessError for {resource}:\n{exc}"
                    f"Form data:\n{pprint.pformat(form.cleaned_data)}")
                return report_exception_response(
                    request,
                    exc,
                    title=("Sorry, an error occurred while actioning your"
                           " request"),
                )
            success_template = 'home/requests/access/success.html'
            return render(request, success_template, {
                'form': form.cleaned_data,
                'actioned': actioned,
            })
        logger.info("Form was invalid. Returning invalid feedback.")
    template = f'home/requests/access/{resource}.html'
    return render(request, template, {'form': form})


def report_exception_response(request, exc, title=None):
    """Report an exception to the user."""
    return render(request, 'generic.html', {
        'message': str(exc),
        'title': title or "Sorry, an error has occurred",
    })


def page(request, *args):
    """Serve an arbitrary static page."""
    logger.warning(args)
    template = f'home/pages/{request.path}'
    templates_dir = os.path.join(
        settings.BASE_DIR,
        'home/templates/home/pages')
    if os.path.basename(template) not in os.listdir(templates_dir):
        raise Http404
    if request.path.endswith('.md'):
        return md_page(request, template)
    return render(request, template)


def md_page(request, template):
    """Return a markdown file rendered to HTML."""
    md_path = (
        loader.get_template(template)
        .origin.name
    )
    with open(md_path) as f:
        markdown = f.read()
    return render(request, 'home/markdown-page.html', {
        'md_text': markdown,
    })


def aaf_info(request):
    """Show current list of AAF institutions."""
    return render(request, 'home/aaf-institutions.html', {
        'entities': aaf.get_entities(),
    })


def australian_institutions(request):
    """Show list of recognised AU research institution email domains."""
    return render(request, 'home/au-institutions.html', {
        'institutions': get_institution_list(),
    })


def unsubscribe_user(request):
    """Add user hash to unsubscribe list."""
    email_hash = request.GET.get('id')
    if not (request.method == 'GET' and email_hash):
        raise Http404
    unsubscribe.add(email_hash)
    return render(request, 'generic.html', {
        'title': "Unsubscribe successful",
        'message': ("You will no longer receive marketing emails from Galaxy"
                    " Australia."),
    })

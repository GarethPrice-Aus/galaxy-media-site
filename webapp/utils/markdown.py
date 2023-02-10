"""Generic filters and parsers."""

import re

# Help text for markdown editors
MARKDOWN_HELP_TEXT = (
    """Enter valid GitHub markdown -
    <a href="https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax" target="_blank">see markdown guide</a>.
    We're using <b>"code-friendly" mode</b>, so __ and _ will be rendered
    literally! Use * and ** for italics/bold instead.
    """
)

MARKDOWN_IMAGE_HELP_TEXT = (
    """
    <br>
    Upload event images at the bottom of the page, and tag them
    in markdown like so:
    <pre>
     <span style="color: #79AEC8"># the URI will replace img&lt;N&gt; after save </span>
     ![alt text](img1)

     <span style="color: #79AEC8"># Use an image tag to define size. Defaults to 100% max-width.</span>
     &lt;img src="img2" width=200&gt; </pre>
     """
)

# To render/replace image URIs
IMAGE_URI_EXPRESSIONS = (
    {   # markdown image tags
        're': r'\(img\d\)',  # regex to match
        'tag': '(img{0})',   # format string to replace
    },
    {   # html image tags
        're': r'src="img\d"',
        'tag': 'src="img{0}"',
    },
)


def get_blurb_from_markdown(text, style=True):
    """Extract a blurb from the first lines of some markdown text."""
    if not text:
        return None

    text = text.replace('\r\n', '\n')

    lines = text.split('\n\n')
    blurb = lines[0]

    if style:
        return blurb

    # Strip style tags
    p = re.compile(r'<style>[\w\W]+</style>', re.MULTILINE)
    matches = p.findall(blurb)
    for m in matches:
        blurb = blurb.replace(m, '')
    return blurb


def render_image_uri(markdown, images):
    """Render image URIs over markdown placeholders.

    Images must be ordered by pk - it appears that pk order will always reflect
    the ordering of images as they are uploaded on the admin UI, and therefore
    the ordering of URI tags entered by the user
    (e.g. img1, img2, img3 should respectively match images ordered by pk).
    """
    if not (markdown and images):
        return markdown
    new = markdown
    for i, image in enumerate(images):
        for e in IMAGE_URI_EXPRESSIONS:
            p = re.compile(e['re'], re.MULTILINE)
            m = p.search(new)
            if not m:
                # No tags to replace
                continue
            # Replace placeholder with real URI
            tag = e['tag'].format(i + 1)
            new = new.replace(
                tag,
                tag.replace(f'img{i + 1}', image.img_uri))
    return new

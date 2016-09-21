import re
from lxml import etree

def parse_length(value, def_units='px'):
	"""Parses value as SVG length and returns it in pixels, or a negative scale (-1 = 100%)."""
	if not value:
		return 0.0
	parts = re.match(r'^\s*(-?\d+(?:\.\d+)?)\s*(px|in|cm|mm|pt|pc|%)?', value)
	if not parts:
		raise Exception('Unknown length format: "{}"'.format(value))
	num = float(parts.group(1))
	units = parts.group(2) or def_units
	if units == 'px':
		return num
	elif units == 'pt':
		return num * 1.25
	elif units == 'pc':
		return num * 15.0
	elif units == 'in':
		return num * 90.0
	elif units == 'mm':
		return num * 3.543307
	elif units == 'cm':
		return num * 35.43307
	elif units == '%':
		return -num / 100.0
	else:
		raise Exception('Unknown length units: {}'.format(units))

def get_svg_dimensions(root):
    if 'width' not in root.keys() or 'height' not in root.keys():
        raise Exception('SVG header must contain width and height attributes')
    width = parse_length(root.get('width'))
    height = parse_length(root.get('height'))
    return height,width

def set_svg_dimensions(root, width, height):
    root.set('width', '{}px'.format(width))
    root.set('height', '{}px'.format(height))

def get_svg_viewbox(root,width,height):
    """parses svg for viewbox or if there is none,, returns viewbox with given width,height at 0,0"""
    viewbox = re.split('[ ,\t]+', root.get('viewBox', '').strip())
    if len(viewbox) == 4:
        for i in [0, 1, 2, 3]:
            viewbox[i] = parse_length(viewbox[i])
        if viewbox[2] * viewbox[3] <= 0.0:
            viewbox = None
    else:
        viewbox = None
    if width <= 0 or height <= 0:
        if viewbox:
            width = viewbox[2]
            height = viewbox[3]
        else:
            raise Exception('SVG width and height should be in absolute units and non-zero')
    if not viewbox:
        viewbox = [0, 0, width, height]
    return viewbox

def resize_svg(tree, longest):
    svg = tree.getroot()
    height,width = get_svg_dimensions(svg)
    viewbox = get_svg_viewbox(svg,width,height)

	# read and convert size and margin values
    twidth = None
    theight = None
    if width > height:
        twidth = longest
        theight = twidth / width * height
    else:
        theight = longest
        twidth = theight / height * width

	# set svg width and height, update viewport for margin
    set_svg_dimensions(svg,twidth,theight)
    offsetx = 0
    offsety = 0
    if twidth / theight > viewbox[2] / viewbox[3]:
		# target page is wider than source image
        page_width = viewbox[3] / theight * twidth
        offsetx = (page_width - viewbox[2]) / 2
        page_height = viewbox[3]
    else:
        page_width = viewbox[2]
        page_height = viewbox[2] / twidth * theight
        offsety = (page_height - viewbox[3]) / 2
    svg.set('viewBox', '{} {} {} {}'.format(viewbox[0] - offsetx, viewbox[1] - offsety, page_width * 2, page_height * 2))

def resize(file_as_string,longest):
    tree = etree.parse(file_as_string)
    resize_svg(tree, longest)
    return etree.tostring(tree.getroot())
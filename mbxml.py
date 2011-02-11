import xml.etree.ElementTree
import string
import StringIO
try:
	from xml.etree.ElementTree import fixtag
except:
	# Python < 2.7
	def fixtag(tag, namespaces):
		# given a decorated tag (of the form {uri}tag), return prefixed
		# tag and namespace declaration, if any
		if isinstance(tag, QName):
			tag = tag.text
		namespace_uri, tag = string.split(tag[1:], "}", 1)
		prefix = namespaces.get(namespace_uri)
		if prefix is None:
			prefix = _namespace_map.get(namespace_uri)
			if prefix is None:
				prefix = "ns%d" % len(namespaces)
			namespaces[namespace_uri] = prefix
			if prefix == "xml":
				xmlns = None
			else:
				xmlns = ("xmlns:%s" % prefix, namespace_uri)
		else:
			xmlns = None
		return "%s:%s" % (prefix, tag), xmlns

NS_MAP = {"http://musicbrainz.org/ns/mmd-2.0#": "ws2"}

def parse_elements(valid_els, element):
	""" Extract single level subelements from an element.
	    For example, given the element:
	    <element>
	        <subelement>Text</subelement>
	    </element>
	    and a list valid_els that contains "subelement",
	    return a dict {'subelement': 'Text'}
	"""
	result = {}
	for sub in element:
		t = fixtag(sub.tag, NS_MAP)[0]
		if ":" in t:
			t = t.split(":")[1]
		if t in valid_els:
			result[t] = sub.text
	return result

def parse_attributes(attributes, element):
	""" Extract attributes from an element.
	    For example, given the element:
	    <element type="Group" />
	    and a list attributes that contains "type",
	    return a dict {'type': 'Group'}
	"""
	result = {}
	for attr in attributes:
		if attr in element.attrib:
			result[attr] = element.attrib[attr]
	return result

def parse_inner(inner_els, element):
	""" Delegate the parsing of a subelement to another function.
	    For example, given the element:
	    <element>
	        <subelement>
	            <a>Foo</a><b>Bar</b>
		</subelement>
	    </element>
	    and a dictionary {'subelement': parse_subelement},
	    call parse_subelement(<subelement>) and
	    return a dict {'subelement': <result>}
	"""
	result = {}
	for sub in element:
		t = fixtag(sub.tag, NS_MAP)[0]
		if ":" in t:
			t = t.split(":")[1]
		if t in inner_els.keys():
			result[t] = inner_els[t](sub)
	return result

def parse_message(message):
	s = message.read()
	print s
	f = StringIO.StringIO(s)
	tree = xml.etree.ElementTree.ElementTree(file=f)
	root = tree.getroot()
	result = {}
	for element in root:
		t = fixtag(element.tag, NS_MAP)[0]
		if t == "ws2:artist":
			result["artist"] = parse_artist(element)
			
	return result

def parse_artist_lifespan(lifespan):
	parts = parse_elements(["begin", "end"], lifespan)
	beginval = parts.get("begin", "")
	endval = parts.get("end", "")
		
	return (beginval, endval)

def parse_artist(artist):
	result = {}
	attribs = ["id", "type"]
	elements = ["name", "sort-name"]
	inner_els = {"life-span": parse_artist_lifespan}

	result.update(parse_attributes(attribs, artist))
	result.update(parse_elements(elements, artist))
	result.update(parse_inner(inner_els, artist))

	return result

import xml.etree.ElementTree as ET
import string
try:
    import cStringIO as StringIO
except:
    import StringIO
import logging
import inspect

try:
    from ET import fixtag
except:
    # Python < 2.7
    def fixtag(tag, namespaces):
        # given a decorated tag (of the form {uri}tag), return prefixed
        # tag and namespace declaration, if any
        if isinstance(tag, ET.QName):
            tag = tag.text
        namespace_uri, tag = string.split(tag[1:], "}", 1)
        prefix = namespaces.get(namespace_uri)
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

def make_artist_credit(artists):
    names = []
    for artist in artists:
        if isinstance(artist, dict):
            names.append(artist.get("artist", {}).get("name", ""))
        else:
            names.append(artist)
    return "".join(names)

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
        else:
            logging.debug("in <%s>, uncaught <%s>", fixtag(element.tag, NS_MAP)[0], t)
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
        else:
            logging.debug("in <%s>, uncaught attribute %s", fixtag(element.tag, NS_MAP)[0], attr)
    return result

# Not all parse_* functions are defined when the _Parser classes
# are instanciated. Thus they are looked-up (and cached) when used.
__FUNC_CACHE = {}

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
        if parse_subelement returns a tuple of the form
        ('subelement-key', <result>) then return a dict
        {'subelement-key': <result>} instead
    """
    result = {}
    for sub in element:
        t = fixtag(sub.tag, NS_MAP)[0]
        if ":" in t:
            t = t.split(":")[1]
        # find parse_* function for this tag
        func = __FUNC_CACHE.get(t, None)
        if not func:
            # the parse_* function for this tag is not yet in cache
            # find it in the module
            _module = inspect.getmodule(parse_inner)
            func = getattr(_module, 'parse_' + t.replace('-', '_'), None)
            # anf put it into the cache
            __FUNC_CACHE[t] = func
        print t, func
        if func:
            inner_result = func(sub)
            if isinstance(inner_result, tuple):
                result[inner_result[0]] = inner_result[1]
            else:
                result[t] = inner_result
        else:
            # the parse_* function for this tag is not defined
            logging.debug("in <%s>, not delegating <%s>", fixtag(element.tag, NS_MAP)[0], t)
    return result


class _Parser(object):
    def __init__(self, attribs, elements, inner_els):
        self.attribs = attribs
        self.elements = elements
        self.inner_els = inner_els

    def __call__(self, element):
        result = {}
        result.update(parse_attributes(self.attribs, element))
        result.update(parse_elements(self.elements, element))
        print '---------__'
        result.update(parse_inner(self.inner_els, element))
        if "artist-credit" in result:
            result["artist-credit-phrase"] = make_artist_credit(result["artist-credit"])
        return result


def parse_message(message):
    s = message.read()
    f = StringIO.StringIO(s)
    tree = ET.ElementTree(file=f)
    root = tree.getroot()
    valid_elements = [
        "artist", "label", "release", "release-group", "recording",
        "work",
        "disc", "puid", "echoprint",
        "artist-list", "label-list", "release-list",
        "release-group-list", "recording-list", "work-list",
        "collection-list", "collection",
        "message"]
    return parse_inner(valid_elements, root)

def parse_response_message(message):
    return parse_elements(["text"], message)

def parse_collection_list(cl):
    return [parse_collection(c) for c in cl]

parse_collection = _Parser(
    attribs = ["id"],
    elements = ["name", "editor"],
    inner_els = ["release-list"])

def parse_collection_release_list(rl):
    attribs = ["count"]
    return parse_attributes(attribs, rl)

def parse_life_span(lifespan):
    parts = parse_elements(["begin", "end"], lifespan)
    beginval = parts.get("begin", "")
    endval = parts.get("end", "")
    return (beginval, endval)

# backward compatible
parse_artist_lifespan = parse_life_span


def parse_artist_list(al):
    return [parse_artist(a) for a in al]

parse_artist = _Parser(
    attribs = ["id", "type"],
    elements = ["name", "sort-name", "country", "user-rating"],
    inner_els = ["life-span", "recording-list", "release-list",
                 "release-group-list", "work-list", "tag-list",
                 "user-tag-list", "rating", "alias-list"])

def parse_label_list(ll):
    return [parse_label(l) for l in ll]

parse_label = _Parser(
    attribs = ["id", "type"],
    elements = ["name", "sort-name", "country", "label-code", "user-rating"],
    inner_els = ["life-span", "release-list", "tag-list",
                 "user-tag-list", "rating", "alias-list"])

def parse_attribute_list(al):
    return [parse_attribute_tag(a) for a in al]

def parse_attribute_tag(attribute):
    return attribute.text

def parse_relation_list(rl):
    attribs = ["target-type"]
    ttype = parse_attributes(attribs, rl)
    key = "%s-relation-list" % ttype["target-type"]
    return (key, [parse_relation(r) for r in rl])

parse_relation = _Parser(
    attribs = ["type"],
    elements = ["target", "direction"],
    inner_els = ["artist", "label", "recording", "release",
                 "release-group", "attribute-list", "work"])

parse_release = _Parser(
    attribs = ["id"],
    elements = ["title", "status", "disambiguation", "quality", "country",
                "barcode", "date", "packaging", "asin"],
    inner_els = ["text-representation", "artist-credit",
                 "label-info-list", "medium-list", "release-group",
                "relation-list"])

def parse_medium_list(ml):
    return [parse_medium(m) for m in ml]

parse_medium = _Parser(
    attribs = [],
    elements = ["position", "format", "title"],
    inner_els = ["disc-list", "track-list"])

def parse_disc_list(dl):
    return [parse_disc(d) for d in dl]

def parse_text_representation(textr):
    return parse_elements(["language", "script"], textr)

parse_release_group = _Parser(
    attribs = ["id", "type"],
    elements = ["title", "user-rating", "first-release-date"],
    inner_els = ["artist-credit", "release-list", "tag-list",
                 "user-tag-list", "rating"])

parse_recording = _Parser(
    attribs = ["id"],
    elements = ["title", "length", "user-rating"],
    inner_els = ["artist-credit", "release-list", "tag-list",
                 "user-tag-list", "rating", "puid-list", "isrc-list",
                 "echoprint-list"])

def parse_external_id_list(pl):
    return [parse_attributes(["id"], p)["id"] for p in pl]

# these are all external id lists:
echoprint_list = parse_external_id_list
isrc_list = parse_external_id_list
puid_list = parse_external_id_list



def parse_work_list(wl):
    return [parse_work(w) for w in wl]

parse_work = _Parser(
    attribs = ["id"],
    elements = ["title", "user-rating"],
    inner_els = ["tag-list", "user-tag-list", "rating", "alias-list"])

parse_disc = _Parser(
    attribs = ["id"],
    elements = ["sectors"],
    inner_els = ["release-list"])
    
def parse_release_list(rl):
    return [parse_release(r) for r in rl]

def parse_release_group_list(rgl):
    return [parse_release_group(rg) for rg in rl]

parse_puid = _Parser(
    attribs = ["id"],
    elements = [],
    inner_els = ["recording-list"])

def parse_recording_list(rl):
    return [parse_recording(r) for r in rl]

def parse_artist_credit(ac):
    result = []
    for namecredit in ac:
        result.append(parse_name_credit(namecredit))
        join = parse_attributes(["joinphrase"], namecredit)
        if "joinphrase" in join:
            result.append(join["joinphrase"])
    return result

parse_name_credit = _Parser(
    attribs = [],
    elements = ["name"],
    inner_els = ["artist"])

    
def parse_label_info_list(lil):
    return [parse_label_info(li) for li in lil]

parse_label_info = _Parser(
    attribs = [],
    elements = ["catalog-number"],
    inner_els = ["label"])

def parse_track_list(tl):
    return [parse_track(t) for t in tl]

parse_track = _Parser(
    attribs = [],
    elements = ["position"],
    inner_els = ["recording"])

def parse_tag_list(tl):
    return [parse_tag(t) for t in tl]

parse_tag = _Parser(
    attribs = ["count"],
    elements = ["name"],
    inner_els = [])

user_tag_list = parse_tag_list


def parse_rating(rating):
    attribs = ["votes-count"]

    result.update(parse_attributes(attribs, rating))
    result["rating"] = rating.text

    return result

def parse_alias_list(al):
    return [parse_alias(a) for a in al]

###
def make_barcode_request(barcodes):
    NS = "http://musicbrainz.org/ns/mmd-2.0#"
    root = ET.Element("{%s}metadata" % NS)
    rel_list = ET.SubElement(root, "{%s}release-list" % NS)
    for release, barcode in barcodes.items():
        rel_xml = ET.SubElement(rel_list, "{%s}release" % NS)
        bar_xml = ET.SubElement(rel_xml, "{%s}barcode" % NS)
        rel_xml.set("{%s}id" % NS, release)
        bar_xml.text = barcode

    return ET.tostring(root, "utf-8")

def make_puid_request(puids):
    NS = "http://musicbrainz.org/ns/mmd-2.0#"
    root = ET.Element("{%s}metadata" % NS)
    rec_list = ET.SubElement(root, "{%s}recording-list" % NS)
    for recording, puid_list in puids.items():
        rec_xml = ET.SubElement(rec_list, "{%s}recording" % NS)
        rec_xml.set("id", recording)
        p_list_xml = ET.SubElement(rec_xml, "{%s}puid-list" % NS)
        l = puid_list if isinstance(puid_list, list) else [puid_list]
        for p in l:
            p_xml = ET.SubElement(p_list_xml, "{%s}puid" % NS)
            p_xml.set("id", p)

    return ET.tostring(root, "utf-8")

def make_echoprint_request(echoprints):
    NS = "http://musicbrainz.org/ns/mmd-2.0#"
    root = ET.Element("{%s}metadata" % NS)
    rec_list = ET.SubElement(root, "{%s}recording-list" % NS)
    for recording, echoprint_list in echoprints.items():
        rec_xml = ET.SubElement(rec_list, "{%s}recording" % NS)
        rec_xml.set("id", recording)
        e_list_xml = ET.SubElement(rec_xml, "{%s}echoprint-list" % NS)
        l = echoprint_list if isinstance(echoprint_list, list) else [echoprint_list]
        for e in l:
            e_xml = ET.SubElement(e_list_xml, "{%s}echoprint" % NS)
            e_xml.set("id", e)

    return ET.tostring(root, "utf-8")

def make_tag_request(artist_tags, recording_tags):
    NS = "http://musicbrainz.org/ns/mmd-2.0#"
    root = ET.Element("{%s}metadata" % NS)
    rec_list = ET.SubElement(root, "{%s}recording-list" % NS)
    for rec, tags in recording_tags.items():
        rec_xml = ET.SubElement(rec_list, "{%s}recording" % NS)
        rec_xml.set("{%s}id" % NS, rec)
        taglist = ET.SubElement(rec_xml, "{%s}user-tag-list" % NS)
        for t in tags:
            usertag_xml = ET.SubElement(taglist, "{%s}user-tag" % NS)
            name_xml = ET.SubElement(usertag_xml, "{%s}name" % NS)
            name_xml.text = t
    art_list = ET.SubElement(root, "{%s}artist-list" % NS)
    for art, tags in artist_tags.items():
        art_xml = ET.SubElement(art_list, "{%s}artist" % NS)
        art_xml.set("{%s}id" % NS, art)
        taglist = ET.SubElement(art_xml, "{%s}user-tag-list" % NS)
        for t in tags:
            usertag_xml = ET.SubElement(taglist, "{%s}user-tag" % NS)
            name_xml = ET.SubElement(usertag_xml, "{%s}name" % NS)
            name_xml.text = t

    return ET.tostring(root, "utf-8")

def make_rating_request(artist_ratings, recording_ratings):
    NS = "http://musicbrainz.org/ns/mmd-2.0#"
    root = ET.Element("{%s}metadata" % NS)
    rec_list = ET.SubElement(root, "{%s}recording-list" % NS)
    for rec, rating in recording_ratings.items():
        rec_xml = ET.SubElement(rec_list, "{%s}recording" % NS)
        rec_xml.set("{%s}id" % NS, rec)
        rating_xml = ET.SubElement(rec_xml, "{%s}user-rating" % NS)
        if isinstance(rating, int):
            rating = "%d" % rating
        rating_xml.text = rating
    art_list = ET.SubElement(root, "{%s}artist-list" % NS)
    for art, rating in artist_ratings.items():
        art_xml = ET.SubElement(art_list, "{%s}artist" % NS)
        art_xml.set("{%s}id" % NS, art)
        rating_xml = ET.SubElement(rec_xml, "{%s}user-rating" % NS)
        if isinstance(rating, int):
            rating = "%d" % rating
        rating_xml.text = rating

    return ET.tostring(root, "utf-8")

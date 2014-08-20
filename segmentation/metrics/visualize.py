def find_root(segment):
    for parent in segment.parents:
        if parent.name == "html":
            return parent


def visualize(segments, name):
    if len(segments) == 0:
        return
    root = find_root(segments[0].tags[0])
    soup = root.parent
    for i in segments:
        par = i.tags[0].parent
        chs = [c for c in par.children]

        new_tag = soup.new_tag("div", style="border:4px solid #FF00FF !important;")

        par.insert(chs.index(i.tags[0]), new_tag)

        for j in i.tags:
            new_tag.insert(0,j.extract())

    output_file = open(name, "w")
    output_file.write(root.prettify().encode("utf8"))

    import webbrowser

    url = name
    webbrowser.open(url, new=2)

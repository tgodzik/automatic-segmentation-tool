def find_root(segment):
    for parent in segment.parents:
        if parent.name == "html":
            return parent


def visualize(segments):
    root = find_root(segments[0].tags[0])
    soup = root.parent
    for i in segments:
        par = i.tags[0].parent

        new_tag = soup.new_tag("div", style="border:1px solid #000000;")
        par.append(new_tag)

        for j in i.tags:
            new_tag.append(j.extract())

    output_file = open("result.html", "w")
    output_file.write(root.prettify().encode("utf8"))

    import webbrowser

    url = "result.html"
    webbrowser.open(url, new=2)
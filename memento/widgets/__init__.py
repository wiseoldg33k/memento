def use_font(text, font="SpaceMono"):
    before = "[font={}]".format(font)
    after = "[/font]"
    return "".join((before, text, after))

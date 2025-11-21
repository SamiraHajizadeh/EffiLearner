
def text_match_three(txt):
 if not txt.startswith("ac"):
 return False
 a = txt.count("a")
 count_b = len(txt) - len(txt.replace("a", "b", 2))
 if count_b < a and count_b > 3:
 return False
 return True
assert not text_match_three("ac")
assert not text_match_three("dc")
assert text_match_three("abbbba")
assert text_match_three("caacabbbba")
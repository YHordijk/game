import re


def find_flags(string):
	pattern = r'\\[^. {}]+(?:\{[^}]*\})*'
	#find raw flags
	flags = re.findall(pattern, string)
	print(flags)
	#decompose flags
	decomposed = []
	for flag in flags:
		d = re.split(r'{', flag)
		d = [x.strip('}').strip('\\') for x in d]
		decomposed.append(d)

	return decomposed



text = r'\newtext{Demo}\test{hello there} general kenobi \color{red}{this text is red}. This text is \bold{bold}. We are now clearing the background \clearbackground. Done'


print(find_flags(text))


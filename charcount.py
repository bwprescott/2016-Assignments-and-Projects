while True:
	word = input("type a word, followed by Enter (to quit, type 'quit'): ")
	if word == 'quit':
		break
	print(word, "has", len(word), "characters.")

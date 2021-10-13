read = open('dictionary.text', 'r').read().split('\n')
read = {w for w in read}
open('dictionary.text', 'w').write('\n'.join(read))


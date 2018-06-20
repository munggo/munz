import asyncio, random
from .base import MzBase


class AgreeHandler(MzBase):
    @asyncio.coroutine
    def proc_msg(self, msg):
        text = msg.get('text', '').lower()
        user = msg.get('user', '')
        ch = msg['channel']

        if text.endswith('알아?') or text.endswith('알아요?'):
            result = random.choice(['몰라요~!', '글쎄요...', '당연하죠!', '그것도 몰라요?'])
            yield from self.go_msg(ch, result)
        elif text.endswith('인정?'):
            yield from self.go_msg(ch, '인정 ㅇㅇ')
        elif text.endswith('ㅇㅈ?'):
            yield from self.go_msg(ch, 'ㅇㅈ ㅇㅇ')
            yield from self.go_msg(ch, result)
            if user == 'U03BW8HU1':
                result = random.choice(['네?', ':gozo:', '졸려요', '일 안하고 뭐해요?'])
            yield from self.go_msg(ch, result)
        elif text.endswith('예쁘지?') or '예뻐?' in text:
            result = random.choice(['그건 아니라고 생각합니다.', '잘못슴다.', '네.:facepalm:', ':gozo:'])
            yield from self.go_msg(ch, result)

        zz_count = text.count('ㅋ')
        if zz_count > 1 and random.randrange(0, 6) == 5:
            result = random.choice(['ㅋ', ':smile:', ':smile_cat:', ':smiley:', ':smiley_cat:', ':smiling_imp:', ':smirk:', ':smirk_cat:', ':sweat_smile:' ])
            if zz_count < 3: zz_count = 3
            yield from self.go_msg(ch, result * (random.randint(1, zz_count)))
        elif text.count('울어') > 0:
            result = random.choice([':crying_cat_face:', ':cry:', ':happy_cry:', 'ㅜㅜ'])
            yield from self.go_msg(ch, result)
        elif text.count('웃어') > 0:
            result = random.choice([':smile:', ':smile_cat:', ':smiley:', ':smiley_cat:', ':smiling_imp:', ':smirk:', ':smirk_cat:', ':sweat_smile:' ])
            yield from self.go_msg(ch, result)

        nn_count = text.count('ㅜ')
        if nn_count > 1 and random.randrange(0, 10) == 5:
            if nn_count > 2: nn_count = 2
            yield from self.go_msg(ch, 'ㅜ' * (random.randint(1, nn_count)))

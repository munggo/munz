## To add a plugin
Create a file in the **munz/plugins/** directory.

```
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
```

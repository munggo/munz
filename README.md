## To add a plugin
Create a file in the **munz/plugins/** directory.

```
import asyncio
from .base import MzBase


class AgreeHandler(MzBase):
    @asyncio.coroutine                                                                                                                                          
    def proc_msg(self, msg):
        ch = msg['channel']
        result = "Send Channel Message"

            yield from self.go_msg(ch, result)
```

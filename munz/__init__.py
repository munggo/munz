import json, requests, asyncio
import websockets, websockets.client
from munz import plugins

class MunZ(object):
    def __init__(self, token):
        self.mz_token, self.mz_sock = token, None
        self.mz_handlers = [cls(self) for cls in plugins.mz_all()]

    @asyncio.coroutine
    def go_msg(self, ch, data):
        send_data = json.dumps({
            'type': 'message',
            'channel': ch,
            'text': data,
        })
        yield from self.mz_sock.send(send_data)

    @asyncio.coroutine
    def _main_loop(self, url):
        self.mz_sock = yield from websockets.connect(url)
        while True:
            raw_msg = yield from self.mz_sock.recv()
            if not raw_msg: continue

            for handler in self.mz_handlers:
                msg = json.loads(raw_msg)
                if 'type' in msg and msg['type'] == 'message':
                    yield from handler.proc_msg(msg)

    def start(self):
        slack_url = 'https://slack.com/api/rtm.start'
        response = requests.get(slack_url, {'token': self.mz_token})
        info = response.json()
        url = info['url']

        start = asyncio.get_event_loop()
        start.run_until_complete(self._main_loop(url))

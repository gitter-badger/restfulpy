import ujson

from sqlalchemy import Unicode, TypeDecorator

from restfulpy.messaging import Messenger


class MockupMessenger(Messenger):
    _last_message = None

    @property
    def last_message(self):
        return self.__class__._last_message

    @last_message.setter
    def last_message(self, value):
        self.__class__._last_message = value

    def send(
            self,
            to, subject, body,
            cc=None,
            bcc=None,
            template_string=None,
            template_filename=None,
            from_=None,
            attachments=None
    ):
        self.last_message = {
            'to': to,
            'body': body,
            'subject': subject
        }


# noinspection PyAbstractClass
class FakeJson(TypeDecorator):  # pragma: no cover
    impl = Unicode

    def process_bind_param(self, value, engine):
        return ujson.dumps(value)

    def process_result_value(self, value, engine):
        if value is None:
            return None

        return ujson.loads(value)

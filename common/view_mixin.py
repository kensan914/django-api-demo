from common.exceptions import demo_exception_handler


class BaseViewMixin:
    def get_exception_handler(self):
        return demo_exception_handler

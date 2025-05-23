from rest_framework.authentication import SessionAuthentication


class DemoSessionAuthentication(SessionAuthentication):
    def authenticate_header(self, _):
        # NOTE: 認証エラー時に 401 ステータスコードでレスポンスさせるため、WWW-Authenticate ヘッダの値を指定する
        return "Session"

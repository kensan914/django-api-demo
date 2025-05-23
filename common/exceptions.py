from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def demo_exception_handler(exc, context):
    if (response := exception_handler(exc, context)) is None:
        response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        error_message = "予期せぬエラーが発生しました。"
        validation_errors = {}

        # print(f"{error_message}: {exc!r}")
    else:
        if "detail" not in response.data:
            # NOTE: DRF のバリデーションエラー
            #       list か dict の場合バリデーションエラー扱いとなる（rest_framework.views.exception_handler 内のロジック参考）
            assert (
                is_validation_error := isinstance(response.data, list | dict)
            ), "detail がない場合は必ずバリデーションエラー扱いのため、response.data が list か dict であるか確認"
            error_content = response.data
        elif is_validation_error := isinstance(response.data["detail"], list | dict):
            # NOTE: "detail" フィールドの DRF バリデーションエラー
            #       list か dict の場合バリデーションエラー扱いとなる（rest_framework.views.exception_handler 内のロジック参考）
            error_content = response.data
        else:
            # NOTE: 非バリデーションエラー
            error_content = response.data["detail"]

        if is_validation_error:
            error_message = "バリデーションエラーが発生しました。"
            validation_errors = error_content
        else:
            error_message = error_content
            validation_errors = {}

    response.data = {
        "error": {
            "message": error_message,
        },
        "validation_errors": validation_errors,
    }
    return response

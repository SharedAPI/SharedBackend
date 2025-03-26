from rest_framework import status
from rest_framework.response import Response


class CustomResponseHandler:
    def success_response(
        self, message: str, object, status_code=status.HTTP_201_CREATED
    ):
        """Generates a standardized success response."""
        return Response(
            {"message": message, "object_id": object.id},
            status=status_code,
        )

    def error_response(self, message: str, details=None):
        """Generates a standardized error response."""
        response_data = {"error": message}
        if details:
            response_data["details"] = details
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

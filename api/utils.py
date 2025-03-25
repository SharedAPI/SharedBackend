from django.http import JsonResponse
from rest_framework import status


class CustomResponseHandler:
    def success_response(self, message: str, object):
        """Generates a standardized success response."""
        return JsonResponse(
            {"message": message, "object_id": object.id},
            status=status.HTTP_201_CREATED,
        )

    def error_response(self, message: str, details=None):
        """Generates a standardized error response."""
        response_data = {"error": message}
        if details:
            response_data["details"] = details
        return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

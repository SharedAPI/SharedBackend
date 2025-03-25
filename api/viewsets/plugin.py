from http import HTTPMethod
from typing import Any, Dict, List

from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.models.column import DynamicColumn
from api.models.plugin import Plugin
from api.serializers.plugin import PluginSerializer
from api.serializers.table import DynamicTableSerializer


class PluginViewSet(viewsets.ModelViewSet):
    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer
    # All the classic method are provide such as list,create,retrieve,update,partial_update, destroy

    # Override create method because DynamicTable and DynamicColumn have to be created
    def create(self, request: Request) -> Response:
        try:
            serialized_data: PluginSerializer = self.get_serializer(data=request.data)
            if not serialized_data.is_valid():
                raise Exception("Error during serialization of plugin")

            plugin = serialized_data.save()
            print(f"Plugin Created with ID: {plugin.id}")
            print(f"{plugin.__dict__}")

            data = serialized_data.data
            # Keep tracking the composition of plugin in our databse
            schema: Dict[str, Any] = data.get("schema", {})
            if not schema:
                return JsonResponse(
                    {
                        "message": "Plugin registered but no schema provided",
                        "plugin": data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            tables: List[Dict[str, Any]] = schema.get("tables", [])
            if not tables:
                return JsonResponse(
                    {
                        "message": "Plugin registered but schema is empty",
                        "plugin": data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            for table in tables:
                name = table.get("name", None)
                if not name:
                    raise Exception("All table should have a name")

                serialized_dynamic_table = DynamicTableSerializer(
                    data={
                        "plugin": plugin.id,
                        "name": name,
                    }
                )

                if not serialized_dynamic_table.is_valid():
                    raise Exception("Error during serialization of dynamic table")
                dynamic_table = serialized_dynamic_table.save()
                print(f"Table Created with ID: {dynamic_table.id}")
                print(f"{dynamic_table.__dict__}")

                columns = table.get("columns", [])
                if not columns:
                    raise Exception("Columns should be provide to create a schema")

                for column in columns:
                    print("TABLE CREATEDDZZQDZ")
                    DynamicColumn.objects.create(
                        table=dynamic_table,
                        name=column["name"],
                        type=column["type"],
                        is_primary=column.get("primary", False),
                    )
                    print("TABLE CREATEDdZQUHDIZUh")
            # TODO Faire fichier de migration automatique est l'appliquer

            return JsonResponse(
                {
                    "message": "Plugin registered and models created",
                    "plugin_id": plugin.id,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=[HTTPMethod.POST])
    def create_schema(self, request, pk=None):
        # Provide a new route that have the following endpoint:
        # /api/plugins/<id>/create_schema
        pass

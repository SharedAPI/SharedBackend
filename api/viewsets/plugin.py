from http import HTTPMethod
from typing import Any, Dict, List

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from api.models.column import DynamicColumn
from api.models.plugin import Plugin
from api.serializers.plugin import PluginSerializer
from api.serializers.table import DynamicTableSerializer
from api.utils import CustomResponseHandler


class PluginViewSet(viewsets.ModelViewSet, CustomResponseHandler):
    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer
    # All the classic method are provide such as list,create,retrieve,update,partial_update, destroy

    # Override create method because DynamicTable and DynamicColumn have to be created
    def create(self: viewsets.ModelViewSet, request: Request) -> Response:
        serialized_data: PluginSerializer = self.get_serializer(data=request.data)
        if not serialized_data.is_valid():
            return self.error_response(
                "Error during plugin serialization", serialized_data.errors
            )

        plugin = serialized_data.save()
        schema: Dict[str, Any] = serialized_data.validated_data.get("schema", {})

        # Keep tracking the composition of plugin in our databse
        if not schema:
            return self.success_response(
                "Plugin registered but no schema provided", plugin
            )

        tables: List[Dict[str, Any]] = schema.get("tables", [])
        if not tables:
            return self.success_response(
                "Plugin registered but schema is empty", plugin
            )

        try:
            self._process_schema(plugin, tables)
        except ValidationError as e:
            return self.error_response(
                "Validation error during schema processing", e.detail
            )
        except Exception as e:
            return self.error_response(
                "Unexpected error during schema processing", str(e)
            )

        return self.success_response("Plugin registered and models created", plugin)

    @action(detail=True, methods=[HTTPMethod.POST])
    def create_schema(self, request, pk=None):
        # Provide a new route that have the following endpoint:
        # /api/plugins/<id>/create_schema
        pass

    def _process_schema(self, plugin, tables: List[Dict[str, Any]]) -> None:
        """Processes the schema, creating tables and columns dynamically."""
        for table in tables:
            name = table.get("name")
            if not name:
                raise ValidationError("All tables must have a name")

            dynamic_table = self._create_dynamic_table(plugin, name)

            columns = table.get("columns", [])
            if not columns:
                raise ValidationError(f"Table '{name}' must have at least one column")

            self._create_dynamic_columns(dynamic_table, columns)

    def _create_dynamic_table(self, plugin, name: str):
        """Creates a dynamic table associated with the plugin."""
        serialized_table = DynamicTableSerializer(
            data={"plugin": plugin.id, "name": name}
        )
        if not serialized_table.is_valid():
            raise ValidationError(serialized_table.errors)

        return serialized_table.save()

    def _create_dynamic_columns(
        self, dynamic_table, columns: List[Dict[str, Any]]
    ) -> None:
        """Creates dynamic columns for a given table."""
        for column in columns:
            DynamicColumn.objects.create(
                table=dynamic_table,
                name=column["name"],
                type=column["type"],
                is_primary=column.get("primary", False),
            )

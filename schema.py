"""
Manager for schema loading from JSON input data model
"""

import json
import logging

from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, create_model
from typing import Dict, Any, Type, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchemaManager():

    def __init__(self, schema_dir: str):
        self.schema_dir = Path(schema_dir)
        self.schema_dir.mkdir(exist_ok=True)
        self.loaded_models = {}

    def load_schema(self, schema_file: str) -> Dict[str, Any]:
        """ Load JSON schema from schema_file"""
        schema_path = self.schema_dir / schema_file

        if not schema_path.exists():
            logger.error("Schema is missing")
            raise FileNotFoundError(f"Schema file not found: {schema_file}")

        with open(schema_path, 'r') as f:
            schema = json.load(f)

        logger.info(f"Schema {schema_file} is loaded!")

        return schema

    def create_model_from_schema(self, schema: Dict[str, Any]) -> Type[BaseModel]:
        """Create Pydantic model from schema"""
        type_mapping = {
            'int': int,
            'str': str,
            'float': float,
            'bool': bool
        }

        field_definitions = {}

        for field_name, field_config in schema.items():
            f_type = field_config.get('type', 'string')
            f_required = field_config.get('required', False)
            f_min = field_config.get('min', None)
            f_max = field_config.get('max', None)
            f_default = field_config.get('default', None)

            python_type = type_mapping.get(f_type, str)

            # Handle optional fields
            if not f_required:
                python_type = Optional[python_type]
                default_value = ... if f_default is None else f_default
            else:
                default_value = ... if f_default is None else f_default

            field_kwargs = {}

            # Add validation constraints
            if f_min is not None:
                if f_type in ['int', 'float']:
                    field_kwargs['ge'] = f_min
                elif f_type == 'str':
                    field_kwargs['min_length'] = f_min

            if f_max is not None:
                if f_type in ['int', 'float']:
                    field_kwargs['le'] = f_max
                elif f_type == 'str':
                    field_kwargs['max_length'] = f_max

            # Handle default values
            if f_default is not None:
                field_kwargs['default'] = f_default
            elif not f_required:
                field_kwargs['default'] = None

            field_definitions[field_name] = (python_type, Field(**field_kwargs))

        # Create model configuration
        model_config = ConfigDict(
            extra='forbid',  # 'allow' to 'forbid'
            str_to_lower=True,
            str_strip_whitespace=True
        )

        # Create the dynamic model
        dynamic_model = create_model(
            "DataModel",
            __config__=model_config,
            **field_definitions
        )

        logger.info(f"Created Data Model with {len(field_definitions)} fields: {list(field_definitions.keys())}")

        return dynamic_model

    def get_model(self, schema_file: str) -> Type[BaseModel]:
        """Get or create a model for the given schema file"""
        if schema_file not in self.loaded_models:
            schema = self.load_schema(schema_file=schema_file)
            self.loaded_models[schema_file] = self.create_model_from_schema(schema=schema)

        return self.loaded_models[schema_file]


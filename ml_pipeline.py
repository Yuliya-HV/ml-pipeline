
import json
import logging

from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, create_model
from typing import Dict, Any, Type, Optional

from schema import SchemaManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class MLPipeline:

    def __init__(self, schema_dir: str):
        self.schema_manager = SchemaManager(schema_dir=schema_dir)
        self.input_model = None
        self.output_model = None
        self._load_models()

    def _load_models(self):

        try:
            self.input_model = self.schema_manager.get_model("input.json")
            self.output_model = self.schema_manager.get_model("output.json")
            logger.info("Models are loaded")

        except:
            raise

    def validate_input(self, input_data: Dict[str, Any]) -> BaseModel:
        """Validate input data against schema."""
        try:
            validated_input = self.input_model(**input_data)
            logger.info("Input validation successful")
            return validated_input
        except Exception as e:
            logger.error(f"Input validation failed: {e}")
            raise

    def process_data(self, validated_input: BaseModel) -> BaseModel:
        """Mock ML processing."""
        try:
            # Simple mock processing based on input
            age = validated_input.age
            income = getattr(validated_input, 'income', 50000)

            # Mock prediction logic
            if age < 25:
                risk = "high"
                prediction = 0.8
            elif age > 60:
                risk = "medium"
                prediction = 0.6
            else:
                risk = "low"
                prediction = 0.3

            # Adjust based on income
            if income > 100000:
                prediction *= 0.8  # Lower risk for high income
                risk = "low" if prediction < 0.5 else risk

            confidence = max(0.7, 1.0 - (prediction * 0.2))

            prediction_result = {
                "prediction": round(prediction, 2),
                "confidence": round(confidence, 2),
                "risk_level": risk,
                "processed_at": "2024-01-01"
            }

            validated_output = self.output_model(**prediction_result)
            logger.info("Processing completed successfully")
            return validated_output

        except Exception as e:
            logger.error(f"Processing failed: {e}")
            raise

    def run_pipeline(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """Run complete ML pipeline."""
        logger.info("Starting ML pipeline...")

        # Step 1: Validate input
        validated_input = self.validate_input(raw_input)
        logger.info(f"Validated input: {validated_input.model_dump()}")

        # Step 2: Process data
        validated_output = self.process_data(validated_input)
        logger.info(f"Generated output: {validated_output.model_dump()}")

        return {
            "input": validated_input.model_dump(),
            "output": validated_output.model_dump(),
            "success": True
        }

def create_test_schemas():
        """Create simple test schema files."""
        test_data_dir = Path("data")
        test_data_dir.mkdir(exist_ok=True)

        # Simple input schema - just field definitions
        input_schema = {
            "age": {
                "type": "int",
                "required": True,
                "min": 0,
                "max": 120
            },
            "name": {
                "type": "str",
                "required": True,
                "min": 1,
                "max": 100
            },
            "income": {
                "type": "float",
                "required": False,
                "min": 0,
                "default": 0
            },
            "country": {
                "type": "str",
                "required": False,
                "default": "unknown"
            }
        }

        # Simple output schema
        output_schema = {
            "prediction": {
                "type": "float",
                "required": True,
                "min": 0,
                "max": 1
            },
            "confidence": {
                "type": "float",
                "required": True,
                "min": 0,
                "max": 1
            },
            "risk_level": {
                "type": "str",
                "required": True
            },
            "processed_at": {
                "type": "str",
                "required": True
            }
        }

        # Write schema files
        with open(test_data_dir / "input.json", "w") as f:
            json.dump(input_schema, f, indent=2)

        with open(test_data_dir / "output.json", "w") as f:
            json.dump(output_schema, f, indent=2)

        print("Created simple schema files in data/ directory")


def main():
        """Test the simplified ML pipeline."""

        # Create test schema files
        create_test_schemas()

        # Initialize pipeline
        pipeline = MLPipeline(schema_dir="data")

        # Test cases
        test_cases = [
            {
                "age": 35,
                "name": "Jane Smith",
                "income": 75000.0,
                "country": "USA"
            },
            {
                "age": 22,
                "name": "John Doe"
                # income and country will use defaults
            },
            {
                "age": 67,
                "name": "  ALICE WONDER  ",  # Will be stripped and lowercased
                "income": 120000.0
            },
            {
                "age": 45,
                "name": "Bob Builder",
                "income": 50000.0,
                "country": "UK",
                "extra_field": "this is allowed"  # Extra fields allowed
            }
        ]

        for i, test_input in enumerate(test_cases, 1):
            print(f"\n{'=' * 50}")
            print(f"TEST CASE {i}")
            print(f"{'=' * 50}")

            try:
                result = pipeline.run_pipeline(test_input)
                print("SUCCESS")
                print(f"Input: {result['input']}")
                print(f"Output: {result['output']}")

            except Exception as e:
                print(f"FAILED: {e}")


if __name__ == "__main__":
        main()


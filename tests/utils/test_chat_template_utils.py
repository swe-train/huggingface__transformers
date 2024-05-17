import unittest
from typing import List, Optional, Union

from transformers.utils import get_json_schema


class JsonSchemaGeneratorTest(unittest.TestCase):
    def test_simple_function(self):
        def fn(x: int):
            """
            Test function

            Args:
                 x: The input
            """
            return x

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": "integer", "description": "The input"}},
                "required": ["x"],
            },
        }
        self.assertEqual(schema, expected_schema)

    def test_no_arguments(self):
        def fn():
            """
            Test function
            """
            return True

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {"type": "object", "properties": {}},
        }
        self.assertEqual(schema, expected_schema)

    def test_union(self):
        def fn(x: Union[int, float]):
            """
            Test function

            Args:
                x: The input
            """
            return x

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": ["integer", "number"], "description": "The input"}},
                "required": ["x"],
            },
        }
        self.assertEqual(schema, expected_schema)

    def test_optional(self):
        def fn(x: Optional[int]):
            """
            Test function

            Args:
                x: The input
            """
            return x

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": "integer", "description": "The input", "nullable": True}},
                "required": ["x"],
            },
        }
        self.assertEqual(schema, expected_schema)

    def test_default_arg(self):
        def fn(x: int = 42):
            """
            Test function

            Args:
                 x: The input
            """
            return x

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {"type": "object", "properties": {"x": {"type": "integer", "description": "The input"}}},
        }
        self.assertEqual(schema, expected_schema)

    def test_nested_list(self):
        def fn(x: List[List[Union[str, int]]]):
            """
            Test function

            Args:
                x: The input
            """
            return x

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": ["string", "integer"]}},
                        "description": "The input",
                    }
                },
                "required": ["x"],
            },
        }
        self.assertEqual(schema, expected_schema)

    def test_multiple_arguments(self):
        def fn(x: int, y: str):
            """
            Test function

            Args:
                x: The input
                y: Also the input
            """
            return x

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer", "description": "The input"},
                    "y": {"type": "string", "description": "Also the input"},
                },
                "required": ["x", "y"],
            },
        }
        self.assertEqual(schema, expected_schema)

    def test_multiple_complex_arguments(self):
        def fn(x: List[Union[int, float]], y: Optional[Union[int, str]] = None):
            """
            Test function

            Args:
                x: The input
                y: Also the input
            """
            return x

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "array", "items": {"type": ["integer", "number"]}, "description": "The input"},
                    "y": {
                        "type": ["integer", "string"],
                        "nullable": True,
                        "description": "Also the input",
                    },
                },
                "required": ["x"],
            },
        }
        self.assertEqual(schema, expected_schema)

    def test_missing_docstring(self):
        def fn(x: int):
            return x

        with self.assertRaises(ValueError):
            get_json_schema(fn)

    def test_missing_param_docstring(self):
        def fn(x: int):
            """
            Test function
            """
            return x

        with self.assertRaises(ValueError):
            get_json_schema(fn)

    def test_missing_type_hint(self):
        def fn(x):
            """
            Test function

            Args:
                 x: The input
            """
            return x

        with self.assertRaises(ValueError):
            get_json_schema(fn)

    def test_return_value(self):
        def fn(x: int) -> int:
            """
            Test function

            Args:
                x: The input
            """
            return x

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": "integer", "description": "The input"}, "return": {"type": "integer"}},
                "required": ["x"],
            },
        }
        self.assertEqual(schema, expected_schema)

    def test_return_value_docstring(self):
        def fn(x: int) -> int:
            """
            Test function

            Args:
                x: The input


            Returns:
                The output
            """
            return x

        schema = get_json_schema(fn)
        expected_schema = {
            "name": "fn",
            "description": "Test function",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer", "description": "The input"},
                    "return": {"type": "integer", "description": "The output"},
                },
                "required": ["x"],
            },
        }
        self.assertEqual(schema, expected_schema)

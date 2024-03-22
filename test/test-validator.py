from guardrails import Guard
from pydantic import BaseModel, Field
from validator import SqlColumnPresence


class ValidatorTestObject(BaseModel):
    test_val: str = Field(
        validators=[
            SqlColumnPresence(cols=["name", "breed", "weight"], on_fail="exception")
        ]
    )


TEST_OUTPUT = """{
  "test_val": "SELECT name, AVG(weight) FROM animals GROUP BY name"
}
"""

guard = Guard.from_pydantic(output_class=ValidatorTestObject)
raw_output, guarded_output, *rest = guard.parse(TEST_OUTPUT)

print("validated output: ", guarded_output)


TEST_FAIL_OUTPUT = """{
  "test_val": "SELECT name, color, AVG(weight) FROM animals GROUP BY name, color"
}
"""

try:
    raw_output, guarded_output, *rest = guard.parse(TEST_FAIL_OUTPUT)
    print("Failed to fail validation when it was supposed to")
except Exception:
    print("Successfully failed validation when it was supposed to")

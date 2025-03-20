import json
import sys
import os
import pytest
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

try:
    from population_visualisation import visualisation
except ImportError:
    # Skip tests if population_visualisation.py or visualisation() don't exist
    pytest.skip(reason="could not import visualisation", allow_module_level=True)

class TestVisualisation():
    def test_sample(self):
        # result = visualisation(...)
        # assert ...
       assert True

    # def test_always_fails(self):
    #    assert False

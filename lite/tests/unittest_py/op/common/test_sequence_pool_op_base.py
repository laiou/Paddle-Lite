# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
sys.path.append('..')

from program_config import TensorConfig, ProgramConfig, OpConfig, CxxConfig, TargetType, PrecisionType, DataLayoutType, Place
import numpy as np
from functools import partial
from typing import Optional, List, Callable, Dict, Any, Set
import unittest
import hypothesis
from hypothesis import given, settings, seed, example, assume
import hypothesis.strategies as st

def sample_program_configs(draw):
    in_shape = draw(st.lists(
        st.integers(
            min_value=13, max_value=64), min_size=0, max_size=3))
    in_shape.insert(0, 7)        
    pad_value = draw(st.sampled_from([0.0, 0.2, 0.5]))
    pooltype = draw(st.sampled_from(["AVERAGE", "SUM", "SQRT", "MAX", "LAST", "FIRST"]))
    lod_tensor = [[0, 2, 5, 7]]

    def generate_input(*args, **kwargs):
        return np.random.uniform(0.1, 1, in_shape).astype('float32')
    
    ops_config = OpConfig(
        type = "sequence_pool",
        inputs = {
            "X": ["input_data"],
        },
        outputs = {
            "Out": ["output_data"],
            "MaxIndex": ["maxindex"]
        },
        attrs = {
            "pad_value": pad_value,
            "pooltype": pooltype
        }
        )

    program_config = ProgramConfig(
        ops=[ops_config],
        weights={},
        inputs={
            "input_data": 
            TensorConfig(data_gen=partial(generate_input), lod=lod_tensor),
        },
        outputs=["output_data", "maxindex"])

    return program_config

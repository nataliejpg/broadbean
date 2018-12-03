from copy import copy

from typing import Tuple, List
from .types import Number, Symbol

def get_transformed_context(input_context,
                            transformation: callable):
    new_context = copy(input_context)
    if transformation:
        transformation(new_context)
    return new_context


def make_linear_transformation(data: List[
        Tuple[Symbol, List[Tuple[Number,Symbol]]]]):
    def transformation(context):
        for item in data:
            assigned = item[0]
            value = sum([multiplier*context[symbol]
                         for multiplier, symbol in item[1]])
            context[assigned] = value
    return transformation


def make_bilinear_transformation(items):
    def transformation(context):
        for item in items:
            assigned = item[0]
            value = sum([get_value(multiplier)*get_value(symbol)
                         for multiplier, symbol in item[1]])
            context[assigned] = value
    return transformation

def get_value(context, val):
    if isinstance(val, Symbol):
        return context[val]
    else:
        return val



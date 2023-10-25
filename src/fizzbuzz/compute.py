from typing import List

from .models import FizzBuzzParams


def compute_fizzbuzz(params: FizzBuzzParams) -> List[str]:
    result = list()
    for i in range(1, params.limit + 1):
        if i % params.factor1 == 0 and i % params.factor2 == 0:
            result.append(params.replacement1 + params.replacement2)
        elif i % params.factor1 == 0:
            result.append(params.replacement1)
        elif i % params.factor2 == 0:
            result.append(params.replacement2)
        else:
            result.append(str(i))
    return result

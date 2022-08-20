async def coroutine_add_one(number: int) -> int:
    return number + 1


def add_one(number: int) -> int:
    return number + 1


function_result = add_one(1)
coroutine_result = coroutine_add_one(1)

print("Function result is {0} and the type is {1}".format(function_result, type(function_result)))
print("Function result is {0} and the type is {1}".format(coroutine_result, type(coroutine_result)))

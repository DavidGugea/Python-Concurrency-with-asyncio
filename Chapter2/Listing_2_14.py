from asyncio import Future

my_future = Future()

print('Is my_future done? {0}'.format(my_future.done()))

my_future.set_result(42)

print('Is my_future done? {0}'.format(my_future.done()))
print('What is the result of my_future? {0}'.format(my_future.result()))

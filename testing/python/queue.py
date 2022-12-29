q = []
q.append({'key1','value1'})
q.append(({'key2','value2'}))
print(q)
while len(q) != 0:
    print(q.pop())
print("finished popping")
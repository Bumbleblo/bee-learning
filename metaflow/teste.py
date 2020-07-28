import base64
import numpy as np

arr = np.array([1.1, 2.2, 3.3], dtype=np.float32)

data = bytes(arr.__str__(), 'utf-8')
enc = base64.b64encode(data)


print(enc)
print(base64.b64decode(enc))



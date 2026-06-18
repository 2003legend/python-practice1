# ========== 1. 列表 list ==========

# 创建
a = [1, 2, 3]
b = list(range(5))          # [0,1,2,3,4]
c = [0] * 5                 # 长度 5，全 0

# 增删改
a.append(4)                 # 尾部加，O(1)
a.insert(0, -1)             # 指定位置插，O(n)
last = a.pop()                # 弹末尾
first = a.pop(0)              # 弹开头，O(n)

# 切片 [start:end) 左闭右开
nums = [0, 1, 2, 3, 4, 5]
print(nums[1:4])            # [1, 2, 3]
print(nums[:3])             # [0, 1, 2]
print(nums[2:])             # [2, 3, 4, 5]
print(nums[::-1])           # 反转

# 排序
arr = [3, 1, 4, 1, 5]
arr.sort()                  # 原地升序
arr.sort(reverse=True)      # 原地降序
sorted_arr = sorted(arr)      # 返回新列表，不改原数组

# 逆序：arr.reverse() 或 arr[::-1]

# 遍历
for i, val in enumerate(arr):
    print(i, val)

for x, y in zip([1, 2, 3], ['a', 'b', 'c']):
    print(x, y)

# 列表推导（很常用）
squares = [x * x for x in range(5)]
evens = [x for x in range(10) if x % 2 == 0]

# ========== 2. 字典 dict ==========

# 创建
mp = {}
mp = dict()
mp = {"a": 1, "b": 2}

# 读写
mp["a"] = 10
mp["c"] = 3                # 没有就新建
val = mp.get("d", 0)         # 没有 key 返回 0，不报错

# 判断
if "a" in mp:
    pass

# 遍历
for k in mp:
    print(k, mp[k])

for k, v in mp.items():
    print(k, v)

# 删
del mp["b"]
mp.pop("a", None)

# 竞赛常用：统计频次
from collections import Counter
cnt = Counter([1, 2, 2, 3, 3, 3])
print(cnt[3])                # 3
print(cnt.most_common(2))    # [(3,3), (2,2)]

# 竞赛常用：自动补默认值
from collections import defaultdict
g = defaultdict(list)
g[1].append(2)               # 不用先判断 key 是否存在

# ========== 3. 函数 ==========

def add(x, y):
    return x + y

def greet(name, prefix="Hello"):
    return f"{prefix}, {name}"

print(add(1, 2))
print(greet("李剑东"))
print(greet("李剑东", "Hi"))

# 多返回值 → 其实是返回一个元组
def min_max(arr):
    return min(arr), max(arr)

lo, hi = min_max([3, 1, 4])

# 可变参数（了解即可）
def total(*nums):
    s = 0
    for x in nums:
        s += x
    return s

print(total(1, 2, 3, 4))

# ========== 4. 和 C++ 对照记这几个 ==========
# len(a)        ↔ a.size()
# a.append(x)   ↔ a.push_back(x)
# a.pop()       ↔ a.pop_back()
# a.sort()      ↔ sort(a.begin(), a.end())
# x in mp       ↔ mp.count(x)
# mp.get(k, 0)  ↔ mp.count(k) ? mp[k] : 0

# 1. Реалізувати LFU алгоритм для кешування. За базу берем існуючий декоратор.Написати для фетчування юерелів. Додати можливість указати максимум елементів в кеші.

# 2. Створити декоратор для заміру пам'яті.

# 3. Створити окремий гіт репозиторій для домашніх завдань (github).
# Окрема гілка, окрема папка. Пул ріквест на main.

import functools
import requests
from collections import OrderedDict
import tracemalloc


def cache(max_limit=64):
    def internal(f):
        
        @functools.wraps(f)
        def deco(*args, **kwargs):
            res = "result"
            cnt = "count_of_usage"
            cache_key = (args, tuple(kwargs.items()))
            
            if cache_key not in deco._cache:
                if len(deco._cache) >= max_limit:
                    deco._cache.popitem(last=False)
                    
                result = f(*args, **kwargs)
                deco._cache[cache_key] = {res: result, cnt: 1}
                
            elif cache_key in deco._cache:
                deco._cache[cache_key][cnt] += 1

            #сортировка элементов словаря по "count_of_usage"(наибольший в конце)
            #таким образом при заполнении кеша будет удаляться первый элемент - наименее использованный
            deco._cache = OrderedDict(sorted(deco._cache.items(), key=lambda item: item[1][cnt]))
            

            return deco._cache[cache_key][res]
        
        deco._cache = OrderedDict()
        return deco
    
    return internal



def measure_memory(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        snapshot_before = tracemalloc.take_snapshot()
        
        result = f(*args, **kwargs)
        
        snapshot_after = tracemalloc.take_snapshot()
        stats = snapshot_after.compare_to(snapshot_before, 'lineno')
        memory_used = sum(stat.size_diff for stat in stats if stat.size_diff > 0)
        tracemalloc.stop()
        
        print(f"Функция {f.__name__} использовала ~{memory_used / 1024:.2f} КБ памяти")
        return result
    return wrapper


def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

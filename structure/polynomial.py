#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

class Polynomial:
    """多项式数据类型"""
    _poly = ()
    def __init__(self, t_list=0):
        """构造函数
        
        传入的参数t_list的每一项是一个二元组(a,e)，代表了ax^e，e是整数。
        """
        if type(t_list) is tuple:
            self._poly = self._tidy(t_list)
        elif type(t_list) is list:
            self._poly = self._tidy(t_list)
        elif type(t_list) is int:
            self._poly = ((t_list, 0), )
        elif type(t_list) is float:
            self._poly = ((t_list, 0), )
        else:
            self._poly = ((0, 0), )
        
    def coef(self, e):
        """返回e的系数"""
        target = list(filter(lambda x: x[1] == e, self._poly))
        if target:
            return target[0][0]
        else:
            return 0
    
    def lead_exp(self):
        """返回最大的指数"""
        return self._poly[0][1]
    
    def eval(self, x):
        """计算多项式的值"""
        return sum([i[0] * (x ** i[1]) for i in self._poly])
    
    def __add__(self, other):
        """计算与other的和"""
        result = []
        i, j = 0, 0
        while True:
            if i >= len(self._poly):
                result.extend(other._poly[j:])
                break
            if j >= len(other._poly):
                result.extend(self._poly[i:])
                break
            if self._poly[i][1] > other._poly[j][1]:
                result.append(self._poly[i])
                i += 1
            elif self._poly[i][1] < other._poly[j][1]:
                result.append(other._poly[j])
                j += 1
            else:
                result.append((self._poly[i][0]+other._poly[j][0], self._poly[i][1]))
                i += 1
                j += 1
        return Polynomial(result)
    
    def __mul__(self, other):
        """计算与other的乘积"""
        result = []
        for i in self._poly:
            for j in other._poly:
                result.append((i[0]*j[0], i[1]+j[1]))
        return Polynomial(result)
    
    def __repr__(self):
        """打印"""
        expression = []
        for i in self._poly:
            if i[0] < 0:
                sign = "-"
                value = -i[0]
            else:
                sign = "+"
                value = i[0]
            if i[1] == 0:
                expression.append(" {0} {1}".format(sign, value))
            elif i[0] == 1 and i[1] == 1:
                expression.append(" {0} x".format(sign))
            elif i[0] == 1:
                expression.append(" {0} x^{1}".format(sign, i[1]))
            elif i[1] == 1:
                expression.append(" {0} {1}x".format(sign, value))
            else:
                expression.append(" {0} {1}x^{2}".format(sign, value, i[1]))
        expression[0] = expression[0].lstrip(" +")
        return "".join(expression)
    
    @classmethod
    def _tidy(cls, tuple_data):
        """合并同类项并从高阶到低阶排序"""
        data_map = {}
        for i in tuple_data:
            if i[1] in data_map:
                data_map[i[1]] += i[0]
            else:
                data_map[i[1]] = i[0]
        list_data = [(v, k) for k,v in data_map.items()]
        list_data.sort(key=lambda x:x[1], reverse=True)
        return tuple(list_data)

if __name__ == "__main__":
    a = Polynomial()
    print(a)
    b = Polynomial(((1, 2), (-3, 2), (1, 3), (1, 0)))
    print(b)
    print(b.eval(1))
    print(b.lead_exp())
    print(b.coef(3))
    c = Polynomial(((3, 1), (1, 0)))
    print(c)
    d = b + c
    print(d)
    e = b * c
    print(e)
    print(e.eval(1))
    print(e.lead_exp())
    print(e.coef(3))

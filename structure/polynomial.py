#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import decimal

class Polynomial:
    """多项式数据类型"""
    _poly = ()
    def __init__(self, t_list=0):
        """构造函数
        
        传入的参数t_list的每一项是一个二元组(a,e)，代表了ax^e，e是整数。
        """
        try:
            if type(t_list) is tuple or type(t_list) is list:
                self._poly = self._tidy(t_list)
            elif type(t_list) is int or type(t_list) is float:
                self._poly = ((decimal.Decimal(str(t_list)), 0), )
            elif type(t_list) is decimal.Decimal:
                self._poly = ((t_list, 0), )
            elif type(t_list) is str:
                self._poly = self._parse(t_list)
            else:
                self._poly = ((0, 0), )
        except:
            raise ValueError("invalid parameter for Polynomial(): '{0}'".format(t_list)) from None
        
    def coef(self, e):
        """返回e的系数"""
        if type(e) is not int:
            raise TypeError("invalid parameter for coef(): '{0}'".format(e))
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
        if type(x) is not int and type(x) is not float and type(x) is not decimal.Decimal:
            raise TypeError("invalid parameter for eval(): '{0}'".format(x))
        return sum([i[0] * (x ** i[1]) for i in self._poly])
    
    def __neg__(self):
        """计算负数"""
        result = []
        for i in self._poly:
            result.append((-i[0], i[1]))
        return Polynomial(result)
    
    def __add__(self, other):
        """计算与other的和"""
        if type(other) is not Polynomial:
            raise TypeError("unsupported operand type(s) for +: 'Polynomial' and '{0}'".format(type(other)))
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
    
    def __sub__(self, other):
        """计算与other的差"""
        if type(other) is not Polynomial:
            raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '{0}'".format(type(other)))
        return self + (-other)
    
    def __mul__(self, other):
        """计算与other的乘积"""
        if type(other) is not Polynomial:
            raise TypeError("unsupported operand type(s) for *: 'Polynomial' and '{0}'".format(type(other)))
        result = []
        for i in self._poly:
            for j in other._poly:
                result.append((i[0]*j[0], i[1]+j[1]))
        return Polynomial(result)
    
    def __floordiv__(self, other):
        """计算与other的商"""
        if type(other) is not Polynomial:
            raise TypeError("unsupported operand type(s) for //: 'Polynomial' and '{0}'".format(type(other)))
        result = []
        poly = []
        for i in range(self.lead_exp()+1):
            poly.append(self.coef(i))
        i, j = len(poly) - 1, 0
        while True:
            if i < other._poly[j][1]:
                break
            c = (poly[i] / other._poly[j][0], i - other._poly[j][1])
            result.append(c)
            for x in other._poly:
                poly[x[1] + c[1]] -= x[0] * c[0]
            i -= 1
        return Polynomial(result)
    
    def __mod__(self, other):
        """计算与other的余数"""
        if type(other) is not Polynomial:
            raise TypeError("unsupported operand type(s) for %: 'Polynomial' and '{0}'".format(type(other)))
        p = self // other
        return self - p * other
    
    def __eq__(self, other):
        """判断与other相等"""
        if type(other) is not Polynomial:
            raise TypeError("unsupported operand type(s) for ==: 'Polynomial' and '{0}'".format(type(other)))
        return self._poly == other._poly
    
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
            value = "{0:g}".format(value).rstrip(".0")
            if value == '':
                value = '0'
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
        return "".join(expression).lstrip(" +")
    
    @classmethod
    def _tidy(cls, tuple_data):
        """合并同类项并从高阶到低阶排序"""
        data_map = {}
        for i in tuple_data:
            if i[1] in data_map:
                data_map[i[1]] += decimal.Decimal(str(i[0]))
            else:
                data_map[i[1]] = decimal.Decimal(str(i[0]))
        list_data = [(v, k) for k,v in data_map.items()]
        list_data = list(filter(lambda x:x[0], list_data))
        if not list_data:
            list_data = [(0, 0)]
        list_data.sort(key=lambda x:x[1], reverse=True)
        return tuple(list_data)
    
    @classmethod
    def _parse(cls, str_data):
        """从字符串parse多项式，以a1x^e1+a2x^e2+...+anx^en的形式"""
        result = []
        sign = 1
        value, exp = '', ''
        status = 0  # 0,outside; 1,sign; 2,value; 3,x; 4,exp;
        for x in str_data:
            if x in '+-':
                if status == 3 or status == 4:
                    if value == '':
                        value = 1
                    else:
                        value = sign * decimal.Decimal(value)
                    if exp == '':
                        exp = 1
                    else:
                        exp = int(exp)
                    result.append((value, exp))
                    value, exp = '', ''
                if x == '+':
                    sign = 1
                else:
                    sign = -1
                status = 1
            elif x in '0123456789.':
                if status == 0 or status == 1 or status == 2:
                    value += x
                    status = 2
                else: # status == 3 or status == 4
                    exp += x
                    status = 4
            elif x in 'x^':
                status = 3
            elif x in ' ':
                pass
            else:
                raise TypeError("invalid character '{0}'".format(x))
        if status == 2:
            result.append((sign * decimal.Decimal(value), 0))
        else:
            if value == '':
                value = 1
            else:
                value = sign * decimal.Decimal(value)
            if exp == '':
                exp = 1
            else:
                exp = int(exp)
            result.append((value, exp))
        return tuple(result)

if __name__ == "__main__":
    a = Polynomial()
    assert str(a) == '0'
    b = Polynomial(((1, 2), (-3, 2), (1, 3), (1, 0)))
    assert str(b) == 'x^3 - 2x^2 + 1'
    assert b.eval(1) == 0
    assert b.coef(3) == 1
    assert b.lead_exp() == 3
    c = Polynomial(((2, 2), (1.2, 0)))
    d = b + c
    assert str(d) == 'x^3 + 2.2'
    e = b * c
    assert str(e) ==  '2x^5 - 4x^4 + 1.2x^3 - 0.4x^2 + 1.2'
    f = d - c
    assert str(f) == 'x^3 - 2x^2 + 1'
    assert b == f
    g = -c
    assert str(g) == '- 2x^2 - 1.2'
    h = e // c
    assert b == h
    i = e % c
    assert i == a
    j = b - h
    assert j == a
    k = Polynomial(str(e))
    assert k == e
    l = Polynomial('  -3.2 x^7-1.52 x^ 3  + 2  x  ^2 - 5x')
    assert str(l) == '- 3.2x^7 - 1.52x^3 + 2x^2 - 5x'
    m = b // c
    assert str(m) == '0.5x - 1'
    n = b % c
    assert str(n) == '- 0.6x + 2.2'

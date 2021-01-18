# -*- coding: utf-8 -*-

import sys
import pymssql
import os
import random


class SQL:
    def __init__(self, server, user, pwd, db):
        self.server = server
        self.user = user
        self.pwd = pwd
        self.db = db

    def db_connect(self):
        if not self.db:
            raise Exception(NameError, "no db info")
        self.conn = pymssql.connect(self.server, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise Exception(NameError, "failed connection")
        else:
            return cur

    def ExecQuery(self, sql):

        cur = self.db_connect()
        cur.execute(sql)
        resList = cur.fetchall()
        return resList

    def close(self):
        self.conn.close()


def get_db_data(start, end, shift, shift1):
    if shift:
        start = start + ' ' + '08:00:00.000'
    else:
        start += " " + "20:00:00.000"
    if shift1:
        end = end + ' ' + '08:00:00.000'
    else:
        end += " " + "20:00:00.000"

    # modifications needed

    command = "select ORDER_ID,ORDER_NUMBER,SAP_NUMBER,EXECUTION_TIME,PRODUCTION_STATUS from dbo.SECOND_TestData where START_DATE_TIME between '%s' and '%s'" % (start, end)

    print(command)
    # establish the sql, and have the data returned
    db = SQL(server="BSCE-TE-HP", user="sa", pwd="yjx199855", db="GUI_test_db")
    outdata = db.ExecQuery(command)

    ret = generate_data(outdata)
    data = dict()
    product = list()
    fail_num = list()
    pass_num = list()
    total_num = list()
    for x in ret:
        product.append(x)
        fail_num.append(ret[x][0])
        pass_num.append(ret[x][1])
        total_num.append(ret[x][2])
    data['production'] = product
    data['fail'] = fail_num
    data['pass'] = pass_num
    data['total'] = total_num
    data['start_time'] = start
    data['end_time'] = end
    # create a random color generator
    color = random_color(len(product))
    # print(color)
    data['color'] = color
    # get the pass percentage
    percent = get_percentage(pass_num, total_num)
    data['percent'] = percent
    data['total_pass'] = sum(pass_num)
    data['total_fail'] = sum(fail_num)

    return data


def random_color(length):
    color = list()
    head = 'rgba('
    tail = ',0.6)'

    for x in range(0, length):
        rs = random.sample(range(0, 255), 3)
        temp = head + str(rs[0]) + ',' + str(rs[1]) + ',' + str(rs[2]) + tail
        color.append(temp)

    return color


def generate_data(data):
    ret = dict()
    for x in data:
        if x[0] not in ret:
            if x[-1] == "PASS":
                pass_num = 1
                fail_num = 0
            else:
                fail_num = 1
                pass_num = 0
            ret[x[0]] = (fail_num, pass_num, fail_num+pass_num)
        else:
            elements = list(ret[x[0]])
            if x[-1] == "PASS":
                print(elements[1])
                elements[1] = elements[1] + 1
                elements[2] = elements[2] + 1
            else:
                elements[0] = elements[0] + 1
                elements[2] = elements[2] + 1
            ret[x[0]] = elements
    return (ret)


def get_percentage(pass_num, total):
    percent = list()
    for x in range(0, len(pass_num)):
        temp = (int(pass_num[x]) / int(total[x])) * 100
        percent.append(temp)

    return percent


def select_period(start1, end1, shift, shift1):
    print(start1)
    print(end1)
    if shift:
        startshift = "20:00:00.000"
    else:
        startshift = "08:00:00.000"
    if shift1:
        endshift = "20:00:00.000"
    else:
        endshift = "08:00:00.000"

    start = start1 + " " + startshift
    end = end1 + " " + endshift

    command = "select ORDER_ID,ORDER_NUMBER,SAP_NUMBER,EXECUTION_TIME,PRODUCTION_STATUS from dbo.SECOND_TestData where START_DATE_TIME between '%s' and '%s'" % (start, end)
    print(command)
    db = SQL(server="BSCE-TE-HP", user="sa", pwd="yjx199855", db="GUI_test_db")
    outdata = db.ExecQuery(command)

    ret = generate_data(outdata)
    data = dict()
    product = list()
    fail_num = list()
    pass_num = list()
    total_num = list()
    for x in ret:
        product.append(x)
        fail_num.append(ret[x][0])
        pass_num.append(ret[x][1])
        total_num.append(ret[x][2])
    data['production'] = product
    data['fail'] = fail_num
    data['pass'] = pass_num
    data['total'] = total_num

    # create a random color generator
    color = random_color(len(product))
    # print(color)
    data['color'] = color
    # get the pass percentage
    percent = get_percentage(pass_num, total_num)
    data['percent'] = percent
    data['total_pass'] = sum((pass_num))
    data['total_fail'] = sum((fail_num))
    data['start_time'] = start
    data['end_time'] = end
    return data


def get_product_info(start, end, product):
    command = '''
select ORDER_ID,ORDER_NUMBER,SAP_NUMBER,EXECUTION_TIME,PRODUCTION_STATUS from dbo.SECOND_TestData where START_DATE_TIME between '%s' and '%s'
    ''' % (start, end)
    print(start)
    print(end)
    db = SQL(server="BSCE-TE-HP", user="sa", pwd="yjx199855", db="GUI_test_db")
    search_data = db.ExecQuery(command)
    ret = generate_data(search_data)
    data = dict()
    for x in ret:
        temp_dict = dict()
        temp_dict["PASS"] = ret[x][1]
        temp_dict["FAIL"] = ret[x][0]
        data[x] = temp_dict

    return data[product]


def total_info(data):
    productions = dict()
    temp_dict = dict()
    for x in data:
        if x[0] not in productions:
            if x[-1] == "PASS":
                temp_dict["PASS"] = 1
                temp_dict["FAIL"] = 0
                productions[x[0]] = temp_dict
            else:
                temp_dict["FAIL"] = 1
                temp_dict["PASS"] = 0
                productions[x[0]] = temp_dict
        else:
            if x[-1] == "PASS":
                temp_dict = productions[x[0]]
                num = temp_dict["PASS"]
                num += 1
                temp_dict["PASS"] = num
                productions[x[0]] = temp_dict
            else:
                temp_dict = productions[x[0]]
                num = temp_dict["FAIL"]
                num += 1
                temp_dict["FAIL"] = num
                productions[x[0]] = temp_dict

    return productions


def total_info1(data):
    productions = dict()
    product = list()
    type = list()
    print(data)
    for x in data:
        if x[0] not in type:
            type.append(x[0])
        if x[0] not in productions:
            product.append(x[0])
            productions[x[0]] = single_info(x)
        else:
            if x[2] not in productions[x[0]]:
                productions[x[0]][x[2]] = x[1]
            else:
                productions[x[0]][x[2]] += x[1]

    productions["production"] = product
    productions["total_type"] = ("PASS")
    return productions

def single_info(product):
    single = dict()
    single[product[2]] = product[1]

    return single
def second_deal(data):
    print(data)
    for x in data:
        if x != "total_type" and x != "production":
            if len(data[x]) != len(data["total_type"]):
                for y in data["total_type"]:
                    if y not in data[x]:
                        data[x][y] = 0

    # sort the stuff over here
    for x in data:
        if x != "total_type" and x != "production":
            data[x] = sorted(data[x].items(), key=lambda x: x[0])

    return data


def real_time_info(start, end):
    command = "select ORDER_ID,ORDER_NUMBER,SAP_NUMBER,EXECUTION_TIME,PRODUCTION_STATUS from dbo.SECOND_TestData where START_DATE_TIME between '%s' and '%s'" % (start, end)

    # print(command)
    # establish the sql, and have the data returned
    db = SQL(server="BSCE-TE-HP", user="sa", pwd="yjx199855", db="GUI_test_db")
    search_data = db.ExecQuery(command)
    ret = generate_data(search_data)
    data = dict()
    for x in ret:
        temp_dict = dict()
        temp_dict["PASS"] = ret[x][1]
        temp_dict["FAIL"] = ret[x][0]
        data[x] = temp_dict
    #data = total_info1(search_data)
    #data = second_deal(data)

    other_data = dict()
    product = list()
    fail_num = list()
    pass_num = list()
    total_num = list()
    for x in ret:
        product.append(x)
        fail_num.append(ret[x][0])
        pass_num.append(ret[x][1])
        total_num.append(ret[x][2])
    data['production'] = product
    other_data['fail'] = fail_num
    other_data['pass'] = pass_num
    other_data['total'] = total_num

    # get the pass percentage
    percent = get_percentage(pass_num, total_num)
    other_data['percent'] = percent
    other_data['total_pass'] = sum((pass_num))
    other_data['total_fail'] = sum((fail_num))
    other_data['start_time'] = start
    other_data['end_time'] = end


    # pat color over here
    color = create_pat_color(len(data["production"]))
    data['color'] = color
    data["total_type"] = ("PASS","FAIL")
    # Get the total num, pass num, fail num, and the percentage
    data["other_graph"] = other_data
    print(data)

    return data


def get_nums(data):
    other_graph = dict()
    num_pass = list()
    num_fail = list()
    num_total = list()
    num_percent = list()

    for x in data["production"]:
        # print(data[x])
        product_info = data[x]
        fail = 0
        for y in product_info:

            if y[0] != "Passed":
                fail += y[1]
            else:
                num_pass.append(y[1])
                pass_num = y[1]

        num_fail.append(fail)
        total_num = pass_num + fail
        percent = (pass_num / total_num) * 100
        num_percent.append(percent)

    other_graph["pass"] = num_pass
    other_graph["fail"] = num_fail
    other_graph["total"] = num_pass + num_fail
    other_graph["percent"] = num_percent
    other_graph["total_pass"] = sum(num_pass)
    other_graph["total_fail"] = sum(num_fail)
    # print(other_graph)
    return other_graph


def create_pat_color(length):
    color = list()
    head = 'rgba('
    tail = ',0.6)'
    # start_color = list()
    for x in range(0, length):
        first_color = (30 * x) % 255
        second_color = (50 * x) % 255
        third_color = (70 * x) % 255
        temp = head + str(first_color) + ',' + str(second_color) + ',' + str(third_color) + tail
        color.append(temp)

    return color


if __name__ == '__main__':
    # select_period("2018-2-1","2018-3-2",1,0)
    start = '2019-07-09 08:00:00.000'
    end = '2019-07-09 20:00:00.000'
    #get_db_data(start, end, 1, 0)
    get_product_info(start,end, '2')
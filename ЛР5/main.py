# Отладка станка 0,2-0,5
# Время выполнения задачи 0.5 и среднекв. отклонение 0.1
# Поломка 20 и среднекв. отклонение 2
# Устранение поломки 0,1-0,5
# 500 деталей

import numpy as np

def get_time_before_next_task():
    return round(np.random.exponential(1.), 2) # экспоненциальное распред
def get_time_before_machine_break():
    return round(np.random.normal(20., 2.), 2) # нормальное распред
def get_setting_machine():
    return round(np.random.uniform(.2, .5), 2) # равномерное распред
def get_task_execution():
    return round(np.random.normal(.5, .1), 2)

def get_repair_time():
    return round(np.random.uniform(.1, .5), 2)


def work(kol_tasks, total_time_machine=0):
    details = kol_tasks
    s=1
    rab=0.0
    kol_det_in_que = 0
    kol_brok = 0 # кол-во поломок станка
    total_repair_time = 0
    time_before_next_task = get_time_before_next_task() # время до следующего задания
    time_to_broke = get_time_before_machine_break() # время до поломки станка
    while details > 0:
        if time_before_next_task > 0: # если время до след задания не равно 0
            total_time_machine += time_before_next_task # добавляем время ожидания задания к общему времени работы
            s += time_before_next_task
            time_before_next_task = 0


        set_machine = get_setting_machine() # настройка станка
        task_execution = get_task_execution() # время выполненния задания
        time_one_task = set_machine + task_execution # время отладки + выполнения для одного задания
        if time_one_task < time_to_broke: # время отладки + выполнения меньше чем время до поломки
            rab+=time_one_task
            time_before_next_task += get_time_before_next_task()
            total_time_machine += time_one_task # к общему времени работы станка добавляем время выполнения одного задания
            time_to_broke -= time_one_task # от времени до поломки отнимаем выполнение одного задания
            time_before_next_task -= time_one_task # от времени до след. задания отнимаем время вып. одного задания

            details -= 1 # задание выполнилось
        else:
            kol_brok += 1 # если до поломки не успели выполнить задание
            total_time_machine += time_to_broke # общее время работы станка + время простоя
            s+=time_to_broke
            time_before_next_task -= time_to_broke
            repair_time = get_repair_time() # время устранение поломки станка

            total_time_machine += repair_time
            time_before_next_task -= repair_time
            time_to_broke = get_time_before_machine_break()
            total_repair_time += repair_time
    while time_before_next_task < 0:
        time_before_next_task += get_time_before_next_task()
        kol_det_in_que += 1
    return kol_brok, total_time_machine, total_time_machine / kol_tasks, kol_det_in_que, total_repair_time , s,rab


kol_tasks = 500
res = work(kol_tasks)
#print("________________________________________________________________________")
print(f'Количество заданий: {kol_tasks}\n'
f'Количество поломок станка: {res[0]}\n'
f'Время работы: {int(res[1])} часов {int(res[1] % 60)} мин.\n'
f'Деталей в очереди (после выполнения 500 заданий): {res[3]}\n'
f'Общее время починки: {int(res[4])} часов {int(res[4] % 60)} мин.\n'
f'Время простоя: {int(res[5])} часов {int(res[5] % 60)} мин\n'
f'Эффективное рабочее время:{int(res[6])} часов {int(res[6] % 60)} мин'      )
#print("________________________________________________________________________")

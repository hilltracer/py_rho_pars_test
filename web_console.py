import base64
import time
from datetime import datetime

import requests


def send_explore_deploy(deploy_data: str):
    return requests.post('http://localhost:40403/api/explore-deploy', data=deploy_data)


if __name__ == '__main__':
    while True:
        command = input('> ')

        if command.startswith('sum'):
            num_of_experiments = 5
            step_size = 10
            for j in range(num_of_experiments):
                phlo_price, valid = (1, 0)
                print("experiment number = " + str(j))
                size = step_size + step_size * j
                contract = """
                new return, loop in {
                  contract loop(@n, @acc, ret) = {
                    if (n == 0) ret!(acc)
                    else loop!(n - 1, acc + n, *ret)
                  } |
                  loop!(%s, 0, *return)
                }
                """ % size
                t1 = datetime.now()
                ans = send_explore_deploy(contract)
                t2 = datetime.now()
                t_m = (t2 - t1).seconds + (t2 - t1).microseconds / 1000000
                # print(ans.text)
                print(f"{size},   {t_m}")

        elif command.startswith('list'):
            num_of_experiments = 5
            step_size = 10
            for j in range(num_of_experiments):
                phlo_price, valid = (1, 0)
                size = step_size + step_size * j
                contract = """
                new return, loop in {
                contract loop(@n, @acc, ret) = {
                if (n == 0) ret!(acc)
                else loop!(n - 1, acc ++ [n], *ret)
                    } |
                    loop!(%s, [], *return)
                }
                """ % size
                t1 = datetime.now()
                ans = send_explore_deploy(contract)
                t2 = datetime.now()
                t_m = (t2 - t1).seconds + (t2 - t1).microseconds / 1000000
                # print(ans.text)
                print(f"{size}, {t_m}")

        elif command.startswith('set'):
            num_of_experiments = 5
            step_size = 100
            for j in range(num_of_experiments):
                phlo_price, valid = (1, 0)
                print("experiment number = " + str(j))
                size = step_size + step_size * j
                contract = """
                new return, loop in {
                  contract loop(@n, @acc, ret) = {
                    if (n == 0) ret!(acc)
                    else loop!(n - 1, acc.add(n), *ret)
                  } |
                  loop!(%s, Set(), *return)
                }                
                """ % size
                t1 = datetime.now()
                ans = send_explore_deploy(contract)
                t2 = datetime.now()
                t_m = (t2 - t1).seconds + (t2 - t1).microseconds / 1000000
                # print(ans.text)
                print(f"{size}, {t_m}")

        elif command.startswith('mapWithLoop1'):
            num_of_experiments = 5
            step_size = 100
            for j in range(num_of_experiments):
                phlo_price, valid = (1, 0)
                size = step_size + step_size * j
                contract = """
                new return, loop in {
                  contract loop(@n, @acc, ret) = {
                    if (n == 0) ret!(acc)
                    else loop!(n - 1, acc.set(n, n), *ret)
                  } |
                  loop!(%s, {}, *return)
                }
                """ % size
                t1 = datetime.now()
                ans = send_explore_deploy(contract)
                t2 = datetime.now()
                t_m = (t2 - t1).seconds + (t2 - t1).microseconds / 1000000
                # print(ans.text)
                print(f"{size}, {t_m}")

        elif command.startswith('mapWithLoop2'):
            num_of_experiments = 5
            step_size = 100
            for j in range(num_of_experiments):
                phlo_price, valid = (1, 0)
                size = step_size + step_size * j
                contract = """
                    @{"loop"}!(%s, {}) |
                    for( @{x0}, @{x1} <= @{"loop"} ) {
                      match (x0 == 0) {
                        true => {
                          Nil
                        }
                        false => {
                          @{"loop"}!((x0 - 1), (x1).set(x0,x0))
                        }
                      }
                    }
                 """ % size
                t1 = datetime.now()
                ans = send_explore_deploy(contract)
                t2 = datetime.now()
                t_m = (t2 - t1).seconds + (t2 - t1).microseconds / 1000000
                # print(ans.text)
                print(f"{size}, {t_m}")

        elif command.startswith('mapWithoutLoop'):
            num_of_experiments = 5
            step_size = 100
            for j in range(num_of_experiments):
                phlo_price, valid = (1, 0)
                size = step_size + step_size * j
                map_primitives = "{}"
                for k in range(1, size+1):
                    map_primitives = map_primitives + ".set(%s,%s)" % (k, k)
                contract = """
                new return, loop in {
                  contract loop(ret) = {
                    ret!(%s)
                  } |
                  loop!(*return)
                }
                """ % map_primitives
                t1 = datetime.now()
                ans = send_explore_deploy(contract)
                t2 = datetime.now()
                t_m = (t2 - t1).seconds + (t2 - t1).microseconds / 1000000
                # print(ans.text)
                print(f"{size}, {t_m}")

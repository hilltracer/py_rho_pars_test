import array
import base64
import random
import time

import requests
from rchain.crypto import PrivateKey
from rchain.util import create_deploy_data


def create_deploy(contract: str, private, phlo_price=1, valid_after_block_no=0):
    return create_deploy_data(key=private,
                              term=contract, phlo_price=phlo_price,
                              phlo_limit=100000000,
                              valid_after_block_no=valid_after_block_no,
                              timestamp_millis=int(time.time() * 1000))


# don't work =(
def get_lfs():
    json = {'depth': 1}
    return requests.post('http://localhost:40403/api/show_blocks', json=json)


def send_deploy(deploy_data):
    json = {
        'data': {
            'term': deploy_data.term,
            'timestamp': deploy_data.timestamp,
            'phloPrice': deploy_data.phloPrice,
            'phloLimit': deploy_data.phloLimit,
            'validAfterBlockNumber': deploy_data.validAfterBlockNumber
        },
        'sigAlgorithm': deploy_data.sigAlgorithm,
        'signature': base64.b16encode(deploy_data.sig),
        'deployer': base64.b16encode(deploy_data.deployer)
    }
    return requests.post('http://localhost:40403/api/deploy', json=json)


def propose():
    return requests.post('http://localhost:40405/api/propose')


def get_result(sig: str):
    json = {'depth': 1, 'name': {'UnforgDeploy': {'data': sig}}}
    return requests.post('http://localhost:40403/api/data-at-name', json=json)


if __name__ == '__main__':

    private = PrivateKey.from_hex('2df2c1c8de1c3469370deed79c2a74eaced38d486fd46d62829a0ead30587565')
    valid_after_block_no = 10
    deploy_data = None

    while True:
        command = input('> ')

        if command.startswith('deploy'):
            contract = command.replace('deploy ', '')
            print(contract)
            phlo_price, valid = [int(item) for item in input('phlo price, valid after: ').split()]
            deploy_data = create_deploy(contract, private, phlo_price, valid)
            ans = send_deploy(deploy_data)
            print(ans.text)

        elif command.startswith('my'):
            phlo_price, valid = [int(item) for item in input('phlo price, valid after: ').split()]
            size = 1000  # number of channels in deploy
            secs = 10
            num_of_levels = 250

            for j in range(num_of_levels):
                print("experiment number = " + str(j))
                mas = array.array('i', range(size))
                for i in range(size):
                    mas[i] = random.randrange(10000000)
                contract = "new "
                if size > 1:
                    for i in range(size - 1):
                        contract = contract + "a" + str(mas[i]) + ","

                contract = contract + "a" + str(mas[size - 1])

                contract = contract + " in{"

                if size > 1:
                    for i in range(size - 1):
                        contract = contract + "for(b" + str(mas[i]) + "<-a" + str(mas[i]) + "){Nil}|"

                contract = contract + "for(b" + str(mas[size - 1]) + "<-a" + str(mas[size - 1]) + "){Nil}"

                contract = contract + "}"
                deploy_data = create_deploy(contract, private, phlo_price, valid + j)
                ans = send_deploy(deploy_data)
                print(ans.text)
                ans = propose()
                print(ans.text)
                time.sleep(secs)

        elif command.startswith('valid_after_block_no'):
            _, no = command.split()
            valid_after_block_no = int(no)
        elif command.startswith('propose'):
            ans = propose()
            print(ans.text)
        elif command.startswith('result'):
            ans = get_result(str(base64.b16encode(deploy_data.sig)))
            print(ans.text)

        elif command.startswith('lfs'):
            ans = get_lfs()
            print(ans.text)
        elif command.startswith('exit'):
            break

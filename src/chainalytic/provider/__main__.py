import os
import argparse
import websockets
import asyncio
import time
from jsonrpcserver import method
from chainalytic.common.rpc_server import EXIT_SERVICE, main_dispatcher
from . import Provider

_PROVIDER = None


@method
async def _call(call_id: str, **kwargs):
    params = kwargs
    print(f'Call: {call_id}')
    if call_id == 'ping':
        message = ''.join(
            [
                'Pong !\n',
                'Provider service is running\n',
                f'Working dir: {_PROVIDER.working_dir}\n',
                f'Params: {params}',
            ]
        )
        return message
    elif call_id == 'exit':
        return EXIT_SERVICE
    else:
        return f'Not implemented'


def _run_server(endpoint, working_dir):
    global _PROVIDER
    _PROVIDER = Provider(working_dir)
    print(f'Provider endpoint: {endpoint}')

    host = endpoint.split(':')[0]
    port = int(endpoint.split(':')[1])
    start_server = websockets.serve(main_dispatcher, host, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    print('Initialized Provider')


# Command to run server, assume you are in root directory of Git repo
# venv/bin/python -m chainalytic.provider --endpoint localhost:5520 --working_dir .
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chainalytic Provider server')
    parser.add_argument('--endpoint', type=str, help='Endpoint of Provider server')
    parser.add_argument('--working_dir', type=str, help='Current working directory')
    args = parser.parse_args()
    endpoint = args.endpoint
    working_dir = args.working_dir if args.working_dir != '.' else os.getcwd()
    _run_server(endpoint, working_dir)

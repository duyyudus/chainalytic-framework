from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from chainalytic.common import config, rpc_client
from chainalytic.common.util import get_child_logger


class BaseKernel(object):
    """
    Base class for different Kernel implementations

    Properties:
        working_dir (str):
        zone_id (str):
        transforms (dict):
        chain_registry (dict):
        warehouse_endpoint (str):

    Methods:
        add_transform(transform: Transform)
        execute(height: int, input_data: Dict, transform_id: str)
    """

    def __init__(self, working_dir: str, zone_id: str):
        super(BaseKernel, self).__init__()
        self.working_dir = working_dir
        self.zone_id = zone_id
        self.transforms = {}
        self.chain_registry = config.get_chain_registry(working_dir)
        self.warehouse_endpoint = config.get_setting(working_dir)['warehouse_endpoint']

        self.logger = get_child_logger('aggregator.kernel')

    def add_transform(self, transform: 'Transform'):
        self.transforms[transform.transform_id] = transform
        transform.set_kernel(self)

    async def execute(self, height: int, input_data: Any, transform_id: str) -> Optional[bool]:
        """Execute transform and push output data to warehouse
        """
        output = None
        if transform_id in self.transforms:
            output = await self.transforms[transform_id].execute(height, input_data)
        if not output:
            return 0

        # Sample
        r = await rpc_client.call_async(
            self.warehouse_endpoint,
            call_id='api_call',
            api_id='put_block',
            api_params={
                'height': output['height'],
                'data': output['data'],
                'transform_id': transform_id,
            },
        )
        return r['status']

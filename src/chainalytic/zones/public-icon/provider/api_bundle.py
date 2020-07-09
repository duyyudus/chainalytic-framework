"""
Example API call

from chainalytic.common import rpc_client

rpc_client.call_aiohttp(
    'localhost:5530',
    call_id='api_call',
    api_id='get_staking_info',
    api_params={'height': 9999999}
)

"""

from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from chainalytic.common import config
from chainalytic.common import util
from chainalytic.provider.api_bundle import BaseApiBundle


class ApiBundle(BaseApiBundle):
    """
    The interface to external consumers/applications
    """

    def __init__(self, working_dir: str, zone_id: str):
        super(ApiBundle, self).__init__(working_dir, zone_id)

    async def get_staking_info(self, api_params: dict) -> Optional[dict]:
        if 'height' in api_params:
            return await self.collator.get_block(api_params['height'], 'stake_history')

    async def last_block_height(self, api_params: dict) -> Optional[int]:
        if 'transform_id' in api_params:
            return await self.collator.last_block_height(api_params['transform_id'])

    async def get_staking_info_last_block(self, api_params: dict) -> Optional[Dict]:
        height = await self.collator.last_block_height('stake_history')
        if height:
            r = await self.collator.get_block(height, 'stake_history')
            if r:
                r['height'] = height
                return r

    async def latest_unstake_state(self, api_params: dict) -> Optional[int]:
        return await self.collator.latest_unstake_state('stake_history')

    async def latest_stake_top100(self, api_params: dict) -> Optional[dict]:
        return await self.collator.latest_stake_top100('stake_top100')

    async def recent_stake_wallets(self, api_params: dict) -> Optional[dict]:
        return await self.collator.recent_stake_wallets('recent_stake_wallets')

    async def abstention_stake(self, api_params: dict) -> Optional[dict]:
        return await self.collator.abstention_stake('abstention_stake')

    async def funded_wallets(self, api_params: dict) -> Optional[dict]:
        return await self.collator.funded_wallets(
            'funded_wallets', float(api_params['min_balance']) if 'min_balance' in api_params else 1
        )

    async def passive_stake_wallets(self, api_params: dict) -> Optional[dict]:
        return await self.collator.passive_stake_wallets(
            'passive_stake_wallets',
            int(api_params['max_inactive_duration'])
            if 'max_inactive_duration' in api_params
            else 1296000,  # One month
        )

    async def contract_transaction(self, api_params: dict) -> Optional[dict]:
        return await self.collator.contract_transaction(
            'contract_history', api_params['address'], int(api_params['size'])
        )

    async def contract_internal_transaction(self, api_params: dict) -> Optional[dict]:
        return await self.collator.contract_internal_transaction(
            'contract_history', api_params['address'], int(api_params['size'])
        )

    async def contract_stats(self, api_params: dict) -> Optional[dict]:
        return await self.collator.contract_stats('contract_history', api_params['address'])

    async def contract_list(self, api_params: dict) -> Optional[dict]:
        return await self.collator.contract_list('contract_history')

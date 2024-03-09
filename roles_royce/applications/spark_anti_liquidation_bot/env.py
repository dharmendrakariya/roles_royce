from dataclasses import dataclass, field
import threading
from prometheus_client import Gauge
import schedule
import time
from decouple import config
from web3.types import Address, ChecksumAddress
from web3 import Web3
from roles_royce.toolshed.alerting.alerting import Messenger, LoggingLevel
from roles_royce.toolshed.anti_liquidation.spark import SparkCDP
import logging
from roles_royce.applications.utils import custom_config, to_dict
import json


@dataclass
class ENV:
    RPC_ENDPOINT: str = config('RPC_ENDPOINT')
    RPC_ENDPOINT_FALLBACK: str = config('FALLBACK_RPC_ENDPOINT', default='')
    AVATAR_SAFE_ADDRESS: Address | ChecksumAddress | str = config('AVATAR_SAFE_ADDRESS')
    ROLES_MOD_ADDRESS: Address | ChecksumAddress | str = config('ROLES_MOD_ADDRESS')
    ROLE: int = config('ROLE', cast=int)
    PRIVATE_KEY: str = config('PRIVATE_KEY')
    TARGET_HEALTH_FACTOR: float = config('TARGET_HEALTH_FACTOR', cast=float)
    THRESHOLD_HEALTH_FACTOR: float = config('THRESHOLD_HEALTH_FACTOR', cast=float)
    ALERTING_HEALTH_FACTOR: float | None = custom_config('ALERTING_HEALTH_FACTOR', default=None, cast=float)
    TOLERANCE: float = custom_config('TOLERANCE', default=0.01, cast=float)
    COOLDOWN_MINUTES: int = custom_config('COOLDOWN_MINUTES', default=5, cast=int)
    SLACK_WEBHOOK_URL: str = config('SLACK_WEBHOOK_URL', default='')
    TELEGRAM_BOT_TOKEN: str = config('TELEGRAM_BOT_TOKEN', default='')
    TELEGRAM_CHAT_ID: int = custom_config('TELEGRAM_CHAT_ID', default='', cast=int)
    PROMETHEUS_PORT: int = custom_config('PROMETHEUS_PORT', default=8000, cast=int)
    TEST_MODE: bool = config('TEST_MODE', default=False, cast=bool)
    LOCAL_FORK_PORT: int = custom_config('LOCAL_FORK_PORT', default=8545, cast=int)
    STATUS_NOTIFICATION_HOUR: int = custom_config('STATUS_NOTIFICATION_HOUR', default='', cast=int)

    BOT_ADDRESS: Address | ChecksumAddress | str = field(init=False)

    def __post_init__(self):
        self.AVATAR_SAFE_ADDRESS = Web3.to_checksum_address(self.AVATAR_SAFE_ADDRESS)
        self.ROLES_MOD_ADDRESS = Web3.to_checksum_address(self.ROLES_MOD_ADDRESS)
        if not Web3(Web3.HTTPProvider(self.RPC_ENDPOINT)).is_connected():
            raise ValueError(f"RPC_ENDPOINT is not valid or not active: {self.RPC_ENDPOINT}.")
        if self.RPC_ENDPOINT_FALLBACK != '':
            if not Web3(Web3.HTTPProvider(self.RPC_ENDPOINT_FALLBACK)).is_connected():
                raise ValueError(f"FALLBACK_RPC_ENDPOINT is not valid or not active: {self.RPC_ENDPOINT_FALLBACK}.")
        self.BOT_ADDRESS = Web3(Web3.HTTPProvider(self.RPC_ENDPOINT)).eth.account.from_key(self.PRIVATE_KEY).address
        if not self.ALERTING_HEALTH_FACTOR:
            self.ALERTING_HEALTH_FACTOR = (self.TARGET_HEALTH_FACTOR + self.THRESHOLD_HEALTH_FACTOR) / 2

    def __str__(self):
        return json.dumps(to_dict(self, exclude_key="PRIVATE_KEY"), indent=4)

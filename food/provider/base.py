from abc import ABC, abstractmethod

class BaseDeliveryClient(ABC):
    @abstractmethod
    def start_delivery(self, order_id: int, webhook_url: str) -> str:

        raise NotImplementedError

from abc import abstractmethod
from typing import Awaitable, Callable, Protocol


class DataProvider(Protocol):
    @abstractmethod
    def get_file_data(self, file_name: str) -> bytes | None:
        pass

    def get_file_data_from_branch(self, file_name: str, branch: str) -> bytes | None:
        """Get file data from a specific branch, defaults to main"""
        return self.get_file_data(file_name)

    def subscribe_config_changes(
        self, callback: Callable[[], None | Awaitable[None]]
    ) -> Callable[[], None]:
        """Register ``callback`` to be notified that main configuration changed.

        The notification is generic: it only ever concerns the main branch and
        carries no data. In response the callback is expected to re-fetch via
        :meth:`get_file_data` and refresh immediately.

        The callback takes no arguments and may be either sync or a coroutine
        function. When it returns an awaitable, the provider awaits it to
        completion before treating the notification as handled, so the refresh
        happens immediately rather than on the next request. The provider is
        responsible for invoking the callback on a running event loop.

        Returns a zero-arg callable that unsubscribes. The default implementation
        is a no-op: the provider has no notification channel and callers should
        rely on their own TTL/polling fallback.
        """
        return lambda: None
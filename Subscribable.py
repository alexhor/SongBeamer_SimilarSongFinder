class Subscribable:
    """Registered subscription callbacks"""
    _subscriptions: dict[int, list[callable]]

    def __init__(self, available_subscription_types):
        """Setup subscriptions
        :type available_subscription_types: tuple[int]
        :param available_subscription_types: All subscription types to add"""
        # Setup subscriptions
        self._subscriptions = {}
        for subscriptionType in available_subscription_types:
            self._subscriptions[subscriptionType] = []

    def subscribe(self, subscription_type, callback):
        """Register a new subscription
        :type subscription_type: int
        :param subscription_type: The type of subscription
        :type callback: callable
        :param callback: The callback to register for the subscription
        """
        if subscription_type in self._subscriptions.keys():
            self._subscriptions[subscription_type].append(callback)

    def _trigger_subscriptions(self, subscription_type, *args, **kwargs):
        """Run all subscriptions for the given type
        :type subscription_type: int
        :param subscription_type: The type of subscription to trigger
        :type args: Any
        :param args: Arguments to pass to the callback functions
        :type kwargs: Any
        :param kwargs: Named arguments to pass to the callback functions
        """
        if subscription_type in self._subscriptions.keys():
            # Run every subscribed callback
            for callback in self._subscriptions[subscription_type]:
                try:
                    callback(*args, **kwargs)
                except AttributeError:
                    continue

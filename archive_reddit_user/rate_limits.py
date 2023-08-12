# rate_limiter.py

import datetime

class RateLimits:
    def __init__(self, reddit_instance):
        self.reddit = reddit_instance

    def get_rate_limits(self):
        """Return the current rate limits from the reddit instance."""
        return self.reddit.auth.limits

    def display_rate_limits(self):
        rate_limits = self.get_rate_limits()

        remaining = rate_limits.get('remaining', 'N/A')
        reset_timestamp = rate_limits.get('reset_timestamp', 'N/A')
        used = rate_limits.get('used', 'N/A')

        readable_reset_time = datetime.datetime.utcfromtimestamp(reset_timestamp).strftime('%Y-%m-%d %H:%M:%S') if reset_timestamp != 'N/A' else 'N/A'

        print(f"You have used {used} out of your available requests. {remaining} requests remain.")
        print(f"The rate limits will reset at {readable_reset_time}.")

import pytest

import ray
from ray import serve


def test_controller_inflight_requests_clear(serve_instance):
    controller = serve.api._global_client._controller
    initial_number_reqs = ray.get(controller._num_pending_goals.remote())

    @serve.deployment
    def test(_):
        return "hello"

    test.deploy()

    assert ray.get(
        controller._num_pending_goals.remote()) - initial_number_reqs == 0


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(["-v", "-s", __file__]))

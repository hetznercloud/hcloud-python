
class TestLoadBalancerTypesClient(object):

    def test_get_by_id(self, hetzner_client):
        load_balancer_type = hetzner_client.load_balancer_types.get_by_id(1)
        assert load_balancer_type.id == 1
        assert load_balancer_type.name == "lb11"

    def test_get_by_name(self, hetzner_client):
        load_balancer_type = hetzner_client.load_balancer_types.get_by_name("lb11")
        assert load_balancer_type.id == 1
        assert load_balancer_type.name == "lb11"

    def test_get_list(self, hetzner_client):
        result = hetzner_client.load_balancer_types.get_list()
        load_balancer_types = result.load_balancer_types
        assert load_balancer_types[0].id == 1
        assert load_balancer_types[0].name == "lb11"

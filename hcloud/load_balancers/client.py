# -*- coding: utf-8 -*-
from hcloud.certificates.client import BoundCertificate
from hcloud.servers.client import BoundServer

from hcloud.load_balancer_types.client import BoundLoadBalancerType
from hcloud.locations.client import BoundLocation
from hcloud.networks.client import BoundNetwork

from hcloud.core.client import ClientEntityBase, BoundModelBase, GetEntityByNameMixin
from hcloud.core.domain import add_meta_to_result

from hcloud.actions.client import BoundAction
from hcloud.load_balancers.domain import LoadBalancer, IPv4Address, IPv6Network, PublicNetwork, PrivateNet, \
    CreateLoadBalancerResponse, LoadBalancerTarget, LoadBalancerService, LoadBalancerServiceHttp, \
    LoadBalancerHealthCheck, LoadBalancerHealtCheckHttp, LoadBalancerAlgorithm


class BoundLoadBalancer(BoundModelBase):
    model = LoadBalancer

    def __init__(self, client, data, complete=True):
        algorithm = data.get("algorithm")
        if algorithm:
            data['algorithm'] = LoadBalancerAlgorithm(type=algorithm['type'])

        public_net = data.get("public_net")
        if public_net:
            ipv4_address = IPv4Address(**public_net['ipv4'])
            ipv6_network = IPv6Network(**public_net['ipv6'])
            data['public_net'] = PublicNetwork(ipv4=ipv4_address, ipv6=ipv6_network, enabled=public_net['enabled'])

        private_nets = data.get("private_net")
        if private_nets:
            private_nets = [PrivateNet(
                network=BoundNetwork(client._client.networks, {"id": private_net['network']}, complete=False),
                ip=private_net['ip']) for private_net in private_nets]
            data['private_net'] = private_nets

        targets = data.get("targets")
        if targets:
            tmp_targets = []
            for target in targets:
                tmp_target = LoadBalancerTarget(type=target["type"], use_private_ip=target["use_private_ip"])
                if target["type"] == "server":
                    tmp_target.server = BoundServer(client._client.servers, data=target['server'], complete=False)
                tmp_targets.append(tmp_target)
            data['targets'] = tmp_targets

        services = data.get("services")
        if services:
            tmp_services = []
            for service in services:
                tmp_service = LoadBalancerService(protocol=service["protocol"], listen_port=service["listen_port"],
                                                  destination_port=service["destination_port"],
                                                  proxyprotocol=service["proxyprotocol"])
                if service["protocol"] != "tcp":
                    tmp_service.http = LoadBalancerServiceHttp(sticky_sessions=service['http']['sticky_sessions'],
                                                               redirect_http=service['http']['redirect_http'],
                                                               cookie_name=service['http']['cookie_name'],
                                                               cookie_lifetime=service['http']['cookie_lifetime'])
                    tmp_service.http.certificates = [
                        BoundCertificate(client._client.certificates, {"id": certificate}, complete=False) for
                        certificate in
                        service['http']['certificates']]

                tmp_service.health_check = LoadBalancerHealthCheck(protocol=service['health_check']['protocol'],
                                                                   port=service['health_check']['port'],
                                                                   interval=service['health_check']['interval'],
                                                                   retries=service['health_check']['retries'],
                                                                   timeout=service['health_check']['timeout'])
                if tmp_service.health_check.protocol != "tcp":
                    tmp_service.health_check.http = LoadBalancerHealtCheckHttp(
                        domain=service['health_check']['http']['domain'], path=service['health_check']['http']['path'],
                        response=service['health_check']['http']['response'],
                        tls=service['health_check']['http']['tls'],
                        status_codes=service['health_check']['http']['status_codes'])
                tmp_services.append(tmp_service)
            data['services'] = tmp_services

        load_balancer_type = data.get("load_balancer_type")
        if load_balancer_type is not None:
            data['load_balancer_type'] = BoundLoadBalancerType(client._client.load_balancer_types, load_balancer_type)

        location = data.get("location")
        if location is not None:
            data['location'] = BoundLocation(client._client.locations, location)

        super(BoundLoadBalancer, self).__init__(client, data, complete)

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundLoadBalancer
        """Updates a Load Balancer. You can update a Load Balancers name and a Load Balancers labels.

         :param name: str (optional)
                New name to set
         :param labels: Dict[str, str] (optional)
                User-defined labels (key-value pairs)
         :return: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>`
         """
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> BoundAction
        """Deletes a Load Balancer.

        :return: boolean
        """
        return self._client.delete(self)

    def get_actions_list(self, status=None, sort=None, page=None, per_page=None):
        # type: (Optional[List[str]], Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction, Meta]]
        """Returns all action objects for a Load Balancer.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundAction <hcloud.actions.client.BoundAction>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        return self._client.get_actions_list(self, status, sort, page, per_page)

    def get_actions(self, status=None, sort=None):
        # type: (Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for a Load Balancer.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status, sort)

    def add_service(self, service):
        # type: (LoadBalancerService) -> List[BoundAction]
        """Adds a service to a Load Balancer.

        :param service: :class:`LoadBalancerService <hcloud.load_balancers.domain.LoadBalancerService>`
                       The LoadBalancerService you want to add to the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.add_service(self, service=service)

    def update_service(self, service):
        # type: (LoadBalancerService) -> List[BoundAction]
        """Updates a service of an Load Balancer.

        :param service: :class:`LoadBalancerService <hcloud.load_balancers.domain.LoadBalancerService>`
                       The LoadBalancerService you  want to update
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.update_service(self, service=service)

    def delete_service(self, service):
        # type: (LoadBalancerService) -> List[BoundAction]
        """Deletes a service from a Load Balancer.

        :param service: :class:`LoadBalancerService <hcloud.load_balancers.domain.LoadBalancerService>`
                       The LoadBalancerService you want to delete from the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.delete_service(self, service)

    def add_target(self, target):
        # type: (LoadBalancerTarget) -> List[BoundAction]
        """Adds a target to a Load Balancer.

        :param target: :class:`LoadBalancerTarget <hcloud.load_balancers.domain.LoadBalancerTarget>`
                       The LoadBalancerTarget you want to add to the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.add_target(self, target)

    def remove_target(self, target):
        # type: (LoadBalancerTarget) -> List[BoundAction]
        """Removes a target from a Load Balancer.

        :param target: :class:`LoadBalancerTarget <hcloud.load_balancers.domain.LoadBalancerTarget>`
                       The LoadBalancerTarget you want to remove from the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.remove_target(self, target)

    def change_algorithm(self, algorithm):
        # type: (LoadBalancerService) -> List[BoundAction]
        """Changes the algorithm used by the Load Balancer

        :param algorithm: :class:`LoadBalancerAlgorithm <hcloud.load_balancers.domain.LoadBalancerAlgorithm>`
                       The LoadBalancerAlgorithm you want to use
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_algorithm(self, algorithm)

    def change_protection(self, delete):
        # type: (LoadBalancerService) -> List[BoundAction]
        """Changes the protection configuration of a Load Balancer.

        :param delete: boolean
               If True, prevents the Load Balancer from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete)

    def attach_to_network(self, network, ip=None):
        # type: (Union[Network,BoundNetwork],Optional[str]) -> BoundAction
        """Attaches a Load Balancer to a Network

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param ip: str
                IP to request to be assigned to this Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.attach_to_network(self, network, ip)

    def detach_from_network(self, network):
        # type: ( Union[Network,BoundNetwork]) -> BoundAction
        """Detaches a Load Balancer from a Network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.detach_from_network(self, network)

    def enable_public_interface(self):
        # type: () -> BoundAction
        """Enables the public interface of a Load Balancer.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.enable_public_interface(self)

    def disable_public_interface(self):
        # type: ( Union[Network,BoundNetwork]) -> BoundAction
        """Disables the public interface of a Load Balancer.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.disable_public_interface(self)


class LoadBalancersClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "load_balancers"

    def get_by_id(self, id):
        # type: (int) -> BoundLoadBalancer
        """Get a specific Load Balancer

        :param id: int
        :return: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>
        """
        response = self._client.request(
            url="/load_balancers/{load_balancer_id}".format(load_balancer_id=id), method="GET"
        )
        return BoundLoadBalancer(self, response["load_balancer"])

    def get_list(
            self,
            name=None,  # type: Optional[str]
            label_selector=None,  # type: Optional[str]
            page=None,  # type: Optional[int]
            per_page=None,  # type: Optional[int]
    ):
        # type: (...) -> PageResults[List[BoundLoadBalancer], Meta]
        """Get a list of Load Balancers from this account

        :param name: str (optional)
               Can be used to filter Load Balancers by their name.
        :param label_selector: str (optional)
               Can be used to filter Load Balancers by labels. The response will only contain Load Balancers matching the label selector.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}
        if name is not None:
            params["name"] = name
        if label_selector is not None:
            params["label_selector"] = label_selector
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/load_balancers", method="GET", params=params)

        ass_load_balancers = [
            BoundLoadBalancer(self, load_balancer_data) for load_balancer_data in response["load_balancers"]
        ]
        return self._add_meta_to_result(ass_load_balancers, response)

    def get_all(self, name=None, label_selector=None):
        # type: (Optional[str], Optional[str]) -> List[BoundLoadBalancer]
        """Get all Load Balancers from this account

        :param name: str (optional)
               Can be used to filter Load Balancers by their name.
        :param label_selector: str (optional)
               Can be used to filter Load Balancers by labels. The response will only contain Load Balancers matching the label selector.
        :return: List[:class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>`]
        """
        return super(LoadBalancersClient, self).get_all(
            name=name, label_selector=label_selector
        )

    def get_by_name(self, name):
        # type: (str) -> BoundLoadBalancer
        """Get Load Balancer by name

        :param name: str
               Used to get Load Balancer by name.
        :return: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>`
        """
        return super(LoadBalancersClient, self).get_by_name(name)

    def create(
            self,
            name,  # type: str
            load_balancer_type,  # type: LoadBalancerType
            algorithm=None,  # type: Optional[LoadBalancerAlgorithm]
            services=None,  # type:  Optional[List[LoadBalancerService]]
            targets=None,  # type:  Optional[List[LoadBalancerTarget]]
            labels=None,  # type: Optional[Dict[str, str]]
            location=None,  # type: Optional[Location]
            network_zone=None,  # type: Optional[str]
            public_interface=None,  # type: Optional[bool]
            network=None  # type: Optional[Union[Network,BoundNetwork]]
    ):
        # type: (...) -> CreateLoadBalancerResponse:
        """Creates a Load Balancer .

        :param name: str
                Name of the Load Balancer
        :param load_balancer_type: LoadBalancerType
                Type of the Load Balancer
        :param labels: Dict[str, str] (optional)
                User-defined labels (key-value pairs)
        :param location: Location
                Location of the Load Balancer
        :param network_zone: str
                Network Zone of the Load Balancer
        :param algorithm: LoadBalancerAlgorithm (optional)
                The algorithm the Load Balancer is currently using
        :param services: LoadBalancerService
                The services the Load Balancer is currently serving
        :param targets: LoadBalancerTarget
                The targets the Load Balancer is currently serving
        :param public_interface: bool
                Enable or disable the public interface of the Load Balancer
        :param network: Network
                Adds the Load Balancer to a Network
        :return: :class:`CreateLoadBalancerResponse <hcloud.load_balancers.domain.CreateLoadBalancerResponse>`
        """
        data = {"name": name, "load_balancer_type": load_balancer_type.id_or_name}
        if network is not None:
            data["network"] = network.id
        if public_interface is not None:
            data["public_interface"] = public_interface
        if labels is not None:
            data["labels"] = labels
        if algorithm is not None:
            data["algorithm"] = {"type": algorithm.type}
        if services is not None:
            service_list = []
            for service in services:
                service_list.append(self.get_service_parameters(service))
            data["services"] = service_list

        if targets is not None:
            target_list = []
            for target in targets:
                target_data = {
                    "type": target.type,
                    "server": target.server,
                    "use_private_ip": target.use_private_ip
                }
                target_list.append(target_data)

            data["targets"] = target_list

        if network_zone is not None:
            data["network_zone"] = network_zone
        if location is not None:
            data["location"] = location.id_or_name

        response = self._client.request(url="/load_balancers", method="POST", json=data)

        return CreateLoadBalancerResponse(load_balancer=BoundLoadBalancer(self, response["load_balancer"]),
                                          action=BoundAction(self._client.actions, response['action']))

    def update(self, load_balancer, name=None, labels=None):
        # type:(LoadBalancer,  Optional[str],  Optional[Dict[str, str]]) -> BoundLoadBalancer
        """Updates a LoadBalancer. You can update a LoadBalancer’s name and a LoadBalancer’s labels.

        :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>`
        """
        data = {}
        if name is not None:
            data.update({"name": name})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(
            url="/load_balancers/{load_balancer_id}".format(load_balancer_id=load_balancer.id),
            method="PUT",
            json=data,
        )
        return BoundLoadBalancer(self, response["load_balancer"])

    def delete(self, load_balancer):
        # type: (LoadBalancer) -> BoundAction
        """Deletes a Load Balancer.

        :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :return: boolean
        """
        self._client.request(
            url="/load_balancers/{load_balancer_id}".format(load_balancer_id=load_balancer.id), method="DELETE"
        )
        return True

    def get_actions_list(
            self, load_balancer, status=None, sort=None, page=None, per_page=None
    ):
        # type: (LoadBalancer, Optional[List[str]], Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction], Meta]
        """Returns all action objects for a Load Balancer.

        :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundAction <hcloud.actions.client.BoundAction>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions".format(load_balancer_id=load_balancer.id),
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return add_meta_to_result(actions, response, "actions")

    def get_actions(self, load_balancer, status=None, sort=None):
        # type: (LoadBalancer, Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for a Load Balancer.

        :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return super(LoadBalancersClient, self).get_actions(
            load_balancer, status=status, sort=sort
        )

    def add_service(self, load_balancer, service):
        # type: (Union[LoadBalancer, BoundLoadBalancer], LoadBalancerService) -> List[BoundAction]
        """Adds a service to a Load Balancer.

        :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param service: :class:`LoadBalancerService <hcloud.load_balancers.domain.LoadBalancerService>`
                       The LoadBalancerService you want to add to the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = self.get_service_parameters(service)

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/add_service".format(load_balancer_id=load_balancer.id),
            method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def get_service_parameters(self, service):
        data = {}
        if service.protocol is not None:
            data["protocol"] = service.protocol
        if service.listen_port is not None:
            data["listen_port"] = service.listen_port
        if service.destination_port is not None:
            data["destination_port"] = service.destination_port
        if service.proxyprotocol is not None:
            data["proxyprotocol"] = service.proxyprotocol
        if service.http is not None:
            data["http"] = {}
            if service.http.cookie_name is not None:
                data["http"]["cookie_name"] = service.http.cookie_name
            if service.http.cookie_lifetime is not None:
                data["http"]["cookie_lifetime"] = service.http.cookie_lifetime
            if service.http.redirect_http is not None:
                data["http"]["redirect_http"] = service.http.redirect_http
            if service.http.sticky_sessions is not None:
                data["http"]["sticky_sessions"] = service.http.sticky_sessions
            certificate_ids = []
            for certificate in service.http.certificates:
                certificate_ids.append(certificate.id)
            data["http"]["certificates"] = certificate_ids
        if service.health_check is not None:
            data['health_check'] = {
                "protocol": service.health_check.protocol,
                "port": service.health_check.port,
                "interval": service.health_check.interval,
                "timeout": service.health_check.timeout,
                "retries": service.health_check.retries,
            }
            data["health_check"] = {}
            if service.health_check.protocol is not None:
                data["health_check"]["protocol"] = service.health_check.protocol
            if service.health_check.port is not None:
                data["health_check"]["port"] = service.health_check.port
            if service.health_check.interval is not None:
                data["health_check"]["interval"] = service.health_check.interval
            if service.health_check.timeout is not None:
                data["health_check"]["timeout"] = service.health_check.timeout
            if service.health_check.retries is not None:
                data["health_check"]["retries"] = service.health_check.retries
            if service.health_check.http is not None:
                data['health_check']['http'] = {}
                if service.health_check.http.domain is not None:
                    data['health_check']['http']['domain'] = service.health_check.http.domain
                if service.health_check.http.path is not None:
                    data['health_check']['http']['path'] = service.health_check.http.path
                if service.health_check.http.response is not None:
                    data['health_check']['http']['response'] = service.health_check.http.response
                if service.health_check.http.status_codes is not None:
                    data['health_check']['http']['status_codes'] = service.health_check.http.status_codes
                if service.health_check.http.tls is not None:
                    data['health_check']['http']['tls'] = service.health_check.http.tls
        return data

    def update_service(self, load_balancer, service):
        # type: (Union[LoadBalancer, BoundLoadBalancer], LoadBalancerService) -> List[BoundAction]
        """Updates a service of an Load Balancer.

        :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param service: :class:`LoadBalancerService <hcloud.load_balancers.domain.LoadBalancerService>`
                       The LoadBalancerService with updated values within for the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = self.get_service_parameters(service)
        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/update_service".format(
                load_balancer_id=load_balancer.id),
            method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def delete_service(self, load_balancer, service):
        # type: (Union[LoadBalancer, BoundLoadBalancer], LoadBalancerService) -> List[BoundAction]
        """Deletes a service from a Load Balancer.

        :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param service: :class:`LoadBalancerService <hcloud.load_balancers.domain.LoadBalancerService>`
                       The LoadBalancerService you want to delete from the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "listen_port": service.listen_port,
        }

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/delete_service".format(load_balancer_id=load_balancer.id),
            method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def add_target(self, load_balancer, target):
        # type: (Union[LoadBalancer, BoundLoadBalancer], LoadBalancerTarget) -> List[BoundAction]
        """Adds a target to a Load Balancer.

        :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param target: :class:`LoadBalancerTarget <hcloud.load_balancers.domain.LoadBalancerTarget>`
                       The LoadBalancerTarget you want to add to the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "type": target.type,
            "server": {"id": target.server.id},
            "use_private_ip": target.use_private_ip
        }

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/add_target".format(load_balancer_id=load_balancer.id),
            method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def remove_target(self, load_balancer, target):
        # type: (Union[LoadBalancer, BoundLoadBalancer], LoadBalancerTarget) -> List[BoundAction]
        """Removes a target from a Load Balancer.

        :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param target: :class:`LoadBalancerTarget <hcloud.load_balancers.domain.LoadBalancerTarget>`
                       The LoadBalancerTarget you want to remove from the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "type": target.type,
            "server": {"id": target.server.id},
        }

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/remove_target".format(load_balancer_id=load_balancer.id),
            method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def change_algorithm(self, load_balancer, algorithm):
        # type: (Union[LoadBalancer, BoundLoadBalancer], Optional[bool]) -> BoundAction
        """Changes the algorithm used by the Load Balancer

        :param load_balancer: :class:` <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param algorithm: :class:`LoadBalancerAlgorithm <hcloud.load_balancers.domain.LoadBalancerAlgorithm>`
                       The LoadBalancerSubnet you want to add to the Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {"type": algorithm.type}

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/change_algorithm".format(load_balancer_id=load_balancer.id),
            method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def change_protection(self, load_balancer, delete=None):
        # type: (Union[LoadBalancer, BoundLoadBalancer], Optional[bool]) -> BoundAction
        """Changes the protection configuration of a Load Balancer.

        :param load_balancer: :class:` <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param delete: boolean
               If True, prevents the Load Balancer from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/change_protection".format(
                load_balancer_id=load_balancer.id),
            method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def attach_to_network(self,
                          load_balancer,  # type: Union[LoadBalancer, BoundLoadBalancer]
                          network,  # type: Union[Network, BoundNetwork]
                          ip=None  # type: Optional[str]
                          ):
        """Attach a Load Balancer to a Network.

        :param load_balancer: :class:` <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param ip: str
                IP to request to be assigned to this Load Balancer
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {"network": network.id}
        if ip is not None:
            data.update({"ip": ip})

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/attach_to_network".format(
                load_balancer_id=load_balancer.id),
            method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def detach_from_network(self, load_balancer, network):
        # type: (Union[LoadBalancer, BoundLoadBalancer], Union[Network,BoundNetwork]) -> BoundAction
        """Detaches a Load Balancer from a Network.

        :param load_balancer: :class:` <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`
        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "network": network.id,
        }
        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/detach_from_network".format(
                load_balancer_id=load_balancer.id), method="POST",
            json=data)
        return BoundAction(self._client.actions, response['action'])

    def enable_public_interface(self, load_balancer):
        # type: (Union[LoadBalancer, BoundLoadBalancer]) -> BoundAction
        """ Enables the public interface of a Load Balancer.

        :param load_balancer: :class:` <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/enable_public_interface".format(
                load_balancer_id=load_balancer.id),
            method="POST")
        return BoundAction(self._client.actions, response['action'])

    def disable_public_interface(self, load_balancer):
        # type: (Union[LoadBalancer, BoundLoadBalancer]) -> BoundAction
        """ Disables the public interface of a Load Balancer.

        :param load_balancer: :class:` <hcloud.load_balancers.client.BoundLoadBalancer>` or :class:`LoadBalancer <hcloud.load_balancers.domain.LoadBalancer>`

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """

        response = self._client.request(
            url="/load_balancers/{load_balancer_id}/actions/disable_public_interface".format(
                load_balancer_id=load_balancer.id),
            method="POST")
        return BoundAction(self._client.actions, response['action'])

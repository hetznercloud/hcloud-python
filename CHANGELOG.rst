=======
History
=======

v1.9.1 (2020-08-11)
--------------------

* Bugfix: BoundLoadBalancer serialization failed when using IP targets

v1.9.0 (2020-08-10)
--------------------

* Feature: Add `included_traffic`, `outgoing_traffic` and `ingoing_traffic` properties to Load Balancer domain
* Feature: Add `change_type`-method to `LoadBalancersClient`
* Feature: Add support for `LoadBalancerTargetLabelSelector`
* Feature: Add support for `LoadBalancerTargetLabelSelector`

v1.8.2 (2020-07-20)
--------------------

* Fix: Loosen up the requirements.


v1.8.1 (2020-06-29)
--------------------

* Fix Load Balancer Client.
* Fix: Unify setting of request parameters within `get_list` methods.

1.8.0 (2020-06-22)
--------------------

* Feature: Add Load Balancers **Attention: The Load Balancer support in v1.8.0 is kind of broken. Please use v1.8.1**
* Feature: Add Certificates


1.7.1 (2020-06-15)
--------------------

* Feature: Add requests 2.23 support

1.7.0 (2020-06-05)
--------------------

* Feature: Add support for the optional 'networks' parameter on server creation.
* Feature: Add python 3.9 support
* Feature: Add subnet type `cloud`

1.6.3 (2020-01-09)
--------------------

* Feature: Add 'created' property to SSH Key domain
* Fix: Remove ISODatetime Descriptor because it leads to wrong dates

1.6.2 (2019-10-15)
-------------------
* Fix: future dependency requirement was too strict

1.6.1 (2019-10-01)
-------------------
* Fix: python-dateutil dependency requirement was too strict

1.6.0 (2019-09-17)
-------------------

* Feature: Add missing `get_by_name` on `FloatingIPsClient`

1.5.0 (2019-09-16)
-------------------

* Fix: ServersClient.create_image fails when specifying the `labels`
* Feature: Add support for `name` on Floating IPs

1.4.1 (2019-08-19)
------------------

* Fix: Documentation for `NetworkRoute` domain was missing

* Fix: `requests` dependency requirement was to strict

1.4.0 (2019-07-29)
------------------

* Feature: Add `mac_address` to Server PrivateNet domain

* Feature: Add python 3.8 support

1.3.0 (2019-07-10)
------------------

* Feature: Add status filter for servers, images and volumes
* Feature: Add 'created' property to Floating IP domain
* Feature: Add 'Networks' support

1.2.1 (2019-03-13)
------------------

* Fix: BoundVolume.server server property now casted to the 'BoundServer'.

1.2.0 (2019-03-06)
------------------

* Feature: Add `get_by_fingerprint`-method for ssh keys
* Fix: Create Floating IP with location raises an error because no action was given.

1.1.0 (2019-02-27)
------------------

* Feature: Add `STATUS`-constants for server and volume status

1.0.1 (2019-02-22)
------------------

  Fix: Ignore unknown fields in API response instead of raising an error

1.0.0 (2019-02-21)
------------------

* First stable release.
  
  You can find the documentation under https://hcloud-python.readthedocs.io/en/latest/

0.1.0 (2018-12-20)
------------------

* First release on GitHub.

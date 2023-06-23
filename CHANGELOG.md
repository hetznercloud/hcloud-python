# Changelog

## [1.22.0](https://github.com/hetznercloud/hcloud-python/compare/v1.21.0...v1.22.0) (2023-06-22)


### Features

* adhere to PEP 517 ([#213](https://github.com/hetznercloud/hcloud-python/issues/213)) ([7a19add](https://github.com/hetznercloud/hcloud-python/commit/7a19addd8b5200f8e61360657964233e7bfae13d))
* bump required python version to &gt;=3.7 ([#198](https://github.com/hetznercloud/hcloud-python/issues/198)) ([62d89f9](https://github.com/hetznercloud/hcloud-python/commit/62d89f94a8a86babd8ab238443054ca4cd9411ef))
* **network:** add field expose_routes_to_vswitch ([#208](https://github.com/hetznercloud/hcloud-python/issues/208)) ([5321182](https://github.com/hetznercloud/hcloud-python/commit/5321182d084d03484431c8ad27da12875d255768))
* setup exception hierarchy ([#199](https://github.com/hetznercloud/hcloud-python/issues/199)) ([8466645](https://github.com/hetznercloud/hcloud-python/commit/846664576a126472289464c0345eb9108c5f46d4))


### Dependencies

* update actions/setup-python action to v4 ([#209](https://github.com/hetznercloud/hcloud-python/issues/209)) ([aeee575](https://github.com/hetznercloud/hcloud-python/commit/aeee575a8ea7c4a1afe312a2cc2624ee564a1408))
* update actions/stale action to v8 ([#210](https://github.com/hetznercloud/hcloud-python/issues/210)) ([cb13230](https://github.com/hetznercloud/hcloud-python/commit/cb13230e570acdbb0287c678b4cee52a0a08a170))
* update pre-commit hook asottile/pyupgrade to v3.7.0 ([#205](https://github.com/hetznercloud/hcloud-python/issues/205)) ([c46c5a4](https://github.com/hetznercloud/hcloud-python/commit/c46c5a49fcc127a21c73e958aa074ff37a2b9664))

## [1.21.0](https://github.com/hetznercloud/hcloud-python/compare/v1.20.0...v1.21.0) (2023-06-19)


### Features

* add deprecation field to ServerType ([#192](https://github.com/hetznercloud/hcloud-python/issues/192)) ([4a0fce7](https://github.com/hetznercloud/hcloud-python/commit/4a0fce7da6d47a7e9094c5efd1769d3d9395b540))


### Bug Fixes

* adjust label validation for max length of 63 characters ([#194](https://github.com/hetznercloud/hcloud-python/issues/194)) ([3cba96d](https://github.com/hetznercloud/hcloud-python/commit/3cba96d261499e5f812aca7936ae9ed1e75ccd52))


### Documentation

* improve branding, design & fix warnings ([#191](https://github.com/hetznercloud/hcloud-python/issues/191)) ([47eb9f1](https://github.com/hetznercloud/hcloud-python/commit/47eb9f1c79e05a61084f0a639f9497beb22d6910))
* use venv for the dev setup ([#196](https://github.com/hetznercloud/hcloud-python/issues/196)) ([93f48ff](https://github.com/hetznercloud/hcloud-python/commit/93f48ff27c0561f66e5fe871e42fc2953bab0993))

## [1.20.0](https://github.com/hetznercloud/hcloud-python/compare/v1.19.0...v1.20.0) (2023-05-12)


### Features

 * **server_type:** add field for included traffic ([#185](https://github.com/hetznercloud/hcloud-python/issues/185)) ([8ae0bc6](https://github.com/hetznercloud/hcloud-python/commit/8ae0bc6e032440538f3aeb2222a9bee34adab04b))


## v1.19.0 (2023-04-12)

- docs: link to PrivateNet broken by @apricote in [#177](https://github.com/hetznercloud/hcloud-python/issues/177)
- feat: add support for ARM APIs by @apricote in [#182](https://github.com/hetznercloud/hcloud-python/issues/182)

## v1.18.2 (2022-12-27)

- fix: remove unused future dependency by @apricote in [#173](https://github.com/hetznercloud/hcloud-python/issues/173)
- chore: update tests to use released python-3.11 by @apricote in [#175](https://github.com/hetznercloud/hcloud-python/issues/175)
- chore: prepare release 1.18.2 by @apricote in [#174](https://github.com/hetznercloud/hcloud-python/issues/174)

## v1.18.1 (2022-10-25)

- Update Github Actions by @LKaemmerling in [#165](https://github.com/hetznercloud/hcloud-python/issues/165)
- Add tests for Python 3.11 by @LKaemmerling in [#167](https://github.com/hetznercloud/hcloud-python/issues/167)

## v1.18.0 (2022-08-17)

- Remove use of external mock module by @s-t-e-v-e-n-k in [#162](https://github.com/hetznercloud/hcloud-python/issues/162)
- document installation path via conda-forge by @s-m-e in [#149](https://github.com/hetznercloud/hcloud-python/issues/149)
- Drop # -- coding: utf-8 -- from files by @jonasdlindner in [#154](https://github.com/hetznercloud/hcloud-python/issues/154)
- Simplify Requirement Constraints by @LKaemmerling in [#163](https://github.com/hetznercloud/hcloud-python/issues/163)
- Add validation helper for Label Values/Keys by @LKaemmerling in [#164](https://github.com/hetznercloud/hcloud-python/issues/164)

## v1.17.0 (2022-06-29)

- Add primary IP support by @LKaemmerling in [#160](https://github.com/hetznercloud/hcloud-python/issues/160)

## v1.16.0 (2021-08-17)

- Feature: Add support for Load Balancer DNS PTRs

## v1.15.0 (2021-08-16)

- Feature: Add support for Placement Groups

## v1.14.1 (2021-08-10)

- Bugfix: Fix crash on extra fields in public_net response
- Improvement: Format code with black

## v1.14.0 (2021-08-03)

- Feature: Add support for Firewall rule descriptions

## v1.13.0 (2021-07-16)

- Feature: Add support for Firewall Protocols ESP and GRE
- Feature: Add support for Image Type APP
- Feature: Add support for creating Firewalls with Firewalls
- Feature: Add support for Label Selectors in Firewalls
- Improvement: Improve handling of underlying TCP connections. Now for every client instance a single TCP connection is used instead of one per call.

- Note: Support for Python 2.7 and Python 3.5 was removed

## v1.12.0 (2021-04-06)

- Feature: Add support for managed Certificates

## v1.11.0 (2021-03-11)

- Feature: Add support for Firewalls
- Feature: Add `primary_disk_size` to `Server` Domain

## v1.10.0 (2020-11-03)

- Feature: Add `include_deprecated` filter to `get_list` and `get_all` on `ImagesClient`
- Feature: Add vSwitch support to `add_subnet` on `NetworksClient`
- Feature: Add subnet type constants to `NetworkSubnet` domain (`NetworkSubnet.TYPE_CLOUD`, `NetworkSubnet.TYPE_VSWITCH`)

## v1.9.1 (2020-08-11)

- Bugfix: BoundLoadBalancer serialization failed when using IP targets

## v1.9.0 (2020-08-10)

- Feature: Add `included_traffic`, `outgoing_traffic` and `ingoing_traffic` properties to Load Balancer domain
- Feature: Add `change_type`-method to `LoadBalancersClient`
- Feature: Add support for `LoadBalancerTargetLabelSelector`
- Feature: Add support for `LoadBalancerTargetLabelSelector`

## v1.8.2 (2020-07-20)

- Fix: Loosen up the requirements.

## v1.8.1 (2020-06-29)

- Fix Load Balancer Client.
- Fix: Unify setting of request parameters within `get_list` methods.

## 1.8.0 (2020-06-22)

- Feature: Add Load Balancers **Attention: The Load Balancer support in v1.8.0 is kind of broken. Please use v1.8.1**
- Feature: Add Certificates

## 1.7.1 (2020-06-15)

- Feature: Add requests 2.23 support

## 1.7.0 (2020-06-05)

- Feature: Add support for the optional 'networks' parameter on server creation.
- Feature: Add python 3.9 support
- Feature: Add subnet type `cloud`

## 1.6.3 (2020-01-09)

- Feature: Add 'created' property to SSH Key domain
- Fix: Remove ISODatetime Descriptor because it leads to wrong dates

## 1.6.2 (2019-10-15)

- Fix: future dependency requirement was too strict

## 1.6.1 (2019-10-01)

- Fix: python-dateutil dependency requirement was too strict

## 1.6.0 (2019-09-17)

- Feature: Add missing `get_by_name` on `FloatingIPsClient`

## 1.5.0 (2019-09-16)

- Fix: ServersClient.create_image fails when specifying the `labels`
- Feature: Add support for `name` on Floating IPs

## 1.4.1 (2019-08-19)

- Fix: Documentation for `NetworkRoute` domain was missing

- Fix: `requests` dependency requirement was to strict

## 1.4.0 (2019-07-29)

- Feature: Add `mac_address` to Server PrivateNet domain

- Feature: Add python 3.8 support

## 1.3.0 (2019-07-10)

- Feature: Add status filter for servers, images and volumes
- Feature: Add 'created' property to Floating IP domain
- Feature: Add 'Networks' support

## 1.2.1 (2019-03-13)

- Fix: BoundVolume.server server property now casted to the 'BoundServer'.

## 1.2.0 (2019-03-06)

- Feature: Add `get_by_fingerprint`-method for ssh keys
- Fix: Create Floating IP with location raises an error because no action was given.

## 1.1.0 (2019-02-27)

- Feature: Add `STATUS`-constants for server and volume status

## 1.0.1 (2019-02-22)

Fix: Ignore unknown fields in API response instead of raising an error

## 1.0.0 (2019-02-21)

- First stable release.

  You can find the documentation under https://hcloud-python.readthedocs.io/en/latest/

## 0.1.0 (2018-12-20)

- First release on GitHub.

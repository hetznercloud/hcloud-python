# Changelog

## [2.1.1](https://github.com/hetznercloud/hcloud-python/compare/v2.1.0...v2.1.1) (2024-07-30)


### Bug Fixes

* do not sleep before checking for the reloaded action status ([#426](https://github.com/hetznercloud/hcloud-python/issues/426)) ([3e0a85b](https://github.com/hetznercloud/hcloud-python/commit/3e0a85b487fc15941008e4d610243de3cb0396cb))
* mark client retry backoff function as static ([#429](https://github.com/hetznercloud/hcloud-python/issues/429)) ([14ed130](https://github.com/hetznercloud/hcloud-python/commit/14ed130e989c68eacce2634c7983b200570de9c2))


### Documentation

* add api changes note in changelog ([#424](https://github.com/hetznercloud/hcloud-python/issues/424)) ([5cbe188](https://github.com/hetznercloud/hcloud-python/commit/5cbe1889a21c686588d91ab90306d345ba5b84dd))

## [2.1.0](https://github.com/hetznercloud/hcloud-python/compare/v2.0.1...v2.1.0) (2024-07-25)

### API Changes for Traffic Prices and Server Type Included Traffic

There will be a breaking change in the API regarding Traffic Prices and Server Type Included Traffic on 2024-08-05. This release marks the affected fields as `Deprecated`. Please check if this affects any of your code and switch to the replacement fields where necessary.

You can learn more about this change in [our changelog](https://docs.hetzner.cloud/changelog#2024-07-25-cloud-api-returns-traffic-information-in-different-format).

### Features

* add exponential and constant backoff function ([#416](https://github.com/hetznercloud/hcloud-python/issues/416)) ([fe7ddf6](https://github.com/hetznercloud/hcloud-python/commit/fe7ddf6da78f8dbbc395eb98ff1200b8117f0cc0))
* deprecate `ServerType` `included_traffic` property ([#423](https://github.com/hetznercloud/hcloud-python/issues/423)) ([3d56ac5](https://github.com/hetznercloud/hcloud-python/commit/3d56ac57d092bb30543fac9249c04393d0864c3b))
* use exponential backoff when retrying requests ([#417](https://github.com/hetznercloud/hcloud-python/issues/417)) ([f306073](https://github.com/hetznercloud/hcloud-python/commit/f3060737d0e2991a0abf69e4953a3967ac8f84ed))

## [2.0.1](https://github.com/hetznercloud/hcloud-python/compare/v2.0.0...v2.0.1) (2024-07-03)


### Bug Fixes

* `assignee_type` is required when creating a primary ip ([#409](https://github.com/hetznercloud/hcloud-python/issues/409)) ([bce5e94](https://github.com/hetznercloud/hcloud-python/commit/bce5e940e27f2c6d9d50016b5828c79aadfc4401))
* clean unused arguments in the `Client.servers.rebuild` method ([#407](https://github.com/hetznercloud/hcloud-python/issues/407)) ([6d33c3c](https://github.com/hetznercloud/hcloud-python/commit/6d33c3cff5443686c7ed37eb8635e0461bb3b928))
* details are optional in API errors ([#411](https://github.com/hetznercloud/hcloud-python/issues/411)) ([f1c6594](https://github.com/hetznercloud/hcloud-python/commit/f1c6594dee7088872f2375359ee259e4e93b31d2))
* rename `trace_id` variable to `correlation_id`  ([#408](https://github.com/hetznercloud/hcloud-python/issues/408)) ([66a0f54](https://github.com/hetznercloud/hcloud-python/commit/66a0f546998193f9078f70a4a2fb1fc11937c086))

## [2.0.0](https://github.com/hetznercloud/hcloud-python/compare/v1.35.0...v2.0.0) (2024-07-03)


### ⚠ BREAKING CHANGES

* return full rebuild response in `Client.servers.rebuild` ([#406](https://github.com/hetznercloud/hcloud-python/issues/406))
* make `datacenter` argument optional when creating a primary ip ([#363](https://github.com/hetznercloud/hcloud-python/issues/363))
* remove deprecated `include_wildcard_architecture` argument in `IsosClient.get_list` and `IsosClient.get_all` ([#402](https://github.com/hetznercloud/hcloud-python/issues/402))
* make `Client.request` `tries` a private argument ([#399](https://github.com/hetznercloud/hcloud-python/issues/399))
* make `Client.poll_interval` a private property ([#398](https://github.com/hetznercloud/hcloud-python/issues/398))
* return empty dict on empty responses in `Client.request` ([#400](https://github.com/hetznercloud/hcloud-python/issues/400))
* remove deprecated `hcloud.hcloud` module ([#401](https://github.com/hetznercloud/hcloud-python/issues/401))
* move `hcloud.__version__.VERSION` to `hcloud.__version__` ([#397](https://github.com/hetznercloud/hcloud-python/issues/397))

### Features

* add `trace_id` to API exceptions ([#404](https://github.com/hetznercloud/hcloud-python/issues/404)) ([8375261](https://github.com/hetznercloud/hcloud-python/commit/8375261da3b84d6fece97263c7bea40ad2a6cfcf))
* allow using a custom poll_interval function ([#403](https://github.com/hetznercloud/hcloud-python/issues/403)) ([93eb56b](https://github.com/hetznercloud/hcloud-python/commit/93eb56ba4d1a69e175398bca42e723a7e8e46371))
* make `Client.poll_interval` a private property ([#398](https://github.com/hetznercloud/hcloud-python/issues/398)) ([d5f24db](https://github.com/hetznercloud/hcloud-python/commit/d5f24db2816a0d00b8c7936e2a0290d2c4bb1e92))
* make `Client.request` `tries` a private argument ([#399](https://github.com/hetznercloud/hcloud-python/issues/399)) ([428ea7e](https://github.com/hetznercloud/hcloud-python/commit/428ea7e3be03a16114f875146971db59aabaac2c))
* move `hcloud.__version__.VERSION` to `hcloud.__version__` ([#397](https://github.com/hetznercloud/hcloud-python/issues/397)) ([4e3f638](https://github.com/hetznercloud/hcloud-python/commit/4e3f638862c9d260df98182c3f7858282049c26c)), closes [#234](https://github.com/hetznercloud/hcloud-python/issues/234)
* remove deprecated `hcloud.hcloud` module ([#401](https://github.com/hetznercloud/hcloud-python/issues/401)) ([db37e63](https://github.com/hetznercloud/hcloud-python/commit/db37e633ebbf73354d3b2f4858cf3eebf173bfbc))
* remove deprecated `include_wildcard_architecture` argument in `IsosClient.get_list` and `IsosClient.get_all` ([#402](https://github.com/hetznercloud/hcloud-python/issues/402)) ([6b977e2](https://github.com/hetznercloud/hcloud-python/commit/6b977e2da5cec30110c32a91d572003e5b5c400a))
* return empty dict on empty responses in `Client.request` ([#400](https://github.com/hetznercloud/hcloud-python/issues/400)) ([9f46adb](https://github.com/hetznercloud/hcloud-python/commit/9f46adb946eb2770ee4f3a4e87cfc1c8b9b33c28))
* return full rebuild response in `Client.servers.rebuild` ([#406](https://github.com/hetznercloud/hcloud-python/issues/406)) ([1970d84](https://github.com/hetznercloud/hcloud-python/commit/1970d84bec2106c8c53d8e611b74d41eb5286e9b))


### Bug Fixes

* make `datacenter` argument optional when creating a primary ip ([#363](https://github.com/hetznercloud/hcloud-python/issues/363)) ([ebef774](https://github.com/hetznercloud/hcloud-python/commit/ebef77464c4c3b0ce33460cad2747e89d35047c7))


### Dependencies

* update dependency coverage to &gt;=7.5,&lt;7.6 ([#386](https://github.com/hetznercloud/hcloud-python/issues/386)) ([5660691](https://github.com/hetznercloud/hcloud-python/commit/5660691ebd6122fa7ebec56a24bce9fce0577573))
* update dependency mypy to &gt;=1.10,&lt;1.11 ([#387](https://github.com/hetznercloud/hcloud-python/issues/387)) ([35c933b](https://github.com/hetznercloud/hcloud-python/commit/35c933bd2108d42e74b74b01d6db74e159ec9142))
* update dependency myst-parser to v3 ([#385](https://github.com/hetznercloud/hcloud-python/issues/385)) ([9f18270](https://github.com/hetznercloud/hcloud-python/commit/9f182704898cb96f1ea162511605906f87cff50c))
* update dependency pylint to &gt;=3,&lt;3.3 ([#391](https://github.com/hetznercloud/hcloud-python/issues/391)) ([4a6f005](https://github.com/hetznercloud/hcloud-python/commit/4a6f005cb0488291ae91390a612bab6afc6d80b6))
* update dependency pytest to &gt;=8,&lt;8.3 ([#390](https://github.com/hetznercloud/hcloud-python/issues/390)) ([584a36b](https://github.com/hetznercloud/hcloud-python/commit/584a36b658670297ffffa9afa70835d29d27fbca))
* update dependency sphinx to &gt;=7.3.4,&lt;7.4 ([#383](https://github.com/hetznercloud/hcloud-python/issues/383)) ([69c2e16](https://github.com/hetznercloud/hcloud-python/commit/69c2e16073df9ef8520e3a635b3866403eba030e))
* update pre-commit hook asottile/pyupgrade to v3.16.0 ([0ce5fbc](https://github.com/hetznercloud/hcloud-python/commit/0ce5fbccba4a4255e08a37abf1f21ab9cc85f287))
* update pre-commit hook pre-commit/pre-commit-hooks to v4.6.0 ([5ef25ab](https://github.com/hetznercloud/hcloud-python/commit/5ef25ab3966d731c4c36ea3e785c2b5f20c69489))
* update pre-commit hook psf/black-pre-commit-mirror to v24.4.0 ([0941fbf](https://github.com/hetznercloud/hcloud-python/commit/0941fbfab20ca8a59e768c4a5e6fc101393c97f0))
* update pre-commit hook psf/black-pre-commit-mirror to v24.4.1 ([fec08c5](https://github.com/hetznercloud/hcloud-python/commit/fec08c5323359d0a4f0771123f483ff975aa68b0))
* update pre-commit hook psf/black-pre-commit-mirror to v24.4.2 ([#389](https://github.com/hetznercloud/hcloud-python/issues/389)) ([2b2e21f](https://github.com/hetznercloud/hcloud-python/commit/2b2e21f61366b5ec0f2ff5558f652d2bfed9d138))
* update pre-commit hook pycqa/flake8 to v7.1.0 ([3bc651d](https://github.com/hetznercloud/hcloud-python/commit/3bc651d50d85aa92ba76dbfeef1d604cabaa4628))


### Documentation

* add v2 upgrade notes ([#405](https://github.com/hetznercloud/hcloud-python/issues/405)) ([c77f771](https://github.com/hetznercloud/hcloud-python/commit/c77f771e2bed176acd6aa5011be006c800181809))
* cx11 is name, not an id ([#381](https://github.com/hetznercloud/hcloud-python/issues/381)) ([b745d40](https://github.com/hetznercloud/hcloud-python/commit/b745d4049f720b93d840a9204a99d246ecb499e5))

## [1.35.0](https://github.com/hetznercloud/hcloud-python/compare/v1.34.0...v1.35.0) (2024-04-02)


### Features

* add `include_deprecated` option when fetching images by name ([#375](https://github.com/hetznercloud/hcloud-python/issues/375)) ([6d86f86](https://github.com/hetznercloud/hcloud-python/commit/6d86f86677fec23e6fd8a69d20d787e234e0fb53))


### Bug Fixes

* raise warnings for the `ImagesClient.get_by_name` deprecation ([#376](https://github.com/hetznercloud/hcloud-python/issues/376)) ([b24de80](https://github.com/hetznercloud/hcloud-python/commit/b24de80684db142ebbe11b62a38d9c61f248e216))

## [1.34.0](https://github.com/hetznercloud/hcloud-python/compare/v1.33.3...v1.34.0) (2024-03-27)


### Features

* add `has_id_or_name` to `DomainIdentityMixin` ([#373](https://github.com/hetznercloud/hcloud-python/issues/373)) ([8facaf6](https://github.com/hetznercloud/hcloud-python/commit/8facaf6d4dd2bbfb4137e7066b49c5f4c1db773c))

## [1.33.3](https://github.com/hetznercloud/hcloud-python/compare/v1.33.2...v1.33.3) (2024-03-27)


### Bug Fixes

* invalid type for load balancer private network property ([#372](https://github.com/hetznercloud/hcloud-python/issues/372)) ([903e92f](https://github.com/hetznercloud/hcloud-python/commit/903e92faab745b7f8270f6195da67f4d9f8b1ba7))


### Dependencies

* update codecov/codecov-action action to v4 ([#359](https://github.com/hetznercloud/hcloud-python/issues/359)) ([a798979](https://github.com/hetznercloud/hcloud-python/commit/a79897977abe970181d19584e51448ff5976b5e2))
* update dependency mypy to &gt;=1.9,&lt;1.10 ([#368](https://github.com/hetznercloud/hcloud-python/issues/368)) ([4b9328c](https://github.com/hetznercloud/hcloud-python/commit/4b9328ceae1e393ff55b3ca6f030cb5ac565be00))
* update dependency pylint to &gt;=3,&lt;3.2 ([#364](https://github.com/hetznercloud/hcloud-python/issues/364)) ([d71d17f](https://github.com/hetznercloud/hcloud-python/commit/d71d17fd6f2968a8c19052753265ef7f514a8955))
* update dependency pytest to &gt;=8,&lt;8.2 ([#366](https://github.com/hetznercloud/hcloud-python/issues/366)) ([8665dcf](https://github.com/hetznercloud/hcloud-python/commit/8665dcff335c755c1ff4d95621334a3f5e196d34))
* update dependency pytest to v8 ([#357](https://github.com/hetznercloud/hcloud-python/issues/357)) ([f8f756f](https://github.com/hetznercloud/hcloud-python/commit/f8f756fe0a492e284bd2a700514c0ba38358b4a8))
* update dependency pytest-cov to v5 ([#371](https://github.com/hetznercloud/hcloud-python/issues/371)) ([04a6a42](https://github.com/hetznercloud/hcloud-python/commit/04a6a42028606ed66657605d98b1f21545eb2e0d))
* update dependency watchdog to v4 ([#360](https://github.com/hetznercloud/hcloud-python/issues/360)) ([cb8d383](https://github.com/hetznercloud/hcloud-python/commit/cb8d38396a8665506e3be64a09450343d7671586))
* update pre-commit hook asottile/pyupgrade to v3.15.1 ([#362](https://github.com/hetznercloud/hcloud-python/issues/362)) ([dd2a521](https://github.com/hetznercloud/hcloud-python/commit/dd2a521eccec8e15b6d1d7fd843d866bf6ea5bcf))
* update pre-commit hook asottile/pyupgrade to v3.15.2 ([3d02ad7](https://github.com/hetznercloud/hcloud-python/commit/3d02ad71e9200f5cc94b2d33eea62035edc1e33a))
* update pre-commit hook psf/black-pre-commit-mirror to v24 ([#356](https://github.com/hetznercloud/hcloud-python/issues/356)) ([b46397d](https://github.com/hetznercloud/hcloud-python/commit/b46397d761caa60014bd32f7142b79bef9a92e18))
* update pre-commit hook psf/black-pre-commit-mirror to v24.1.1 ([#358](https://github.com/hetznercloud/hcloud-python/issues/358)) ([7e4645e](https://github.com/hetznercloud/hcloud-python/commit/7e4645e3e38a106f38a7f63810d71a628fead939))
* update pre-commit hook psf/black-pre-commit-mirror to v24.2.0 ([#361](https://github.com/hetznercloud/hcloud-python/issues/361)) ([5b56ace](https://github.com/hetznercloud/hcloud-python/commit/5b56ace93b8b4fddddbf5610c11fd20bf6f9a561))
* update pre-commit hook psf/black-pre-commit-mirror to v24.3.0 ([3bbac5d](https://github.com/hetznercloud/hcloud-python/commit/3bbac5dc41ca509d6679fd6b06ae99ca33fd62ee))
* update pre-commit hook pycqa/flake8 to v7 ([#354](https://github.com/hetznercloud/hcloud-python/issues/354)) ([66a582f](https://github.com/hetznercloud/hcloud-python/commit/66a582f3ce728d92045625885d0634fc96fbc6a0))
* update pypa/gh-action-pypi-publish action to v1.8.12 ([#365](https://github.com/hetznercloud/hcloud-python/issues/365)) ([55db255](https://github.com/hetznercloud/hcloud-python/commit/55db2551dd0f0ea6a29da4e7a6dce2af8de86eaf))
* update pypa/gh-action-pypi-publish action to v1.8.14 ([#367](https://github.com/hetznercloud/hcloud-python/issues/367)) ([0cb615f](https://github.com/hetznercloud/hcloud-python/commit/0cb615fe0d852cddbf636c1fdb8538ad60f5a3d9))

## [1.33.2](https://github.com/hetznercloud/hcloud-python/compare/v1.33.1...v1.33.2) (2024-01-02)


### Bug Fixes

* publish package to PyPI using OIDC auth ([1a0e93b](https://github.com/hetznercloud/hcloud-python/commit/1a0e93bbf1ae6cc747e6c4d8305dafd3e49dbbdc))

## [1.33.1](https://github.com/hetznercloud/hcloud-python/compare/v1.33.0...v1.33.1) (2024-01-02)


### Bug Fixes

* private object not exported in top level module ([#346](https://github.com/hetznercloud/hcloud-python/issues/346)) ([5281b05](https://github.com/hetznercloud/hcloud-python/commit/5281b0583541b6e0e9b8c7ad75faa42c5d379735))


### Dependencies

* update dependency coverage to &gt;=7.4,&lt;7.5 ([#348](https://github.com/hetznercloud/hcloud-python/issues/348)) ([3ac5711](https://github.com/hetznercloud/hcloud-python/commit/3ac57117e8a68a02cba19c56f850f037c4aca462))
* update dependency mypy to &gt;=1.8,&lt;1.9 ([#343](https://github.com/hetznercloud/hcloud-python/issues/343)) ([984022f](https://github.com/hetznercloud/hcloud-python/commit/984022fd3888ef856be83de82554d55a8af18dba))
* update pre-commit hook psf/black-pre-commit-mirror to v23.12.1 ([#347](https://github.com/hetznercloud/hcloud-python/issues/347)) ([2c24efe](https://github.com/hetznercloud/hcloud-python/commit/2c24efe93bc221846f8dcc91abcf1aad61547875))

## [1.33.0](https://github.com/hetznercloud/hcloud-python/compare/v1.32.0...v1.33.0) (2023-12-19)


### Features

* add metrics endpoint for load balancers and servers ([#331](https://github.com/hetznercloud/hcloud-python/issues/331)) ([ee3c54f](https://github.com/hetznercloud/hcloud-python/commit/ee3c54fd1b6963533bc9d1e1f9ff57f6c5872cd5))


### Bug Fixes

* fallback to error code when message is unset ([#328](https://github.com/hetznercloud/hcloud-python/issues/328)) ([1c94153](https://github.com/hetznercloud/hcloud-python/commit/1c94153d93acd567548604b08b5fabeabd8d33d9))


### Dependencies

* update actions/setup-python action to v5 ([#335](https://github.com/hetznercloud/hcloud-python/issues/335)) ([2ac252d](https://github.com/hetznercloud/hcloud-python/commit/2ac252d18ba6079d5372c6ab9e3f67b4740db465))
* update dependency sphinx-rtd-theme to v2 ([#330](https://github.com/hetznercloud/hcloud-python/issues/330)) ([7cc4335](https://github.com/hetznercloud/hcloud-python/commit/7cc4335cacab6073cf39a0ecbecf8890903d5bca))
* update pre-commit hook psf/black-pre-commit-mirror to v23.12.0 ([#338](https://github.com/hetznercloud/hcloud-python/issues/338)) ([38e4748](https://github.com/hetznercloud/hcloud-python/commit/38e4748d3d194d37ea3d0c63683609f5db432e0d))
* update pre-commit hook pycqa/isort to v5.13.0 ([#336](https://github.com/hetznercloud/hcloud-python/issues/336)) ([3244cfe](https://github.com/hetznercloud/hcloud-python/commit/3244cfef2f90ef52d0fb791d514d6afe481aa4d7))
* update pre-commit hook pycqa/isort to v5.13.1 ([#337](https://github.com/hetznercloud/hcloud-python/issues/337)) ([020a0ef](https://github.com/hetznercloud/hcloud-python/commit/020a0eff6bc2b63d16b339fd5d4c3ea3610c0509))
* update pre-commit hook pycqa/isort to v5.13.2 ([#339](https://github.com/hetznercloud/hcloud-python/issues/339)) ([b46df8c](https://github.com/hetznercloud/hcloud-python/commit/b46df8cbb263945c59ce4408e0a7189d19d9c597))

## [1.32.0](https://github.com/hetznercloud/hcloud-python/compare/v1.31.0...v1.32.0) (2023-11-17)


### Features

* allow returning root_password in servers rebuild ([#276](https://github.com/hetznercloud/hcloud-python/issues/276)) ([38e098a](https://github.com/hetznercloud/hcloud-python/commit/38e098a41154e6561578cd723608fcd7577c3d01))


### Dependencies

* update dependency mypy to &gt;=1.7,&lt;1.8 ([#325](https://github.com/hetznercloud/hcloud-python/issues/325)) ([7b59a2d](https://github.com/hetznercloud/hcloud-python/commit/7b59a2decc9bb5152dc9de435bfe12ce1f34ac1c))
* update pre-commit hook pre-commit/mirrors-prettier to v3.1.0 ([#326](https://github.com/hetznercloud/hcloud-python/issues/326)) ([213b661](https://github.com/hetznercloud/hcloud-python/commit/213b661d897cdd327f478b52aeb79844826694d8))
* update pre-commit hook psf/black-pre-commit-mirror to v23.10.1 ([#322](https://github.com/hetznercloud/hcloud-python/issues/322)) ([999afe3](https://github.com/hetznercloud/hcloud-python/commit/999afe37e02a113639930aff6879f50918ac0e89))
* update pre-commit hook psf/black-pre-commit-mirror to v23.11.0 ([#324](https://github.com/hetznercloud/hcloud-python/issues/324)) ([7b2a24e](https://github.com/hetznercloud/hcloud-python/commit/7b2a24ecf69c0bead7f9113053fda37a0cc31d1b))

## [1.31.0](https://github.com/hetznercloud/hcloud-python/compare/v1.30.0...v1.31.0) (2023-10-23)


### Features

* prepare for iso deprecated field removal ([#320](https://github.com/hetznercloud/hcloud-python/issues/320)) ([beae328](https://github.com/hetznercloud/hcloud-python/commit/beae328dd6b9afb8c0db9fa9b44340270db7dd09))


### Dependencies

* update pre-commit hook psf/black-pre-commit-mirror to v23.10.0 ([#319](https://github.com/hetznercloud/hcloud-python/issues/319)) ([184bbe6](https://github.com/hetznercloud/hcloud-python/commit/184bbe65a736a42d13774b6c29fa7dd8a13ec645))

## [1.30.0](https://github.com/hetznercloud/hcloud-python/compare/v1.29.1...v1.30.0) (2023-10-13)


### Features

* add deprecation field to Iso ([#318](https://github.com/hetznercloud/hcloud-python/issues/318)) ([036b52f](https://github.com/hetznercloud/hcloud-python/commit/036b52fe51bcbb6b610c0c99ca224d3c4bbfc68d))
* support python 3.12 ([#311](https://github.com/hetznercloud/hcloud-python/issues/311)) ([7e8cd1d](https://github.com/hetznercloud/hcloud-python/commit/7e8cd1d92e56d210fe3fb180e403122ef0e7bd7f))


### Dependencies

* update dependency mypy to &gt;=1.6,&lt;1.7 ([#317](https://github.com/hetznercloud/hcloud-python/issues/317)) ([d248bbd](https://github.com/hetznercloud/hcloud-python/commit/d248bbd4e55f3bcf6a107cfa4f38768df0bf3de5))
* update dependency pylint to v3 ([#307](https://github.com/hetznercloud/hcloud-python/issues/307)) ([277841d](https://github.com/hetznercloud/hcloud-python/commit/277841dd84ba3b2bbc99a06a3f97e114d1c83dcb))
* update pre-commit hook asottile/pyupgrade to v3.14.0 ([#308](https://github.com/hetznercloud/hcloud-python/issues/308)) ([07a4513](https://github.com/hetznercloud/hcloud-python/commit/07a4513e284b9ee964bca003d0a9dfd948d39b02))
* update pre-commit hook asottile/pyupgrade to v3.15.0 ([#312](https://github.com/hetznercloud/hcloud-python/issues/312)) ([c544639](https://github.com/hetznercloud/hcloud-python/commit/c5446394acfa25d23761da4c6b5b75fb6d376b23))
* update pre-commit hook pre-commit/pre-commit-hooks to v4.5.0 ([#313](https://github.com/hetznercloud/hcloud-python/issues/313)) ([e51eaa9](https://github.com/hetznercloud/hcloud-python/commit/e51eaa990336251c2afc8c83d4c5e6f5e5bb857b))
* update python docker tag to v3.12 ([#309](https://github.com/hetznercloud/hcloud-python/issues/309)) ([3a1ee67](https://github.com/hetznercloud/hcloud-python/commit/3a1ee675f2c980a4d9e63188e8ffceb64f4797fc))

## [1.29.1](https://github.com/hetznercloud/hcloud-python/compare/v1.29.0...v1.29.1) (2023-09-26)


### Bug Fixes

* prevent api calls when printing bound models ([#305](https://github.com/hetznercloud/hcloud-python/issues/305)) ([c1de7ef](https://github.com/hetznercloud/hcloud-python/commit/c1de7efc851b3b10e2a50e66268fc8fb0ff648a8))

## [1.29.0](https://github.com/hetznercloud/hcloud-python/compare/v1.28.0...v1.29.0) (2023-09-25)


### Features

* add domain attribute type hints to bound models ([#300](https://github.com/hetznercloud/hcloud-python/issues/300)) ([6d46d06](https://github.com/hetznercloud/hcloud-python/commit/6d46d06c42e2e86e88b32a74d7fbd588911cc8ad))
* **firewalls:** add `applied_to_resources` to `FirewallResource` ([#297](https://github.com/hetznercloud/hcloud-python/issues/297)) ([55d2b20](https://github.com/hetznercloud/hcloud-python/commit/55d2b2043ec1e3a040eb9e360ca0dc0c299ad60f))


### Bug Fixes

* missing BaseDomain base class inheritance ([#303](https://github.com/hetznercloud/hcloud-python/issues/303)) ([0ee7598](https://github.com/hetznercloud/hcloud-python/commit/0ee759856cb1352f6cc538b7ef86a91cd20380f2))


### Dependencies

* update actions/checkout action to v4 ([#295](https://github.com/hetznercloud/hcloud-python/issues/295)) ([c02b446](https://github.com/hetznercloud/hcloud-python/commit/c02b4468f0e499791bbee8fe48fe7a737985df1f))
* update dependency sphinx to &gt;=7.2.2,&lt;7.3 ([#291](https://github.com/hetznercloud/hcloud-python/issues/291)) ([10234ea](https://github.com/hetznercloud/hcloud-python/commit/10234ea7bf51a427b18f2b5605d9ffa7ac5f5ee8))
* update dependency sphinx to v7 ([#211](https://github.com/hetznercloud/hcloud-python/issues/211)) ([f635c94](https://github.com/hetznercloud/hcloud-python/commit/f635c94c23b8ae49283b9b7fcb4fe7b948b203b9))
* update pre-commit hook asottile/pyupgrade to v3.11.0 ([#298](https://github.com/hetznercloud/hcloud-python/issues/298)) ([4bbd0cc](https://github.com/hetznercloud/hcloud-python/commit/4bbd0ccb0f606e2f90f8242951d3f4d9b86d7aea))
* update pre-commit hook asottile/pyupgrade to v3.11.1 ([#299](https://github.com/hetznercloud/hcloud-python/issues/299)) ([2f9fcd7](https://github.com/hetznercloud/hcloud-python/commit/2f9fcd7bb80efb8da6eafab0ee70a8dda93eb6f1))
* update pre-commit hook asottile/pyupgrade to v3.13.0 ([#301](https://github.com/hetznercloud/hcloud-python/issues/301)) ([951dbf3](https://github.com/hetznercloud/hcloud-python/commit/951dbf3e3b3816ffaeb44a583251a5a3a4b90b70))
* update pre-commit hook pre-commit/mirrors-prettier to v3.0.3 ([#294](https://github.com/hetznercloud/hcloud-python/issues/294)) ([381e336](https://github.com/hetznercloud/hcloud-python/commit/381e336ff1259fa26cb6abae3b7341cb16229a4b))
* update pre-commit hook psf/black to v23.9.1 ([#296](https://github.com/hetznercloud/hcloud-python/issues/296)) ([4374a7b](https://github.com/hetznercloud/hcloud-python/commit/4374a7be9f244a72f1fc0c2dd76357cf63f19bfd))


### Documentation

* load token from env in examples scripts ([#302](https://github.com/hetznercloud/hcloud-python/issues/302)) ([f18c9a6](https://github.com/hetznercloud/hcloud-python/commit/f18c9a60e045743b26892eeb1fe9e5737a63c11f))

## [1.28.0](https://github.com/hetznercloud/hcloud-python/compare/v1.27.2...v1.28.0) (2023-08-17)


### Features

* add load balancer target health status field ([#288](https://github.com/hetznercloud/hcloud-python/issues/288)) ([5780418](https://github.com/hetznercloud/hcloud-python/commit/5780418f00a42e20cccacec6e030e464105807ba))
* implement resource actions clients ([#252](https://github.com/hetznercloud/hcloud-python/issues/252)) ([4bb9a97](https://github.com/hetznercloud/hcloud-python/commit/4bb9a9730eadea9fd0569d5d11b7585dbb5da157))


### Dependencies

* update dependency coverage to &gt;=7.3,&lt;7.4 ([#286](https://github.com/hetznercloud/hcloud-python/issues/286)) ([a4df4fa](https://github.com/hetznercloud/hcloud-python/commit/a4df4fa1cc7a17e1afdea1c33f4428a8a594a011))
* update dependency mypy to &gt;=1.5,&lt;1.6 ([#284](https://github.com/hetznercloud/hcloud-python/issues/284)) ([9dd5c81](https://github.com/hetznercloud/hcloud-python/commit/9dd5c8110bf679c13e8e6ba08e760019b4dae706))
* update pre-commit hook pre-commit/mirrors-prettier to v3.0.2 ([#287](https://github.com/hetznercloud/hcloud-python/issues/287)) ([6bf03cb](https://github.com/hetznercloud/hcloud-python/commit/6bf03cb9ab1203f172e1634d28a99a7cb3210ad0))


### Documentation

* fail on warning ([#289](https://github.com/hetznercloud/hcloud-python/issues/289)) ([e61300e](https://github.com/hetznercloud/hcloud-python/commit/e61300eda7f0ba15e0a91cce3e4b8f7542ed42c8))

## [1.27.2](https://github.com/hetznercloud/hcloud-python/compare/v1.27.1...v1.27.2) (2023-08-09)


### Documentation

* fix python references ([#281](https://github.com/hetznercloud/hcloud-python/issues/281)) ([0c0518e](https://github.com/hetznercloud/hcloud-python/commit/0c0518e38e8c6ebe280ee85259480fb5671c2d84))

## [1.27.1](https://github.com/hetznercloud/hcloud-python/compare/v1.27.0...v1.27.1) (2023-08-08)


### Bug Fixes

* missing long_description content_type in setup.py ([#279](https://github.com/hetznercloud/hcloud-python/issues/279)) ([6d79d1d](https://github.com/hetznercloud/hcloud-python/commit/6d79d1d18d3731c3db70184c841428e9c4b2a32c))

## [1.27.0](https://github.com/hetznercloud/hcloud-python/compare/v1.26.0...v1.27.0) (2023-08-08)


### Features

* add global request timeout option ([#271](https://github.com/hetznercloud/hcloud-python/issues/271)) ([07a663f](https://github.com/hetznercloud/hcloud-python/commit/07a663fd8628d305a7461a90a94c61a97c12421b))
* reexport references in parent ressources modules ([#256](https://github.com/hetznercloud/hcloud-python/issues/256)) ([854c12b](https://github.com/hetznercloud/hcloud-python/commit/854c12bbde3a5f0dcc77cabe72ecab2fd72fbac0))
* the package is now typed ([#265](https://github.com/hetznercloud/hcloud-python/issues/265)) ([da8baa5](https://github.com/hetznercloud/hcloud-python/commit/da8baa551628fb759c790871362fef1e3666c56b))


### Bug Fixes

* allow omitting `datacenter` when creating a primary ip ([#171](https://github.com/hetznercloud/hcloud-python/issues/171)) ([4375dc6](https://github.com/hetznercloud/hcloud-python/commit/4375dc6ec351207380a011ec35e1397bf2bd17e9))
* ineffective doc strings ([#266](https://github.com/hetznercloud/hcloud-python/issues/266)) ([bb34df9](https://github.com/hetznercloud/hcloud-python/commit/bb34df9390030e70f39bb82c92f4040eef18eb3b))
* invalid attribute in placement group ([#258](https://github.com/hetznercloud/hcloud-python/issues/258)) ([23b3607](https://github.com/hetznercloud/hcloud-python/commit/23b36079d997d28d73cb9edc9a51a8c3b4481d7e))


### Dependencies

* update pre-commit hook asottile/pyupgrade to v3.10.1 ([#261](https://github.com/hetznercloud/hcloud-python/issues/261)) ([efa5780](https://github.com/hetznercloud/hcloud-python/commit/efa5780d0de3080bffe43994c064a0f1bcf6da43))
* update pre-commit hook pre-commit/mirrors-prettier to v3.0.1 ([#269](https://github.com/hetznercloud/hcloud-python/issues/269)) ([2239b0b](https://github.com/hetznercloud/hcloud-python/commit/2239b0bc9beae457215c6514b0b823cc84a4a463))
* update pre-commit hook pycqa/flake8 to v6.1.0 ([#260](https://github.com/hetznercloud/hcloud-python/issues/260)) ([fd01384](https://github.com/hetznercloud/hcloud-python/commit/fd013842f7f94e98520ed403a8cd91b68a4c4e5c))


### Documentation

* update documentation ([#247](https://github.com/hetznercloud/hcloud-python/issues/247)) ([e63741f](https://github.com/hetznercloud/hcloud-python/commit/e63741fab50524f4e4098af5c77f806915ae93c8))
* update hetzner logo ([#264](https://github.com/hetznercloud/hcloud-python/issues/264)) ([ee79851](https://github.com/hetznercloud/hcloud-python/commit/ee79851dbf00e50d7f6b398fd4323f3e14831831))

## [1.26.0](https://github.com/hetznercloud/hcloud-python/compare/v1.25.0...v1.26.0) (2023-07-19)


### Features

* add __repr__ method to domains ([#246](https://github.com/hetznercloud/hcloud-python/issues/246)) ([4c22765](https://github.com/hetznercloud/hcloud-python/commit/4c227659bfb61551e44c41315b135039576960d3))
* drop support for python 3.7 ([#242](https://github.com/hetznercloud/hcloud-python/issues/242)) ([2ce71e9](https://github.com/hetznercloud/hcloud-python/commit/2ce71e9ded5e9bb87ce96519ce59db942f4f9670))

## [1.25.0](https://github.com/hetznercloud/hcloud-python/compare/v1.24.0...v1.25.0) (2023-07-14)


### Features

* add details to raise exceptions ([#240](https://github.com/hetznercloud/hcloud-python/issues/240)) ([cf64e54](https://github.com/hetznercloud/hcloud-python/commit/cf64e549a2b28aea91062dea67db8733b4ecdd6f))
* move hcloud.hcloud module to hcloud._client ([#243](https://github.com/hetznercloud/hcloud-python/issues/243)) ([413472d](https://github.com/hetznercloud/hcloud-python/commit/413472d7af1602b872a9b56324b9bffd0067eee6))


### Dependencies

* update pre-commit hook asottile/pyupgrade to v3.9.0 ([#238](https://github.com/hetznercloud/hcloud-python/issues/238)) ([0053ded](https://github.com/hetznercloud/hcloud-python/commit/0053ded5a1d0c2407134706830dd8ff3d4d1e8ce))
* update pre-commit hook pre-commit/mirrors-prettier to v3 ([#235](https://github.com/hetznercloud/hcloud-python/issues/235)) ([047d4e1](https://github.com/hetznercloud/hcloud-python/commit/047d4e173a53e91252d57d01b2e95def1c4949d9))
* update pre-commit hook psf/black to v23.7.0 ([#239](https://github.com/hetznercloud/hcloud-python/issues/239)) ([443bf26](https://github.com/hetznercloud/hcloud-python/commit/443bf262cb524dd674d2007db8100fec94dab80d))

## [1.24.0](https://github.com/hetznercloud/hcloud-python/compare/v1.23.1...v1.24.0) (2023-07-03)


### Features

* revert remove python-dateutil dependency ([#231](https://github.com/hetznercloud/hcloud-python/issues/231)) ([945bfde](https://github.com/hetznercloud/hcloud-python/commit/945bfde2ff0f64896e5c4d017e69236913e9d9dd)), closes [#226](https://github.com/hetznercloud/hcloud-python/issues/226)


### Dependencies

* update pre-commit hook asottile/pyupgrade to v3.8.0 ([#232](https://github.com/hetznercloud/hcloud-python/issues/232)) ([27f21bc](https://github.com/hetznercloud/hcloud-python/commit/27f21bc41e17a800a8a3bed1df7935e7fb31de42))

## [1.23.1](https://github.com/hetznercloud/hcloud-python/compare/v1.23.0...v1.23.1) (2023-06-30)


### Bug Fixes

* handle Z timezone in ISO8601 datetime format ([#228](https://github.com/hetznercloud/hcloud-python/issues/228)) ([6a5c3f4](https://github.com/hetznercloud/hcloud-python/commit/6a5c3f42c092610c4a82cb79c0052499563549dc)), closes [#226](https://github.com/hetznercloud/hcloud-python/issues/226)

## [1.23.0](https://github.com/hetznercloud/hcloud-python/compare/v1.22.0...v1.23.0) (2023-06-26)


### Features

* remove python-dateutil dependency ([#221](https://github.com/hetznercloud/hcloud-python/issues/221)) ([8ea4aa0](https://github.com/hetznercloud/hcloud-python/commit/8ea4aa0ad12e85eeb14c81dfa2195e1a6ee79a76))


### Bug Fixes

* **isos:** invalid name for include_wildcard_architecture argument ([#222](https://github.com/hetznercloud/hcloud-python/issues/222)) ([c3dfcab](https://github.com/hetznercloud/hcloud-python/commit/c3dfcaba44d88fcf6913a6e68caee2afde06e551))


### Dependencies

* update dependency pytest to &gt;=7.4,&lt;7.5 ([#217](https://github.com/hetznercloud/hcloud-python/issues/217)) ([11e1f45](https://github.com/hetznercloud/hcloud-python/commit/11e1f455611b17a22328b3422d0b800552ea91e3))

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

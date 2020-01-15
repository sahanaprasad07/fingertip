#!/usr/bin/python3
import fingertip

BASES = dict(
    podman_centos=lambda: fingertip.build('backend.podman-criu', 'centos'),
    podman_fedora=lambda: fingertip.build('backend.podman-criu', 'fedora'),
    podman_alpine=lambda: (
        fingertip.build('backend.podman-criu').apply('os.alpine')
    ),
    podman_ubuntu=lambda: (
        fingertip
        .build('backend.podman-criu', 'ubuntu')
        .apply('backend.podman-criu.exec', 'apt update&&apt install -y python')
    ),
    qemu_alpine=lambda: fingertip.build('os.alpine'),
    qemu_fedora=lambda: fingertip.build('os.fedora'),
)

TESTS = dict(
    uname=lambda m: m.apply('ansible', 'command', 'uname -a'),
    patch=lambda m: m.apply('ansible', 'package',
                            name='patch', state='present'),
    xtrue=lambda m: m.apply('ssh.exec', 'true') if hasattr(m, 'ssh') else None,
    greet=lambda m: m.apply('self_test.greeting'),
    prmpt=lambda m: m.apply('self_test.prompts'),
    subsh=lambda m: m.apply('self_test.subshell'),
    wait4=lambda m: m.apply('self_test.wait_for_it'),
)

SKIP = (
    ('qemu_fedora', 'prmpt'),  # takes too much time
    ('podman_alpine', 'wait4'),  # shell poorly snapshottable with CRIU (ash)
    ('podman_alpine', 'subsh'),  # shell poorly snapshottable with CRIU (ash)
    ('podman_ubuntu', 'wait4'),  # shell poorly snapshottable with CRIU (dash)
    ('podman_ubuntu', 'subsh'),  # shell poorly snapshottable with CRIU (ash)
)

for base_name, base in BASES.items():
    for test_name, test in TESTS.items():
        if (base_name, test_name) in SKIP:
            continue

        test(base())
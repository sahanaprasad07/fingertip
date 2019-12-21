# Licensed under GNU General Public License v3 or later, see COPYING.
# Copyright (c) 2019 Red Hat, Inc., see CONTRIBUTORS.


def setup(m, greeting='Hello!'):
    with m:
        m.console.sendline('PS1=@"parent> "')
        m.console.expect_exact('@parent> ')
        m.console.sendline('PS1=@"child> " sh')
        m.console.expect_exact('@child> ')
        return m


def main(m, greeting='Hello!'):
    with m.apply(setup, greeting=greeting).transient() as m:
        m.console.sendline('')
        m.console.expect_exact('@child> ')
        m.console.sendcontrol('d')
        m.console.expect_exact('@parent> ')

#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/monit.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main._tmpl import TMPL

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md'


def run_module():
    module_args = dict(
        name=dict(type='str', required=True, description='Unique test name'),
        type=dict(
            type='str', required=False, default='Custom',  # required for create
            choises=[
                'Existence', 'SystemResource', 'ProcessResource', 'ProcessDiskIO',
                'FileChecksum', 'Timestamp', 'FileSize', 'FileContent', 'FilesystemMountFlags',
                'SpaceUsage', 'InodeUsage', 'DiskIO', 'Permisssion', 'UID', 'GID', 'PID', 'PPID',
                'Uptime', 'ProgramStatus', 'NetworkInterface', 'NetworkPing', 'Connection', 'Custom',
            ]
        ),
        condition=dict(type='str', required=False),  # required for create
        action=dict(
            type='str', required=False,  # required for create
            choises=['alert', 'restart', 'start', 'stop', 'exec', 'unmonitor']
        ),
        path=dict(type='path', required=False),
        **STATE_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    tmpl = TMPL(module=module, result=result)

    def process():
        tmpl.check()
        # tmpl.process()
        # if result['changed'] and module.params['reload']:
        #     tmpl.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='monit_test.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    tmpl.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

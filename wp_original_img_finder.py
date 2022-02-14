#!/usr/bin/env python3

"""
Paves the way for the uploads to sync locally, by analysing the provided
paths. This is needed because WordPress resizes the originals automatically,
and these aren't worth backing up, save for simplicity's sake. Figured if we
have a module this would make it simpler.

Loads of literature about testing. Turns out it was all just QA for getting
a module into the Ansible distribution. That's gonna be tighter than ansible
galaxy. But I've tested this, too much probably, and automating the unit
tests is plenty. Though I've been given ideas about automated integration
tests now, having only known one company's, previously.

1. create a sub-directory called "library" in the playbooks directory
2. copy the script there and refer to it without any suffix:
    >   - name: exercise own module
    >     my_first_working_module:
    >       name: hello
    >       new: true
    >    register: new_module_output
    >
    >  - debug: var=new_module_output
3. run playbook as usual


Component tests:

1. git clone git://github.com/ansible/ansible.git --recursive
  - Fix shebang for python3
2. ansible/hacking/test-module -m ./wp_original_img_finder.py -a "path=xyz"
  - the path is on the local machine; no inventory is in play here.


Integration tests:

Run manually for now.


See https://ansible.readthedocs.io/en/stable/dev_guide/developing_modules_general.html
"""

DOCUMENTATION = '''
---
module: wp_original_img_finder

short_description: Analyse the contents of the path provided
version_added: "2.12"

description:
  - Analyse the contents of the path to `wp-content/uploads/` provided.
  - Ensure directory paths are mirrored and proceed to sync original files.

options:
  path:
    description:
      - Path to `wp-content/uploads/` where the search begins from.
    required: true
author:
  - ployt0 (@ployt0)
'''

EXAMPLES = '''
# Obtain lists of directories and master image files in the default uploads path
- name: Test with a message
  wp_original_img_finder:
    path: /var/www/html/wordpress/wp-content/uploads/
'''

RETURN = '''
path_argument:
  description: The original path param that was passed in.
  returned: always
  type: str
directories:
  description: List of directories found on path.
  returned: success
  type: str
  sample: [ '/var/www/html/wp/wp-cont/uploads/2022/' ]
master_files:
  description: List of original image files found on path.
  returned: success
  type: str
  sample: [
      '/var/www/html/wp/wp-cont/uploads/2022/a.img',
      '/var/www/html/wp/wp-cont/uploads/2022/b.img'
  ]
'''

import re
from typing import List, Tuple, Dict
from ansible.module_utils.basic import AnsibleModule
from pathlib import Path
import os


def file_is_src_of(potential_src: str, potential_derivative: str) -> bool:
    """
    All input paths must have been stripped of their extensions.

    :param potential_src:
    :param potential_derivative:
    :return:
    """
    if not potential_derivative.startswith(potential_src):
        return False
    extension = potential_derivative[len(potential_src):]
    return re.match(r"^-\d+x\d+$", extension) is not None


def find_derived_filenames(files: List[str]) -> Dict[str, List[str]]:
    """
    :param files: must have been stripped of their extensions.
    :return: mapping of each source file to a list of its derivatives.
    """
    src_derivatives = {}
    for i, fqn1 in enumerate(files):
        file_1, ext_1 = os.path.splitext(fqn1)
        for fqn2 in files[i+1:]:
            file_2, ext_2 = os.path.splitext(fqn2)
            if ext_1 != ext_2:
                continue
            if file_is_src_of(file_1, file_2):
                src_derivatives.setdefault(fqn1, []).append(fqn2)
            elif file_is_src_of(file_2, file_1):
                src_derivatives.setdefault(fqn2, []).append(fqn1)
    return src_derivatives


def get_dirs_and_files(root_path: str) -> Tuple[List[str], List[str]]:
    """
    :param root_path: where the path exploration begins.
    :return: list of directories, list of files.
    """
    # This rglob will need updating for supported image types if we are in
    # danger of cloning other media.
    list_result = list(map(str, Path(root_path).rglob("*")))
    directories = []
    files = []
    for entry in list_result:
        if os.path.isdir(entry):
            directories.append(entry)
        else:
            files.append(entry)
    return directories, files


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True)
        ),
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        path_argument=module.params['path']
    )

    if module.params['path'] == 'fail me':
        module.fail_json(failed=True, msg='You requested this to fail', **result)

    if not os.path.exists(module.params['path']):
        module.fail_json(failed=True, msg='Path not present on target.', **result)

    directories, files = get_dirs_and_files(module.params['path'])
    src_derivatives = find_derived_filenames(files)
    result['directories'] = directories
    result['master_files'] = list(src_derivatives.keys())

    module.exit_json(**result)


if __name__ == '__main__':
    main()

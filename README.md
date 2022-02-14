# ansible_mod_id_master_images
Ansible module, with tests and brief documentation, I can understand, on how to go about creating ansible modules in general.

The specific purpose of the module is to identify the unique images in a WordPress uploads subdirectory.
These directories are sub divided by month and year, so the module returns all these directory paths
so that the caller may recreate them for storing the images in.

What do I mean "unique images"? I mean the ones that haven't been scaled by WordPress. This assumes
images which WordPress resizes have "-[0-9]+x[0-9]+" appended to their basenames.

I decided I don't know enough about WordPress to continue development of this, for now. Also I
can forego using images, since I'm mostly just coding.

I don't know too much about Ansible either. Remember to put new modules in the "library" subfolder underneath
the playbook that uses them. I've a lot to learn!

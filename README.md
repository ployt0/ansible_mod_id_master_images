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

## Restoring

Alas this is very manual, but it is disaster recover right? Pretty pictures can wait.

What is an obstacle with restoring these backups is making the derived images again. The sqldump will
hold details of the sizes expected and I believe there are options in the WordPress UI to influence
the resized images' dimensions. The SQL won't need modifying, although re uploading images could create
duplicate entries so use the media uploader UI to delete the orhpaned images, after ascertaining their
expected sizes. You can spot the orphaned thumbnails because they have no image content.

The media uploader can then safely accept dropping the master images onto it. These of course will
end up in the path determined by the current month and year. You'll need to log onto the server
and move them manually, creating the historic directories as you go. This works, I've tried it,
and it is so much more concise to describe here than in 200 lines of playbook + 200 of test.

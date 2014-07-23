Vagrant.configure("2") do |config|

  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.provider :virtualbox do |vb|
    vb.customize [ "setextradata", :id,
                   "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1" ]
  end

  config.vm.network :private_network, ip: "10.18.6.30"

  config.vm.synced_folder "./", "/var/django/caesar", group: 'www-data'

  config.vm.provision :shell, :inline => <<SCRIPT

# Setup needed by all Caesar installs
/var/django/caesar/setup.sh

# Setup specific to Vagrant -- make a folder for the sqlite3 database.  We can't
# just store it in the shared folder /var/django/caesar, because Sqlite3 needs to
# lock the database file and Windows hosts don't support locking in the shared folder.
mkdir -p /var/django/db
touch /var/django/db/caesar.sqlite3
chown -R vagrant /var/django/db
chgrp -R www-data /var/django/db
chmod -R g+w /var/django/db

SCRIPT

end

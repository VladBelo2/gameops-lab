Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.hostname = "gameops-lab"
  config.vm.network "private_network", ip: "192.168.56.156"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 4096
    vb.cpus = 2
  end

  config.vm.provision "shell", path: "provision.sh"
  # config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox", rsync__exclude: [".venv/"]
end

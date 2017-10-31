VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.ssh.insert_key = false

    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end
    
  config.vm.define "upvotebot-ubuntu" do |app|
    app.vm.hostname = "upvotebot.dev"
    app.vm.network "private_network", ip: "192.168.101.101", auto_config: false
    app.vm.box = "bento/ubuntu-16.04"
    app.vm.network "forwarded_port", guest: 80, host: 8082
    app.vm.network "forwarded_port", guest: 8001, host: 8081
  end

end

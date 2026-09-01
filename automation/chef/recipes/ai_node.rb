package %w[containerd chrony]

service 'containerd' do
  action [:enable, :start]
end

file '/etc/sysctl.d/99-ai-fabric.conf' do
  content "net.ipv4.ip_forward=1\n"
  mode '0644'
  notifies :run, 'execute[reload-sysctl]', :immediately
end

execute 'reload-sysctl' do
  command 'sysctl --system'
  action :nothing
end

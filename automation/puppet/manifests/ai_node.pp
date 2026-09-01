class ai_factory::node {
  package { 'containerd': ensure => installed }
  package { 'chrony': ensure => installed }
  service { 'containerd': ensure => running, enable => true, require => Package['containerd'] }
  file { '/etc/sysctl.d/99-ai-fabric.conf':
    ensure  => file,
    mode    => '0644',
    content => "net.ipv4.ip_forward=1\n",
  }
}

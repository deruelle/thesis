%define mss_source mss-1.5.0.FINAL-jboss-jdk6-5.1.0.GA
%define mss_version 1012212016-LGPL
%define server_path server

Summary:        Mobicents Sip Load Balancer
Name:           mobicents-load-balancer
Version:        1.5.final
Release:        1
License:        GPL
BuildArch:      noarch
Group:          Applications/System
Source0:        http://sourceforge.net/projects/mobicents/files/Mobicents%20Sip%20Servlets/Mobicents%20Sip%20Servlets%201.5.0.FINAL/%{mss_source}-%{mss_version}.zip
Source1:        mobicents-load-balancer.init
Requires:       java-1.6.0-openjdk
Requires(post): /sbin/chkconfig
BuildRoot:      /tmp/mss


%description
The Mobicents Sip Load Balancer

%prep
# Untar the source to BUILD/.
# The -c option is set to create a folder of the same name as the package.
# The -q option means quiet.
%setup -c -q


%install
# CD in the BUILD directory.
cd %{_topdir}/BUILD

# Clean the BUILDROOT directory.
rm -fr $RPM_BUILD_ROOT

# Copy mobicents to BUILDROOT
install -d -m 775 $RPM_BUILD_ROOT/%{server_path}/%{name}
cp -R %{name}-%{version}/%{mss_source}/sip-balancer/* $RPM_BUILD_ROOT/%{server_path}/%{name}/

# Give very permissive rights.
chmod -R 775 $RPM_BUILD_ROOT/%{server_path}/%{name}

# install the service init script
install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

# install the options file
install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig
 
echo "MOBICENTS_VERSION=%{version}"           	   > $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "MOBICENTS_HOME=/%{server_path}/%{name}" 	  >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}


%post
/sbin/chkconfig --add mobicents-load-balancer
/sbin/chkconfig mobicents-load-balancer on


%clean
# Clean the BUILDROOT directory.
rm -fr $RPM_BUILD_ROOT


%files
# This package is responsible of the all folder below.
%defattr(-,root,root)
/%{server_path}/%{name}/
%{_initrddir}/%{name}
/etc/sysconfig/%{name}


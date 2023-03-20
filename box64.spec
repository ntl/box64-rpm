%global debug_package %{nil}
%global pkg_name box64

Name:       %{pkg_name}
Version:    0.0.git.2571.4a5a9a18
Release:    1%{?dist}
Summary:    Linux Userspace x86_64 Emulator with a twist, targeted at ARM64 Linux devices
License:    MIT
URL:        https://github.com/robertzaage/box64
BuildArch:  noarch

Source:     box64-4a5a9a18.tar.gz

Provides:   %{pkg_name} = %{version}
Recommends:    gl4es
BuildRequires: git cmake make gcc gcc-c++

%description
Box64 lets you run x86_64 Linux programs (such as games) on non-x86_64 Linux systems, like ARM (host system needs to be 64-bit little-endian).

%prep
%setup -T -b 0 -q -n box64
mkdir -p build && cd build
cmake .. -DARM_DYNAREC=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=/usr

%build
cd build
make -j$(nproc)

%install
#cat system/box64.conf.cmake > %{_sysconfdir}/binfmt.d/box64.conf
cp build/system/box64.conf %{_sysconfdir}/binfmt.d
cp x64lib/libstdc++.so.5 %{_lib}
cp x64lib/libstdc++.so.6 %{_lib}
cp x64lib/libgcc_s.so.1 %{_lib}
cp x64lib/libpng12.so.0 %{_lib}
cp system/box64.box64rc %{_sysconfdir}

%post -n %{name}
systemctl restart systemd-binfmt

%files
%license LICENSE
%doc README.md
%{_lib}/libstdc++.so.5
%{_lib}/libstdc++.so.6
%{_lib}/libgcc_s.so.1
%{_lib}/libpng12.so.0
%{_sysconfdir}/box64.box64rc
%{_sysconfdir}/binfmt.d/box64.conf

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
